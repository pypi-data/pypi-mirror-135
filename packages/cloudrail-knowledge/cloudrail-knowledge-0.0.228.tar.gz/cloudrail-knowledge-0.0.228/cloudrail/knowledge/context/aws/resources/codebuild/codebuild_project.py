from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.tags_utils import filter_tags


class CodeBuildProject(NetworkEntity):
    """
        Attributes:
            project_name: The name of the project.
            encryption_key: The KMS ID of the encryption key, if used, or None otherwise.
            arn: The ARN of the project.
            vpc_config: The network configuration of the project, if configured.
    """
    def __init__(self,
                 project_name: str,
                 encryption_key: str,
                 arn: str,
                 account: str,
                 region: str,
                 vpc_config: NetworkConfiguration):
        super().__init__(project_name, account, region, AwsServiceName.AWS_CODEBUILD_PROJECT)
        self.project_name: str = project_name
        self.encryption_key: str = encryption_key
        self.arn: str = arn
        self.kms_data: KmsKey = None
        self.vpc_config: NetworkConfiguration = vpc_config

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.project_name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CodeBuild'
        else:
            return 'CodeBuilds'

    def get_all_network_configurations(self) -> Optional[List[NetworkConfiguration]]:
        if self.vpc_config:
            return [NetworkConfiguration(self.vpc_config.assign_public_ip,
                                         self.vpc_config.security_groups_ids,
                                         self.vpc_config.subnet_list_ids)]
        else:
            return []

    def get_cloud_resource_url(self) -> Optional[str]:
        if self.account:
            return '{0}codesuite/codebuild/{1}/projects/{2}/'\
                .format(self.AWS_CONSOLE_URL, self.account, self.project_name)
        else:
            return None

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'project_name': self.project_name,
                'encryption_key': self.encryption_key,
                'assign_public_ip': self.vpc_config and self.vpc_config.assign_public_ip,
                'security_groups_ids': self.vpc_config and self.vpc_config.security_groups_ids,
                'subnet_list_ids': self.vpc_config and self.vpc_config.subnet_list_ids}
