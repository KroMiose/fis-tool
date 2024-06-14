from typing import Optional
from google.api_core import grpc_helpers
from google.ai.generativelanguage_v1beta.services.generative_service.transports.grpc import (
    ga_credentials,
    Sequence,
    grpc,
    GenerativeServiceGrpcTransport,
)


def patch_gemini_proxy(proxy_url):

    @classmethod
    def create_channel(
        cls,
        host: str = "generativelanguage.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        nonlocal proxy_url

        if "options" in kwargs:
            kwargs["options"] = [
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
                ("grpc.http_proxy", proxy_url),
            ]

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    GenerativeServiceGrpcTransport.create_channel = create_channel  # type: ignore
