from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class FunctionAppAccessibleOnlyViaHttpsRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_function_app_accessible_only_via_https'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for func_app in env_context.function_apps:
            if not func_app.https_only:
                issues.append(
                    Issue(
                        f'The Function App `{func_app.get_friendly_name()}` does not have HTTPS only enabled.',
                        func_app,
                        func_app))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.function_apps)
