from typing import List
from cloudrail.knowledge.context.environment_context.common_component_builder import extract_name_from_gcp_link
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, IterFunctionData, FunctionData
from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator
from cloudrail.knowledge.context.gcp.pseudo_builder import PseudoBuilder
from cloudrail.knowledge.context.gcp.resources.binary_authorization.gcp_binary_authorization_policy import GcpClusterContainerBinaryAuthorizationPolicy
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_forwarding_rule import GcpComputeForwardingRule
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_pool import GcpComputeTargetPool
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_global_forwarding_rule import GcpComputeGlobalForwardingRule
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_ssl_policy import GcpComputeSslPolicy
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_subnetwork import GcpComputeSubNetwork
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_proxy import GcpComputeTargetProxy
from cloudrail.knowledge.context.gcp.resources.iam.iam_access_policy import GcpIamPolicyType
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket import GcpStorageBucket
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket_iam_policy import GcpStorageBucketIamPolicy
from cloudrail.knowledge.context.gcp.gcp_iam_actions import IamActions


class GcpRelationsAssigner(DependencyInvocation):

    def __init__(self, ctx: GcpEnvironmentContext = None):
        self.pseudo_builder = PseudoBuilder(ctx)
        self.pseudo_builder.create_default_firewalls()

        function_pool = [
            ### VPC network
            FunctionData(self._assign_implied_firewalls_to_vpcs, (ctx.compute_networks,)),
            IterFunctionData(self._assign_firewalls_to_vpcs, ctx.compute_networks, (ctx.compute_firewalls,), [self._assign_implied_firewalls_to_vpcs]),
            ### Compute Instance
            IterFunctionData(self._assign_networking_info_to_network_interfaces, ctx.compute_instances, (ctx.compute_networks,), [self._assign_firewalls_to_vpcs]),
            IterFunctionData(self._assign_forward_rule_to_instance, ctx.compute_instances, (ctx.compute_forwarding_rules,), [self._assign_targets_to_forward_rule]),
            ### Compute Forwarding Rule
            IterFunctionData(self._assign_targets_to_forward_rule, ctx.compute_forwarding_rules, (ctx.compute_target_pools,)),
            ### SSL policies
            IterFunctionData(self._assign_ssl_policy, ctx.compute_target_ssl_proxy, (ctx.compute_ssl_policy,)),
            IterFunctionData(self._assign_ssl_policy, ctx.compute_target_https_proxy, (ctx.compute_ssl_policy,)),
            IterFunctionData(self._assign_target_proxy, ctx.compute_global_forwarding_rule, (ctx.get_all_targets_proxy(),)),
            IterFunctionData(self._assign_subnetwork, ctx.compute_networks, (ctx.compute_subnetworks,)),
            ### Storage Bucket
            IterFunctionData(self._assign_iam_policies_to_bucket, ctx.storage_buckets, (ctx.storage_bucket_iam_policies,)),
            ### Container cluster
            IterFunctionData(self._assign_binary_policy_to_cluster, ctx.container_clusters, (ctx.binary_authorization_policies,)),
        ]

        super().__init__(function_pool, context=ctx)

    ## According to GCP docs, every VPC has 2 implied rules for Ipv4 and IPv6 if enabled:
    ## https://cloud.google.com/vpc/docs/firewalls#default_firewall_rules
    def _assign_implied_firewalls_to_vpcs(self, vpcs: AliasesDict[GcpComputeNetwork]):
        implied_firewalls = self.pseudo_builder.get_implied_firewalls()
        for vpc in vpcs:
            for firewall in implied_firewalls:
                firewall.network = vpc.self_link
            vpc.firewalls.extend(implied_firewalls)

    @staticmethod
    def _assign_firewalls_to_vpcs(vpc: GcpComputeNetwork, firewalls: List[GcpComputeFirewall]):
        def get_firewalls_vpc():
            firewalls_list = [firewall for firewall in firewalls if extract_name_from_gcp_link(firewall.network) == vpc.name]
            return firewalls_list

        vpc.firewalls.extend(ResourceInvalidator.get_by_logic(get_firewalls_vpc, False))

    @staticmethod
    def _assign_networking_info_to_network_interfaces(instance: GcpComputeInstance, vpcs: AliasesDict[GcpComputeNetwork]):
        def get_instance_vpcs():
            instance_vpcs = [vpc for vpc in vpcs if any(extract_name_from_gcp_link(interface.network) == vpc.name for interface in instance.network_interfaces)]
            return instance_vpcs
        if instance_vpcs := ResourceInvalidator.get_by_logic(get_instance_vpcs, True, instance, 'Unable to find interface related VPC network'):
            for nic in instance.network_interfaces:
                vpc_network = next((vpc for vpc in instance_vpcs if extract_name_from_gcp_link(nic.network) == vpc.name), None)
                nic.vpc_network = vpc_network
                nic.firewalls = vpc_network.firewalls

    @staticmethod
    def _assign_targets_to_forward_rule(forward_rule: GcpComputeForwardingRule, target_pools: AliasesDict[GcpComputeTargetPool]):
        forward_rule.target_pool = ResourceInvalidator.get_by_id(target_pools, forward_rule.target, True, forward_rule)

    @staticmethod
    def _assign_forward_rule_to_instance(compute_instance: GcpComputeInstance, forwarding_rules: List[GcpComputeForwardingRule]):
        def get_forwarding_rules():
            forwarding_rules_list = [rule for rule in forwarding_rules if rule.target_pool and compute_instance.self_link in rule.target_pool.instances]
            return forwarding_rules_list

        compute_instance.forwarding_rules = (ResourceInvalidator.get_by_logic(get_forwarding_rules, False))

    @staticmethod
    def _assign_ssl_policy(target_proxy: GcpComputeTargetProxy, ssl_policies: AliasesDict[GcpComputeSslPolicy]):
        def get_ssl_policy():
            ssl_policy = ResourceInvalidator.get_by_id(ssl_policies, target_proxy.ssl_policy_identifier, False)
            if not ssl_policy:
                ssl_policy = next((ssl_policy for ssl_policy in ssl_policies if
                                   target_proxy.project_id == ssl_policy.project_id and
                                   target_proxy.ssl_policy_identifier == ssl_policy.name), None)
            return ssl_policy

        # only is_encrypted resources have ssl_policy
        if target_proxy.is_encrypted and not target_proxy.ssl_policy:
            target_proxy.ssl_policy = ResourceInvalidator.get_by_logic(get_ssl_policy, False)

    @staticmethod
    def _assign_target_proxy(global_forwarding_rule: GcpComputeGlobalForwardingRule, targets: AliasesDict[GcpComputeTargetProxy]):
        def get_target():
            target = ResourceInvalidator.get_by_id(targets, global_forwarding_rule.target_identifier, False)
            if not target:
                target = next((target for target in targets if
                               global_forwarding_rule.project_id == target.project_id and
                               global_forwarding_rule.target_identifier == target.name), None)
            return target

        global_forwarding_rule.target = ResourceInvalidator.get_by_logic(get_target, True, global_forwarding_rule, "Could not associate target proxy")

    @staticmethod
    def _assign_subnetwork(network: GcpComputeNetwork, subnetworks: AliasesDict[GcpComputeSubNetwork]):
        def get_subnetworks():
            subnetworks_list: List[GcpComputeSubNetwork] = []
            for subnetwork in subnetworks:
                if subnetwork.network_identifier in [network.self_link, network.name, network.network_id]:
                    subnetworks_list.append(subnetwork)
            return subnetworks_list

        network.subnetworks = ResourceInvalidator.get_by_logic(get_subnetworks, False)

    def _assign_iam_policies_to_bucket(self, storage_bucket: GcpStorageBucket, bucket_iam_policies: List[GcpStorageBucketIamPolicy]):
        if any(policy.policy_type != GcpIamPolicyType.AUTHORITATIVE for policy in bucket_iam_policies
               if policy.bucket_name == storage_bucket.name and not policy.is_default) or len(bucket_iam_policies) == 0:
            default_policy = self.pseudo_builder.create_default_storage_bucket_iam_policy(storage_bucket.project_id)
            bucket_iam_policies.append(default_policy)
            bucket_iam_policies = IamActions.merge_iam_policies(bucket_iam_policies)
        def get_iam_policies():
            iam_policy = next((policy for policy in bucket_iam_policies
                               if policy.bucket_name == storage_bucket.name), None)
            return iam_policy

        storage_bucket.iam_policy = ResourceInvalidator.get_by_logic(get_iam_policies, False)

    def _assign_binary_policy_to_cluster(self, container_cluster: GcpContainerCluster, binary_auth_policies: List[GcpClusterContainerBinaryAuthorizationPolicy]):
        def get_binary_policies():
            default_policy_from_context = next((policy.default_admission_rule for policy in binary_auth_policies
                                                if policy.project_id == container_cluster.project_id), None)
            cluster_policy_from_context = next((rule for policy in binary_auth_policies for rule in policy.cluster_admission_rules
                                                if policy.project_id == container_cluster.project_id
                                                and rule.cluster_id == f'{container_cluster.location}.{container_cluster.name}'), None)
            if default_policy_from_context:
                binary_policies = [default_policy_from_context]
                if cluster_policy_from_context:
                    binary_policies.append(cluster_policy_from_context)
            else:
                binary_policies = [self.pseudo_builder.create_default_binary_auth_policy(container_cluster.project_id).default_admission_rule]
            return binary_policies

        container_cluster.binary_auth_policies = ResourceInvalidator.get_by_logic(get_binary_policies, False)
