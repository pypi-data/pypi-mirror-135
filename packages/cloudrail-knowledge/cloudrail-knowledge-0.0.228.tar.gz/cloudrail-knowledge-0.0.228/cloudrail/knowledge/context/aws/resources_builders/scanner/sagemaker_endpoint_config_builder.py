from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_sagemaker_endpoint_config


class SageMakerEndpointConfigBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'sagemaker-describe-endpoint-config/*'

    def get_section_name(self) -> str:
        pass

    def do_build(self, attributes: dict):
        return build_sagemaker_endpoint_config(attributes)
