from google.auth import impersonated_credentials as gcp_impersonated_credentials
from googleapiclient.discovery import build


class ImpersonatedServiceAccount:
    def __init__(self, impersonator_credentials, the_one_you_want_to_impersonate, target_scopes, service_name, version) -> None:
        self.impersonated_credentials = gcp_impersonated_credentials.Credentials(
            source_credentials=impersonator_credentials,
            target_principal=the_one_you_want_to_impersonate,
            target_scopes=target_scopes,
            lifetime=500
        )

        self.service = build(service_name, version,
                             credentials=self.impersonated_credentials)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass
