from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EsEncryptAtRestRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_es_domain_encrypt_at_rest_creating'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for es_domain in env_context.elastic_search_domains:
            if es_domain.is_new_resource():
                if self._supported_es_domain_for_encryption(es_domain) and not es_domain.encrypt_at_rest_state:
                    issues.append(
                        Issue(
                            f"~{es_domain.get_type()}~. {es_domain.get_type()} `{es_domain.get_friendly_name()}`. "
                            f"is not set to use encrypt at rest", es_domain, es_domain))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.elastic_search_domains)

    @staticmethod
    def _supported_es_domain_for_encryption(es_domain: ElasticSearchDomain) -> bool:
        return (es_domain.es_domain_cluster_instance_type.split('.')[0] not in ('m3', 'r3', 't2')
                and es_domain.es_domain_version not in ('1.5', '2.3'))
