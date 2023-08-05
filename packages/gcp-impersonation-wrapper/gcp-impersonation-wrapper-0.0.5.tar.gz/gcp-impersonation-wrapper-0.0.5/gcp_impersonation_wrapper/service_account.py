from google.auth.credentials import Credentials
from googleapiclient.discovery import build
from gcp_impersonation_wrapper.impersonated_service_account import ImpersonatedServiceAccount


class ServiceAccount:
    def __init__(self, project_id, impersonator_credentials: Credentials) -> None:
        self.project_id = project_id
        self.impersonator_credentials = impersonator_credentials
        self.service = build(
            'iam', 'v1', credentials=self.impersonator_credentials)
        self.service_account_email = self.impersonator_credentials._service_account_email

    def impersonate(self, service_account_email: str, target_scopes: list, service: str, version: str) -> None:
        return ImpersonatedServiceAccount(self.impersonator_credentials, service_account_email, target_scopes, service, version)

    def list_all_impersonatable_service_account_emails(self) -> list:
        impersonatable_service_accounts = self.list_all_impersonatable_service_account_objects()
        emails = self.get_emails(impersonatable_service_accounts)
        emails = list(emails)
        return emails

    def list_all_impersonatable_service_account_objects(self) -> list:
        self.service_accounts = []

        more_pages = True
        next_page_token = None
        while more_pages:
            request_kwargs = {
                "name": f"projects/{self.project_id}",
            }

            if next_page_token:
                request_kwargs["pageToken"] = next_page_token

            response = self.service.projects().serviceAccounts().list(**
                                                                      request_kwargs).execute()

            self.service_accounts = [
                *self.service_accounts, *response["accounts"]]

            next_page_token = response.get('nextPageToken', None)
            more_pages = bool(next_page_token)

        impersonatable_service_accounts = self.filter_impersonatable_service_accounts(
            self.service_accounts)
        impersonatable_service_accounts = list(impersonatable_service_accounts)
        return impersonatable_service_accounts

    def is_impersonatable(self, service_account_email: str) -> bool:
        policies = self.service.projects().serviceAccounts().getIamPolicy(
            resource=f"projects/{self.project_id}/serviceAccounts/{service_account_email}"
        ).execute()
        if "bindings" not in policies:
            return False
        for binding in policies["bindings"]:
            if "role" in binding and binding["role"] == "roles/iam.serviceAccountTokenCreator" and f"serviceAccount:{self.service_account_email}" in binding["members"]:
                return True
        return False

    def filter_impersonatable_service_accounts(self, service_accounts: str) -> list:
        for service_account in service_accounts:
            if self.is_impersonatable(service_account["email"]):
                yield service_account

    def get_emails(self, service_accounts):
        for service_account in service_accounts:
            yield service_account["email"]
