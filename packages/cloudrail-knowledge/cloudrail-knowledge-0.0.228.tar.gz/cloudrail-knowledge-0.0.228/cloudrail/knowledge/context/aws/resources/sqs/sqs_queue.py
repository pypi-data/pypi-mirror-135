import urllib
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_policied_resource import PoliciedResource
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.tags_utils import filter_tags


class SqsQueue(PoliciedResource):
    """
        Attributes:
            arn: The ARN of the SQS Queue.
            queue_name: The name of the queue.
            encrypted_at_rest: True if the queue is encrypted at rest.
            kms_key: The ID of the KMS Key used to encrypt the queue, if any is used.
            kms_data: A reference to KmsKey based on the kms_key provided.
            queue_url: The URL of the queue.
    """
    def __init__(self,
                 arn: str,
                 queue_name: str,
                 encrypted_at_rest: bool,
                 account: str,
                 region: str,
                 queue_url: str):
        super().__init__(account, region, AwsServiceName.AWS_SQS_QUEUE)
        self.arn: str = arn
        self.queue_name: str = queue_name
        self.encrypted_at_rest: bool = encrypted_at_rest
        self.kms_key: str = None
        self.kms_data: Optional[KmsKey] = None
        self.queue_url: str = queue_url

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_arn(self) -> str:
        return self.arn

    def get_name(self) -> str:
        return self.queue_name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'SQS queue'
        else:
            return 'SQS queues'

    def get_cloud_resource_url(self) -> str:
        return '{0}sqs/v2/home?region={1}#/queues/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, urllib.parse.quote_plus(self.queue_url))

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'queue_name': self.queue_name,
                'encrypted_at_rest': self.encrypted_at_rest,
                'resource_based_policy': self.resource_based_policy and self.resource_based_policy.to_drift_detection_object()}
