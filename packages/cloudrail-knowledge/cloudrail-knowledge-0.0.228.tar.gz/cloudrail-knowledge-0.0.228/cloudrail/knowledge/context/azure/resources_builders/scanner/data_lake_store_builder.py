from typing import List

from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity
from cloudrail.knowledge.context.azure.resources.storage.azure_data_lake_store import AzureDataLakeStore, DataLakeStoreTier
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import create_scanner_system_managed_identity
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.context.field_active import FieldActive


class DataLakeStoreBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'get-datalakestore.json'

    def do_build(self, attributes: dict) -> AzureDataLakeStore:
        properties: dict = attributes['properties']
        tier: DataLakeStoreTier = DataLakeStoreTier(properties['currentTier'])
        encryption_state: FieldActive = FieldActive(properties.get('encryptionState'))
        encryption_type: str = properties.get('encryptionConfig', {}).get('type')
        encryption_type = encryption_type or ('ServiceManaged' if encryption_state == FieldActive.ENABLED else '')
        firewall_allow_azure_ips: FieldActive = FieldActive(properties.get('firewallAllowAzureIps'))
        firewall_state: FieldActive = FieldActive(properties.get('firewallState'))
        identity = create_scanner_system_managed_identity(attributes)
        managed_identities: List[AzureManagedIdentity] = []
        if identity:
            managed_identities.append(identity)
        return AzureDataLakeStore(name=attributes['name'],
                                  tier=tier,
                                  encryption_state=encryption_state,
                                  encryption_type=encryption_type,
                                  managed_identities=managed_identities,
                                  firewall_allow_azure_ips=firewall_allow_azure_ips,
                                  firewall_state=firewall_state)
