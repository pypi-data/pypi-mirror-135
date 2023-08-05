# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
# with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "LICENSE.txt" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime

from aws_cdk import aws_batch as batch
from aws_cdk import aws_cloudformation as cfn
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as awslambda
from aws_cdk import aws_logs as logs
from aws_cdk.core import CfnOutput, CfnResource, Construct, Fn, Stack

from pcluster.config.cluster_config import AwsBatchClusterConfig, CapacityType, SharedStorageType
from pcluster.constants import AWSBATCH_CLI_REQUIREMENTS, CW_LOG_GROUP_NAME_PREFIX, IAM_ROLE_PATH
from pcluster.models.s3_bucket import S3Bucket
from pcluster.templates.cdk_builder_utils import (
    PclusterLambdaConstruct,
    add_lambda_cfn_role,
    get_assume_role_policy_document,
    get_cloud_watch_logs_policy_statement,
    get_cloud_watch_logs_retention_days,
    get_custom_tags,
    get_default_instance_tags,
    get_log_group_deletion_policy,
    get_mount_dirs_by_type,
    get_queue_security_groups_full,
    get_shared_storage_ids_by_type,
)


class AwsBatchConstruct(Construct):
    """Create the resources required when using AWS Batch as a scheduler."""

    def __init__(
        self,
        scope: Construct,
        id: str,
        cluster_config: AwsBatchClusterConfig,
        stack_name: str,
        bucket: S3Bucket,
        create_lambda_roles: bool,
        compute_security_groups: dict,
        shared_storage_mappings: dict,
        shared_storage_options: dict,
        head_node_instance: ec2.CfnInstance,
        instance_roles: dict,
        **kwargs,
    ):
        super().__init__(scope, id)
        self.stack_name = stack_name
        self.stack_scope = scope
        self.config = cluster_config
        self.bucket = bucket
        self.create_lambda_roles = create_lambda_roles
        self.compute_security_groups = compute_security_groups
        self.shared_storage_mappings = shared_storage_mappings
        self.shared_storage_options = shared_storage_options
        self.head_node_instance = head_node_instance
        self.instance_roles = instance_roles

        # Currently AWS batch integration supports a single queue and a single compute resource
        self.queue = self.config.scheduling.queues[0]
        self.compute_resource = self.queue.compute_resources[0]

        self._add_resources()
        self._add_outputs()

    # -- Utility methods --------------------------------------------------------------------------------------------- #

    @property
    def _stack_account(self):
        return Stack.of(self).account

    @property
    def _stack_region(self):
        return Stack.of(self).region

    @property
    def _url_suffix(self):
        return Stack.of(self).url_suffix

    def _stack_unique_id(self):
        return Fn.select(2, Fn.split("/", Stack.of(self).stack_id))

    def _format_arn(self, **kwargs):
        return Stack.of(self).format_arn(**kwargs)

    def _stack_id(self):
        return Stack.of(self).stack_id

    def _get_compute_env_prefix(self):
        return Fn.select(1, Fn.split("compute-environment/", self._compute_env.ref))

    def _cluster_scoped_iam_path(self):
        """Return a path to be associated IAM roles and instance profiles."""
        return f"{IAM_ROLE_PATH}{self.stack_name}/"

    # -- Resources --------------------------------------------------------------------------------------------------- #

    def _add_resources(self):

        # Augment head node instance profile with Batch-specific policies, only add policies to Role craeted by
        # ParallelCluster
        if self.instance_roles.get("HeadNode"):
            self._add_batch_head_node_policies_to_role()

        # Iam Roles
        self._ecs_instance_role, self._iam_instance_profile = self._add_ecs_instance_role_and_profile()

        # Spot Iam Role
        self._spot_iam_fleet_role = None
        if self.queue.capacity_type == CapacityType.SPOT:
            self._spot_iam_fleet_role = self._add_spot_fleet_iam_role()

        # Batch resources
        self._compute_env = self._add_compute_env()
        self._job_queue = self._add_job_queue()
        self._job_role = self._add_job_role()
        self._docker_images_repo = self._add_docker_images_repo()
        self._job_definition_serial = self._add_job_definition_serial()
        self._job_definition_mnp = self._add_job_definition_mnp()
        self._batch_user_role = self._add_batch_user_role()

        # Code build resources
        self._code_build_role = self._add_code_build_role()
        self._code_build_policy = self._add_code_build_policy()
        self._docker_build_wait_condition_handle = self._add_docker_build_wait_condition_handle()
        self._code_build_image_builder_project = self._add_code_build_docker_image_builder_project()

        # Docker image management
        self._manage_docker_images_lambda = self._add_manage_docker_images_lambda()
        self._manage_docker_images_custom_resource = self._add_manage_docker_images_custom_resource()
        self._docker_build_wait_condition = self._add_docker_build_wait_condition()
        self._docker_build_wait_condition.add_depends_on(self._manage_docker_images_custom_resource)

        # Code build notification
        self._code_build_notification_lambda = self._add_code_build_notification_lambda()
        self._code_build_notification_lambda.add_depends_on(self._docker_build_wait_condition_handle)
        self._code_build_notification_rule = self._add_code_build_notification_rule()
        self._manage_docker_images_custom_resource.add_depends_on(self._code_build_notification_rule)

    def _add_compute_env(self):
        return batch.CfnComputeEnvironment(
            self.stack_scope,
            "ComputeEnvironment",
            type="MANAGED",
            # service_role=self._batch_service_role.ref,
            state="ENABLED",
            compute_resources=batch.CfnComputeEnvironment.ComputeResourcesProperty(
                type="SPOT" if self.queue.capacity_type == CapacityType.SPOT else "EC2",
                minv_cpus=self.compute_resource.min_vcpus,
                desiredv_cpus=self.compute_resource.desired_vcpus,
                maxv_cpus=self.compute_resource.max_vcpus,
                instance_types=self.compute_resource.instance_types,
                subnets=self.queue.networking.subnet_ids,
                security_group_ids=get_queue_security_groups_full(self.compute_security_groups, self.queue),
                instance_role=self._iam_instance_profile.ref,
                bid_percentage=self.compute_resource.spot_bid_percentage,
                spot_iam_fleet_role=self._spot_iam_fleet_role.attr_arn if self._spot_iam_fleet_role else None,
                tags={
                    **get_default_instance_tags(
                        self.stack_name,
                        self.config,
                        self.compute_resource,
                        "Compute",
                        self.shared_storage_mappings,
                        raw_dict=True,
                    ),
                    **get_custom_tags(self.config, raw_dict=True),
                },
            ),
        )

    def _add_job_queue(self):
        return batch.CfnJobQueue(
            self.stack_scope,
            "JobQueue",
            priority=1,
            compute_environment_order=[
                batch.CfnJobQueue.ComputeEnvironmentOrderProperty(
                    compute_environment=self._compute_env.ref,
                    order=1,
                )
            ],
        )

    def _add_ecs_instance_role_and_profile(self):
        ecs_instance_role = iam.CfnRole(
            self.stack_scope,
            "EcsInstanceRole",
            path=self._cluster_scoped_iam_path(),
            managed_policy_arns=[
                self._format_arn(
                    service="iam",
                    account="aws",
                    region="",
                    resource="policy/service-role/AmazonEC2ContainerServiceforEC2Role",
                )
            ],
            assume_role_policy_document=get_assume_role_policy_document(f"ec2.{self._url_suffix}"),
        )

        iam_instance_profile = iam.CfnInstanceProfile(
            self.stack_scope, "IamInstanceProfile", path=self._cluster_scoped_iam_path(), roles=[ecs_instance_role.ref]
        )

        return ecs_instance_role, iam_instance_profile

    def _add_job_role(self):
        return iam.CfnRole(
            self.stack_scope,
            "JobRole",
            path=self._cluster_scoped_iam_path(),
            managed_policy_arns=[
                self._format_arn(service="iam", account="aws", region="", resource="policy/AmazonS3ReadOnlyAccess"),
                self._format_arn(
                    service="iam",
                    account="aws",
                    region="",
                    resource="policy/service-role/AmazonECSTaskExecutionRolePolicy",
                ),
            ],
            assume_role_policy_document=get_assume_role_policy_document("ecs-tasks.amazonaws.com"),
            policies=[
                iam.CfnRole.PolicyProperty(
                    policy_name="s3PutObject",
                    policy_document=iam.PolicyDocument(
                        statements=[
                            iam.PolicyStatement(
                                actions=["s3:PutObject"],
                                effect=iam.Effect.ALLOW,
                                resources=[
                                    self._format_arn(
                                        service="s3",
                                        resource=f"{self.bucket.name}/{self.bucket.artifact_directory}/batch/*",
                                        region="",
                                        account="",
                                    ),
                                ],
                                sid="CloudWatchLogsPolicy",
                            ),
                        ],
                    ),
                ),
                iam.CfnRole.PolicyProperty(
                    policy_name="cfnDescribeStacks",
                    policy_document=iam.PolicyDocument(
                        statements=[
                            iam.PolicyStatement(
                                actions=["cloudformation:DescribeStacks"],
                                effect=iam.Effect.ALLOW,
                                resources=[
                                    self._format_arn(
                                        service="cloudformation",
                                        resource=f"stack/{self.stack_name}/*",
                                    ),
                                    self._format_arn(
                                        # ToDo: This resource is for substack. Check if this is necessary for pcluster3
                                        service="cloudformation",
                                        resource=f"stack/{self.stack_name}-*/*",
                                    ),
                                ],
                                sid="CloudWatchLogsPolicy",
                            ),
                        ],
                    ),
                ),
            ],
        )

    def _add_docker_images_repo(self):
        return ecr.CfnRepository(self.stack_scope, "ParallelClusterDockerImagesRepo")

    def _add_job_definition_serial(self):
        return batch.CfnJobDefinition(
            self.stack_scope,
            "JobDefinitionSerial",
            type="container",
            container_properties=self._get_container_properties(),
        )

    def _add_job_definition_mnp(self):
        return batch.CfnJobDefinition(
            self.stack_scope,
            "JobDefinitionMNP",
            type="multinode",
            node_properties=batch.CfnJobDefinition.NodePropertiesProperty(
                main_node=0,
                num_nodes=1,
                node_range_properties=[
                    batch.CfnJobDefinition.NodeRangePropertyProperty(
                        target_nodes="0:", container=self._get_container_properties()
                    )
                ],
            ),
        )

    def _add_batch_user_role(self):
        batch_user_role_statement = iam.PolicyStatement(effect=iam.Effect.ALLOW, actions=["sts:AssumeRole"])
        batch_user_role_statement.add_account_root_principal()

        return iam.CfnRole(
            self.stack_scope,
            "PclusterBatchUserRole",
            path=self._cluster_scoped_iam_path(),
            max_session_duration=36000,
            assume_role_policy_document=iam.PolicyDocument(statements=[batch_user_role_statement]),
            policies=[
                iam.CfnRole.PolicyProperty(
                    policy_name="BatchUserPolicy",
                    policy_document=iam.PolicyDocument(
                        statements=[
                            iam.PolicyStatement(
                                actions=[
                                    "batch:SubmitJob",
                                    "cloudformation:DescribeStacks",
                                    "ecs:ListContainerInstances",
                                    "ecs:DescribeContainerInstances",
                                    "logs:GetLogEvents",
                                    "logs:FilterLogEvents",
                                    "s3:PutObject",
                                    "s3:Get*",
                                    "s3:DeleteObject",
                                    "iam:PassRole",
                                ],
                                effect=iam.Effect.ALLOW,
                                resources=[
                                    self._job_definition_serial.ref,
                                    self._job_definition_mnp.ref,
                                    self._job_queue.ref,
                                    self._job_role.attr_arn,
                                    self._format_arn(service="cloudformation", resource=f"stack/{self.stack_name}/*"),
                                    # ToDo: This resource is for substack. Check if this is necessary for pcluster3
                                    self._format_arn(service="cloudformation", resource=f"stack/{self.stack_name}-*/*"),
                                    self._format_arn(
                                        service="s3",
                                        resource=f"{self.bucket.name}/{self.bucket.artifact_directory}/batch/*",
                                        region="",
                                        account="",
                                    ),
                                    self._format_arn(
                                        service="ecs",
                                        resource=f"cluster/{self._get_compute_env_prefix()}_Batch_*",
                                        region=self._stack_region,
                                        account=self._stack_account,
                                    ),
                                    self._format_arn(
                                        service="ecs",
                                        resource="container-instance/*",
                                        region=self._stack_region,
                                        account=self._stack_account,
                                    ),
                                    self._format_arn(
                                        service="logs",
                                        resource="log-group:/aws/batch/job:log-stream:*",
                                        region=self._stack_region,
                                        account=self._stack_account,
                                    ),
                                ],
                            ),
                            iam.PolicyStatement(
                                effect=iam.Effect.ALLOW,
                                actions=["s3:List*"],
                                resources=[
                                    self._format_arn(service="s3", resource=self.bucket.name, region="", account=""),
                                ],
                            ),
                            iam.PolicyStatement(
                                effect=iam.Effect.ALLOW,
                                actions=[
                                    "batch:DescribeJobQueues",
                                    "batch:TerminateJob",
                                    "batch:DescribeJobs",
                                    "batch:CancelJob",
                                    "batch:DescribeJobDefinitions",
                                    "batch:ListJobs",
                                    "batch:DescribeComputeEnvironments",
                                    "ec2:DescribeInstances",
                                ],
                                resources=["*"],
                            ),
                        ],
                    ),
                ),
                iam.CfnRole.PolicyProperty(
                    policy_name="cfnDescribeStacks",
                    policy_document=iam.PolicyDocument(
                        statements=[
                            iam.PolicyStatement(
                                actions=["cloudformation:DescribeStacks"],
                                effect=iam.Effect.ALLOW,
                                resources=[
                                    self._format_arn(
                                        service="cloudformation",
                                        resource=f"stack/{self.stack_name}/*",
                                    ),
                                    self._format_arn(
                                        # ToDo: This resource is for substack. Check if this is necessary for pcluster3
                                        service="cloudformation",
                                        resource=f"stack/{self.stack_name}-*/*",
                                    ),
                                ],
                                sid="CloudWatchLogsPolicy",
                            ),
                        ],
                    ),
                ),
            ],
        )

    def _add_spot_fleet_iam_role(self):
        return iam.CfnRole(
            self.stack_scope,
            "BatchSpotRole",
            path=self._cluster_scoped_iam_path(),
            managed_policy_arns=[
                self._format_arn(
                    service="iam",
                    account="aws",
                    region="",
                    resource="policy/service-role/AmazonEC2SpotFleetTaggingRole",
                )
            ],
            assume_role_policy_document=get_assume_role_policy_document("spotfleet.amazonaws.com"),
        )

    def _get_container_properties(self):
        return batch.CfnJobDefinition.ContainerPropertiesProperty(
            job_role_arn=self._job_role.attr_arn,
            image="{account}.dkr.ecr.{region}.{url_suffix}/{docker_images_repo}:{os}".format(
                account=self._stack_account,
                region=self._stack_region,
                url_suffix=self._url_suffix,
                docker_images_repo=self._docker_images_repo.ref,
                os=self.config.image.os,
            ),
            vcpus=1,
            memory=512,
            privileged=True,
            environment=[
                batch.CfnJobDefinition.EnvironmentProperty(name="PCLUSTER_AWS_REGION", value=self._stack_region),
                batch.CfnJobDefinition.EnvironmentProperty(name="PCLUSTER_STACK_NAME", value=self.stack_name),
                batch.CfnJobDefinition.EnvironmentProperty(
                    name="PCLUSTER_SHARED_DIRS",
                    value=get_mount_dirs_by_type(self.shared_storage_options, SharedStorageType.EBS),
                ),
                batch.CfnJobDefinition.EnvironmentProperty(
                    name="PCLUSTER_EFS_SHARED_DIR",
                    value=get_mount_dirs_by_type(self.shared_storage_options, SharedStorageType.EFS),
                ),
                batch.CfnJobDefinition.EnvironmentProperty(
                    name="PCLUSTER_EFS_FS_ID",
                    value=get_shared_storage_ids_by_type(self.shared_storage_mappings, SharedStorageType.EFS),
                ),
                batch.CfnJobDefinition.EnvironmentProperty(
                    name="PCLUSTER_RAID_SHARED_DIR",
                    value=get_mount_dirs_by_type(self.shared_storage_options, SharedStorageType.RAID),
                ),
                batch.CfnJobDefinition.EnvironmentProperty(
                    name="PCLUSTER_HEAD_NODE_IP", value=self.head_node_instance.attr_private_ip
                ),
            ],
        )

    def _add_code_build_role(self):
        return iam.CfnRole(
            self.stack_scope,
            "CodeBuildRole",
            path=self._cluster_scoped_iam_path(),
            assume_role_policy_document=get_assume_role_policy_document("codebuild.amazonaws.com"),
        )

    def _add_code_build_policy(self):
        return iam.CfnPolicy(
            self.stack_scope,
            "CodeBuildPolicy",
            policy_name="CodeBuildPolicy",
            policy_document=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        sid="ECRRepoPolicy",
                        effect=iam.Effect.ALLOW,
                        actions=[
                            "ecr:BatchCheckLayerAvailability",
                            "ecr:CompleteLayerUpload",
                            "ecr:InitiateLayerUpload",
                            "ecr:PutImage",
                            "ecr:UploadLayerPart",
                        ],
                        resources=[self._docker_images_repo.attr_arn],
                    ),
                    iam.PolicyStatement(
                        sid="ECRPolicy", effect=iam.Effect.ALLOW, actions=["ecr:GetAuthorizationToken"], resources=["*"]
                    ),
                    get_cloud_watch_logs_policy_statement(
                        resource=self._format_arn(service="logs", account="*", region="*", resource="*")
                    ),
                    iam.PolicyStatement(
                        sid="S3GetObjectPolicy",
                        effect=iam.Effect.ALLOW,
                        actions=["s3:GetObject", "s3:GetObjectVersion"],
                        resources=[
                            self._format_arn(
                                service="s3",
                                region="",
                                resource=f"{self.bucket.name}/{self.bucket.artifact_directory}/*",
                                account="",
                            )
                        ],
                    ),
                ]
            ),
            roles=[self._code_build_role.ref],
        )

    def _add_code_build_docker_image_builder_project(self):
        timestamp = f"{datetime.utcnow().strftime('%Y%m%d%H%M')}"
        log_group_name = (
            f"{CW_LOG_GROUP_NAME_PREFIX}codebuild/{self.stack_name}-CodeBuildDockerImageBuilderProject-{timestamp}"
        )

        log_group = logs.CfnLogGroup(
            self.stack_scope,
            "CodeBuildLogGroup",
            log_group_name=log_group_name,
            retention_in_days=get_cloud_watch_logs_retention_days(self.config),
        )
        log_group.cfn_options.deletion_policy = get_log_group_deletion_policy(self.config)

        return codebuild.CfnProject(
            self.stack_scope,
            "CodeBuildDockerImageBuilderProj",
            artifacts=codebuild.CfnProject.ArtifactsProperty(type="NO_ARTIFACTS"),
            environment=codebuild.CfnProject.EnvironmentProperty(
                compute_type="BUILD_GENERAL1_LARGE"
                if self._condition_use_arm_code_build_image()
                else "BUILD_GENERAL1_SMALL",
                environment_variables=[
                    codebuild.CfnProject.EnvironmentVariableProperty(
                        name="AWS_REGION",
                        value=self._stack_region,
                    ),
                    codebuild.CfnProject.EnvironmentVariableProperty(
                        name="AWS_ACCOUNT_ID",
                        value=self._stack_account,
                    ),
                    codebuild.CfnProject.EnvironmentVariableProperty(
                        name="IMAGE_REPO_NAME",
                        value=self._docker_images_repo.ref,
                    ),
                    codebuild.CfnProject.EnvironmentVariableProperty(
                        name="IMAGE",
                        value=self.config.image.os,
                    ),
                    codebuild.CfnProject.EnvironmentVariableProperty(
                        name="NOTIFICATION_URL",
                        value=self._docker_build_wait_condition_handle.ref,
                    ),
                ],
                image="aws/codebuild/amazonlinux2-aarch64-standard:1.0"
                if self._condition_use_arm_code_build_image()
                else "aws/codebuild/amazonlinux2-x86_64-standard:3.0",
                type="ARM_CONTAINER" if self._condition_use_arm_code_build_image() else "LINUX_CONTAINER",
                privileged_mode=True,
            ),
            name=f"pcluster-{self.stack_name}-build-docker-images-project",
            service_role=self._code_build_role.attr_arn,
            source=codebuild.CfnProject.SourceProperty(
                location=f"{self.bucket.name}/{self.bucket.artifact_directory}"
                "/custom_resources/scheduler_resources.zip",
                type="S3",
            ),
            logs_config=codebuild.CfnProject.LogsConfigProperty(
                cloud_watch_logs=codebuild.CfnProject.CloudWatchLogsConfigProperty(
                    group_name=log_group_name, status="ENABLED"
                )
            ),
        )

    def _add_manage_docker_images_lambda(self):
        manage_docker_images_lambda_execution_role = None
        if self.create_lambda_roles:

            manage_docker_images_lambda_execution_role = add_lambda_cfn_role(
                scope=self.stack_scope,
                function_id="ManageDockerImages",
                statements=[
                    iam.PolicyStatement(
                        actions=["ecr:BatchDeleteImage", "ecr:ListImages"],
                        effect=iam.Effect.ALLOW,
                        resources=[self._docker_images_repo.attr_arn],
                        sid="ECRPolicy",
                    ),
                    iam.PolicyStatement(
                        actions=["codebuild:BatchGetBuilds", "codebuild:StartBuild"],
                        effect=iam.Effect.ALLOW,
                        resources=[self._code_build_image_builder_project.attr_arn],
                        sid="CodeBuildPolicy",
                    ),
                    get_cloud_watch_logs_policy_statement(
                        resource=self._format_arn(service="logs", account="*", region="*", resource="*")
                    ),
                ],
            )

        return PclusterLambdaConstruct(
            scope=self.stack_scope,
            id="ManageDockerImagesFunctionConstruct",
            function_id="ManageDockerImages",
            bucket=self.bucket,
            config=self.config,
            execution_role=manage_docker_images_lambda_execution_role.attr_arn
            if manage_docker_images_lambda_execution_role
            else self.config.iam.roles.lambda_functions_role,
            handler_func="manage_docker_images",
            timeout=60,
        ).lambda_func

    def _add_code_build_notification_rule(self):
        code_build_notification_rule = events.CfnRule(
            self.stack_scope,
            "CodeBuildNotificationRule",
            event_pattern={
                "detail": {
                    "build-status": ["FAILED", "STOPPED", "SUCCEEDED"],
                    "project-name": [self._code_build_image_builder_project.ref],
                },
                "detail-type": ["CodeBuild Build State Change"],
                "source": ["aws.codebuild"],
            },
            state="ENABLED",
            targets=[
                events.CfnRule.TargetProperty(
                    arn=self._code_build_notification_lambda.attr_arn,
                    id="BuildNotificationFunction",
                )
            ],
        )

        awslambda.CfnPermission(
            self.stack_scope,
            "BuildNotificationFunctionInvokePermission",
            action="lambda:InvokeFunction",
            function_name=self._code_build_notification_lambda.attr_arn,
            principal="events.amazonaws.com",
            source_arn=code_build_notification_rule.attr_arn,
        )

        return code_build_notification_rule

    def _add_code_build_notification_lambda(self):
        build_notification_lambda_execution_role = None
        if self.create_lambda_roles:
            build_notification_lambda_execution_role = add_lambda_cfn_role(
                scope=self.stack_scope,
                function_id="BuildNotification",
                statements=[
                    get_cloud_watch_logs_policy_statement(
                        resource=self._format_arn(service="logs", account="*", region="*", resource="*")
                    )
                ],
            )

        return PclusterLambdaConstruct(
            scope=self.stack_scope,
            id="BuildNotificationFunctionConstruct",
            function_id="BuildNotification",
            bucket=self.bucket,
            config=self.config,
            execution_role=build_notification_lambda_execution_role.attr_arn
            if build_notification_lambda_execution_role
            else self.config.iam.roles.lambda_functions_role,
            handler_func="send_build_notification",
            timeout=60,
        ).lambda_func

    def _add_manage_docker_images_custom_resource(self):
        return CfnResource(
            self.stack_scope,
            "ManageDockerImagesCustomResource",
            type="AWS::CloudFormation::CustomResource",
            properties={
                "ServiceToken": self._manage_docker_images_lambda.attr_arn,
                "CodeBuildProject": self._code_build_image_builder_project.ref,
                "EcrRepository": self._docker_images_repo.ref,
            },
        )

    def _add_docker_build_wait_condition_handle(self):
        return cfn.CfnWaitConditionHandle(self.stack_scope, "DockerBuildWaitHandle")

    def _add_docker_build_wait_condition(self):
        return cfn.CfnWaitCondition(
            self.stack_scope,
            "DockerBuildWaitCondition",
            handle=self._docker_build_wait_condition_handle.ref,
            timeout="3600",
        )

    def _add_batch_head_node_policies_to_role(self):
        iam.CfnPolicy(
            self,
            "ParallelClusterBatchPoliciesHeadNode",
            policy_name="parallelcluster-awsbatch-head-node",
            policy_document=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        sid="Cloudformation",
                        actions=[
                            "cloudformation:DescribeStacks",
                            "cloudformation:DescribeStackResource",
                            "cloudformation:SignalResource",
                        ],
                        effect=iam.Effect.ALLOW,
                        resources=[
                            self._format_arn(service="cloudformation", resource=f"stack/{self.stack_name}/*"),
                            # ToDo: This resource is for substack. Check if this is necessary for pcluster3
                            self._format_arn(service="cloudformation", resource=f"stack/{self.stack_name}-*/*"),
                        ],
                    ),
                    iam.PolicyStatement(
                        sid="EC2",
                        effect=iam.Effect.ALLOW,
                        actions=[
                            "ec2:DescribeInstances",
                            "ec2:DescribeInstanceStatus",
                            "ec2:DescribeVolumes",
                            "ec2:AttachVolume",
                        ],
                        resources=["*"],
                    ),
                    iam.PolicyStatement(
                        sid="S3PutObj",
                        actions=["s3:PutObject"],
                        effect=iam.Effect.ALLOW,
                        resources=[
                            self._format_arn(
                                service="s3",
                                resource=f"{self.bucket.name}/{self.bucket.artifact_directory}/batch/*",
                                region="",
                                account="",
                            )
                        ],
                    ),
                    iam.PolicyStatement(
                        sid="BatchJobPassRole",
                        actions=["iam:PassRole"],
                        effect=iam.Effect.ALLOW,
                        resources=[
                            self._format_arn(
                                service="iam",
                                region="",
                                resource=f"role{self._cluster_scoped_iam_path()}*",
                            )
                        ],
                    ),
                    iam.PolicyStatement(
                        sid="DcvLicense",
                        actions=["s3:GetObject"],
                        effect=iam.Effect.ALLOW,
                        resources=[
                            self._format_arn(
                                service="s3",
                                resource="dcv-license.{0}/*".format(self._stack_region),
                                region="",
                                account="",
                            )
                        ],
                    ),
                ]
            ),
            roles=[self.instance_roles.get("HeadNode").get("RoleRef")],
        )

    # -- Conditions -------------------------------------------------------------------------------------------------- #

    def _condition_use_arm_code_build_image(self):
        return self.config.head_node.architecture == "arm64"

    # -- Outputs ----------------------------------------------------------------------------------------------------- #

    def _add_outputs(self):

        CfnOutput(
            scope=self.stack_scope,
            id="BatchCliRequirements",
            description="List of requirements for the ParallelCluster AWS Batch CLI.",
            value=AWSBATCH_CLI_REQUIREMENTS,
        )
        CfnOutput(
            self.stack_scope,
            "BatchComputeEnvironmentArn",
            description="Compute Environment created within the cluster.",
            value=self._compute_env.ref,
        )
        CfnOutput(
            self.stack_scope,
            "BatchJobQueueArn",
            description="Job Queue created within the cluster.",
            value=self._job_queue.ref,
        )
        CfnOutput(
            self.stack_scope,
            "BatchJobDefinitionArn",
            description="Job Definition for serial submission.",
            value=self._job_definition_serial.ref,
        )
        CfnOutput(
            self.stack_scope,
            "ECRRepoName",
            description="Name of the ECR repository where docker images used by AWS Batch are located.",
            value=self._docker_images_repo.ref,
        )
        CfnOutput(
            self.stack_scope,
            "CodeBuildDockerImageBuilderProject",
            description="CodeBuild project used to bake docker images.",
            value=self._code_build_image_builder_project.ref,
        )
        CfnOutput(
            self.stack_scope,
            "BatchJobDefinitionMnpArn",
            description="Job Definition for MNP submission.",
            value=self._job_definition_mnp.ref,
        )
        CfnOutput(
            self.stack_scope,
            "BatchUserRole",
            description="Role to be used to contact AWS Batch resources created within the cluster.",
            value=self._batch_user_role.ref,
        )
