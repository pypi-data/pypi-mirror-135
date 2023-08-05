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
import re
from typing import List

from botocore.exceptions import ClientError

from pcluster import utils
from pcluster.aws.aws_resources import ImageInfo, InstanceTypeInfo
from pcluster.aws.common import AWSClientError, AWSExceptionHandler, Boto3Client, Cache, ImageNotFoundError, get_region
from pcluster.constants import (
    IMAGE_NAME_PART_TO_OS_MAP,
    IMAGEBUILDER_ARN_TAG,
    IMAGEBUILDER_RESOURCE_NAME_PREFIX,
    OS_TO_IMAGE_NAME_PART_MAP,
    PCLUSTER_IMAGE_BUILD_STATUS_TAG,
    PCLUSTER_IMAGE_ID_TAG,
    SUPPORTED_ARCHITECTURES,
)
from pcluster.utils import get_partition


class Ec2Client(Boto3Client):
    """Implement EC2 Boto3 client."""

    def __init__(self):
        super().__init__("ec2")
        self.additional_instance_types_data = {}

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def list_instance_types(self) -> List[str]:
        """Return a list of instance types."""
        return [offering.get("InstanceType") for offering in self.describe_instance_type_offerings()] + list(
            self.additional_instance_types_data.keys()
        )

    @AWSExceptionHandler.handle_client_exception
    def describe_instance_type_offerings(self, filters=None, location_type=None):
        """Return a list of instance types."""
        kwargs = {"Filters": filters} if filters else {}
        if location_type:
            kwargs["LocationType"] = location_type
        return list(self._paginate_results(self._client.describe_instance_type_offerings, **kwargs))

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def get_default_instance_type(self):
        """If current region support free tier, return the free tier instance type. Otherwise, return t3.micro."""
        kwargs = {
            "Filters": [
                {"Name": "free-tier-eligible", "Values": ["true"]},
                {"Name": "current-generation", "Values": ["true"]},
            ]
        }
        free_tier_instance_type = list(self._paginate_results(self._client.describe_instance_types, **kwargs))
        return free_tier_instance_type[0]["InstanceType"] if free_tier_instance_type else "t3.micro"

    @AWSExceptionHandler.handle_client_exception
    def describe_subnets(self, subnet_ids):
        """Return a list of subnets."""
        return list(self._paginate_results(self._client.describe_subnets, SubnetIds=subnet_ids))

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def get_subnet_avail_zone(self, subnet_id):
        """Return the availability zone associated to the given subnet."""
        subnets = self.describe_subnets([subnet_id])
        if subnets:
            return subnets[0].get("AvailabilityZone")
        raise AWSClientError(function_name="describe_subnets", message=f"Subnet {subnet_id} not found")

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def get_subnet_vpc(self, subnet_id):
        """Return a vpc associated to the given subnet."""
        subnets = self.describe_subnets([subnet_id])
        if subnets:
            return subnets[0].get("VpcId")
        raise AWSClientError(function_name="describe_subnets", message=f"Subnet {subnet_id} not found")

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def describe_image(self, ami_id):
        """Describe image by image id, return an object of ImageInfo."""
        result = self._client.describe_images(ImageIds=[ami_id])
        if result.get("Images"):
            return ImageInfo(result.get("Images")[0])
        raise AWSClientError(function_name="describe_images", message=f"Image {ami_id} not found")

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def describe_images(self, ami_ids, filters, owners):
        """Return a list of objects of ImageInfo."""
        result = self._client.describe_images(ImageIds=ami_ids, Filters=filters, Owners=owners)
        if result.get("Images"):
            return [ImageInfo(image) for image in result.get("Images")]
        raise ImageNotFoundError(function_name="describe_images")

    def image_exists(self, image_id: str):
        """Return a boolean describing whether or not an image with the given search criteria exists."""
        try:
            self.describe_image_by_id_tag(image_id)
            return True
        except ImageNotFoundError:
            return False

    def failed_image_exists(self, image_id: str):
        """Return a boolean describing whether or not a failed image with the given search criteria exists."""
        try:
            self.describe_image_by_imagebuilder_arn_tag(image_id)
            return True
        except ImageNotFoundError:
            return False

    @AWSExceptionHandler.handle_client_exception
    def describe_image_by_id_tag(self, image_id: str):
        """Return a dict of image info by searching image id tag as filter."""
        filters = [
            {"Name": "tag:" + PCLUSTER_IMAGE_ID_TAG, "Values": [image_id]},
            {"Name": "tag:" + PCLUSTER_IMAGE_BUILD_STATUS_TAG, "Values": ["available"]},
        ]
        owners = ["self"]
        return self.describe_images(ami_ids=[], filters=filters, owners=owners)[0]

    @AWSExceptionHandler.handle_client_exception
    def describe_image_by_imagebuilder_arn_tag(self, image_id: str):
        """Return a dict of image info by searching imagebuilder arn tag."""
        partition = get_partition()
        region = get_region()
        name = "{0}-{1}".format(IMAGEBUILDER_RESOURCE_NAME_PREFIX, image_id)[0:1024].lower()
        filters = [
            {
                "Name": "tag:" + IMAGEBUILDER_ARN_TAG,
                "Values": [f"arn:{partition}:imagebuilder:{region}:*:image/{name}*"],
            }
        ]
        owners = ["self"]
        return self.describe_images(ami_ids=[], filters=filters, owners=owners)[0]

    @AWSExceptionHandler.handle_client_exception
    def get_instance_ids_by_ami_id(self, image_id):
        """Get instance ids by ami id, when status is not terminated nor shutting-down."""
        instance_state = ("pending", "running", "stopping", "stopped")
        return [
            instance.get("InstanceId")
            for result in self._paginate_results(
                self._client.describe_instances,
                Filters=[
                    {"Name": "image-id", "Values": [image_id]},
                    {"Name": "instance-state-name", "Values": list(instance_state)},
                ],
            )
            for instance in result.get("Instances")
        ]

    @AWSExceptionHandler.handle_client_exception
    def get_image_shared_account_ids(self, image_id):
        """Get account ids that image is shared with."""
        return [
            permission.get("UserId") or permission.get("Group")
            for permission in self._client.describe_image_attribute(Attribute="launchPermission", ImageId=image_id).get(
                "LaunchPermissions"
            )
        ]

    def get_images(self):
        """Return existing pcluster images by pcluster image name tag."""
        try:
            filters = [
                {"Name": "tag-key", "Values": [PCLUSTER_IMAGE_ID_TAG]},
                {"Name": f"tag:{PCLUSTER_IMAGE_BUILD_STATUS_TAG}", "Values": ["available"]},
            ]
            owners = ["self"]
            return self.describe_images(ami_ids=[], filters=filters, owners=owners)
        except ImageNotFoundError:
            return []

    @AWSExceptionHandler.handle_client_exception
    def describe_key_pair(self, key_name):
        """Return the given key, if exists."""
        return self._client.describe_key_pairs(KeyNames=[key_name])

    @AWSExceptionHandler.handle_client_exception
    def describe_placement_group(self, group_name):
        """Return the given placement group, if exists."""
        return self._client.describe_placement_groups(GroupNames=[group_name])

    @AWSExceptionHandler.handle_client_exception
    def describe_vpc_attribute(self, vpc_id, attribute):
        """Return the attribute of the VPC."""
        return self._client.describe_vpc_attribute(VpcId=vpc_id, Attribute=attribute)

    def is_enable_dns_support(self, vpc_id):
        """Return the value of EnableDnsSupport of the VPC."""
        return (
            self.describe_vpc_attribute(vpc_id=vpc_id, attribute="enableDnsSupport")
            .get("EnableDnsSupport")
            .get("Value")
        )

    def is_enable_dns_hostnames(self, vpc_id):
        """Return the value of EnableDnsHostnames of the VPC."""
        return (
            self.describe_vpc_attribute(vpc_id=vpc_id, attribute="enableDnsHostnames")
            .get("EnableDnsHostnames")
            .get("Value")
        )

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def get_instance_type_info(self, instance_type):
        """Return the results of calling EC2's DescribeInstanceTypes API for the given instance type."""
        return InstanceTypeInfo(
            self.additional_instance_types_data.get(instance_type)
            or self._client.describe_instance_types(InstanceTypes=[instance_type]).get("InstanceTypes")[0]
        )

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def get_supported_architectures(self, instance_type):
        """Return a list of architectures supported for the given instance type."""
        instance_info = self.get_instance_type_info(instance_type)
        supported_architectures = instance_info.supported_architecture()

        # Some instance types support multiple architectures (x86_64 and i386). Filter unsupported ones.
        return list(set(supported_architectures) & set(SUPPORTED_ARCHITECTURES))

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def get_official_image_id(self, os, architecture, filters=None):
        """Return the id of the current official image, for the provided os-architecture combination."""
        owner = filters.owner if filters and filters.owner else "amazon"
        tags = filters.tags if filters and filters.tags else []

        filters = [{"Name": "name", "Values": ["{0}*".format(self._get_official_image_name_prefix(os, architecture))]}]
        filters.extend([{"Name": f"tag:{tag.key}", "Values": [tag.value]} for tag in tags])
        images = self._client.describe_images(Owners=[owner], Filters=filters).get("Images")
        if not images:
            raise AWSClientError(function_name="describe_images", message="Cannot find official ParallelCluster AMI")
        return max(images, key=lambda image: image["CreationDate"]).get("ImageId")

    def get_official_images(self, os=None, architecture=None):
        """Get the list of official images, optionally filtered by os and architecture."""
        try:
            owners = ["amazon"]
            name = f"{self._get_official_image_name_prefix(os, architecture)}*"
            filters = [{"Name": "name", "Values": [name]}]
            return self.describe_images(ami_ids=[], owners=owners, filters=filters)
        except ImageNotFoundError:
            return []

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def get_eip_allocation_id(self, eip):
        """Retrieve the allocation id of an Elastic IP."""
        return self._client.describe_addresses(PublicIps=[eip])["Addresses"][0]["AllocationId"]

    @staticmethod
    def extract_os_from_official_image_name(name):
        """Return the os from the os part in an official image name."""
        name_pattern = "aws-parallelcluster-[^-]+-(?P<OsPart>.+-hvm)-.*"
        matches = re.match(name_pattern, name)
        os_part = matches.groupdict().get("OsPart") if matches else None
        return IMAGE_NAME_PART_TO_OS_MAP.get(os_part, "linux")

    @staticmethod
    def _get_official_image_name_prefix(os=None, architecture=None):
        """Return the prefix of the current official image, for the provided os-architecture combination."""
        version = utils.get_installed_version()
        os = "*" if os is None else OS_TO_IMAGE_NAME_PART_MAP.get(os, "")
        architecture = architecture or "*"
        return f"aws-parallelcluster-{version}-{os}-{architecture}"

    @AWSExceptionHandler.handle_client_exception
    def terminate_instances(self, instance_ids):
        """Terminate list of EC2 instances."""
        return self._client.terminate_instances(InstanceIds=instance_ids)

    @AWSExceptionHandler.handle_client_exception
    def list_instance_ids(self, filters):
        """Retrieve a filtered list of instance ids."""
        return [
            instance.get("InstanceId")
            for result in self._paginate_results(self._client.describe_instances, Filters=filters)
            for instance in result.get("Instances")
        ]

    @AWSExceptionHandler.handle_client_exception
    def describe_instances(self, filters, next_token=None):
        """Retrieve a filtered list of instances."""
        describe_stacks_kwargs = {}
        if next_token:
            describe_stacks_kwargs["NextToken"] = next_token
        response = self._client.describe_instances(Filters=filters, **describe_stacks_kwargs)
        instances = []
        for reservation in response["Reservations"]:
            instances.extend(reservation["Instances"])
        return instances, response.get("NextToken")

    @AWSExceptionHandler.handle_client_exception
    @Cache.cached
    def get_supported_az_for_instance_type(self, instance_type: str):
        """
        Return a tuple of availability zones that have the instance_type.

        This function build above _get_supported_az_for_instance_types,
        but simplify the input to 1 instance type and result to a list

        :param instance_type: the instance type for which the supporting AZs.
        :return: a tuple of the supporting AZs
        """
        return self.get_supported_az_for_instance_types([instance_type])[instance_type]

    @AWSExceptionHandler.handle_client_exception
    def get_supported_az_for_instance_types(self, instance_types: List[str]):
        """
        Return a dict of instance types to list of availability zones that have each of the instance_types.

        :param instance_types: the list of instance types for which the supporting AZs.
        :return: a dicts. keys are strings of instance type, values are the tuples of the supporting AZs

        Example:
        If instance_types is:
        ["t2.micro", "t2.large"]
        Result can be:
        {
            "t2.micro": (us-east-1a, us-east-1b),
            "t2.large": (us-east-1a, us-east-1b)
        }
        """
        # first looks for info in cache, then using only one API call for all infos that is not inside the cache
        result = {}
        offerings = self.describe_instance_type_offerings(
            filters=[{"Name": "instance-type", "Values": instance_types}], location_type="availability-zone"
        )
        for instance_type in instance_types:
            result[instance_type] = tuple(
                offering["Location"] for offering in offerings if offering["InstanceType"] == instance_type
            )
        return result

    @AWSExceptionHandler.handle_client_exception
    def deregister_image(self, image_id):
        """Deregister ami."""
        self._client.deregister_image(ImageId=image_id)

    @AWSExceptionHandler.handle_client_exception
    def delete_snapshot(self, snapshot_id: str):
        """Delete snapshot."""
        self._client.delete_snapshot(SnapshotId=snapshot_id)

    @AWSExceptionHandler.handle_client_exception
    def get_ebs_snapshot_info(self, ebs_snapshot_id):
        """
        Return a dict described the information of an EBS snapshot returned by EC2's DescribeSnapshots API.

        Example of output:
        {
            "Description": "This is my snapshot",
            "Encrypted": False,
            "VolumeId": "vol-049df61146c4d7901",
            "State": "completed",
            "VolumeSize": 120,
            "StartTime": "2014-02-28T21:28:32.000Z",
            "Progress": "100%",
            "OwnerId": "012345678910",
            "SnapshotId": "snap-1234567890abcdef0",
        }
        """
        return self._client.describe_snapshots(SnapshotIds=[ebs_snapshot_id]).get("Snapshots")[0]

    @AWSExceptionHandler.handle_client_exception
    def describe_security_group(self, security_group_id):
        """Describe a single security group."""
        return self.describe_security_groups([security_group_id]).get("SecurityGroups")[0]

    @AWSExceptionHandler.handle_client_exception
    def describe_security_groups(self, security_group_ids):
        """Describe a single security group."""
        return self._client.describe_security_groups(GroupIds=security_group_ids)

    @AWSExceptionHandler.handle_client_exception
    def describe_network_interfaces(self, network_interface_ids):
        """Describe network interfaces."""
        return self._client.describe_network_interfaces(NetworkInterfaceIds=network_interface_ids).get(
            "NetworkInterfaces"
        )

    @AWSExceptionHandler.handle_client_exception
    def describe_volume(self, volume_id):
        """Describe a volume."""
        return self._client.describe_volumes(VolumeIds=[volume_id]).get("Volumes")[0]

    @AWSExceptionHandler.handle_client_exception
    def run_instances(self, **kwargs):
        """Describe network interfaces."""
        try:
            self._client.run_instances(**kwargs)
        except ClientError as e:
            if e.response.get("Error").get("Code") != "DryRunOperation":
                raise
