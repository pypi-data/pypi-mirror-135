from typing import AnyStr, Dict, Any

import requests

# from packaging.version import parse
from ..auth import OAuthClientParams
from ..constants import DEFAULT_SERVICE_REGISTRY
from ..exceptions import InvalidOAuthClientParamsError


class ServiceInfo:
    """
    The collection of configuration data collected from a Service Registry. It follows the GA4GH Service schema
    https://raw.githubusercontent.com/ga4gh-discovery/ga4gh-service-info/v1.0.0/service-info.yaml#/components/schemas/Service

    :param oauth_client: The OAuthClientParams specified by the service registry entry
    :param required_cli_version: The required version specified in the service registry
    """

    def __init__(
        self,
        id: AnyStr = None,
        name: AnyStr = None,
        type: AnyStr = None,
        organization: AnyStr = None,
        version: AnyStr = None,
        url: AnyStr = None,
        oauth_client: OAuthClientParams = None,
        required_cli_version: AnyStr = None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.organization = organization
        self.version = version

        self.url = url
        self.oauth_client = oauth_client
        self.required_cli_version = required_cli_version

    @classmethod
    def parse(cls, service_config: Dict[AnyStr, Any]):
        """
        Parse a Service Info type dict and return a ServiceInfo

        :param service_config: A dictionary retrieved from a GA4GH service registry
        :return: A Registry Entry with the
        """

        service_info = cls()

        service_info.id = service_config.get("id")
        service_info.name = service_config.get("name")
        service_info.type = service_config.get("type")
        service_info.organization = service_config.get("organization")
        service_info.version = service_config.get("version")

        cli_config = service_config.get("cli")
        required_version = None

        # if cli_config:
        #     service_info.required_cli_version = cli_config.get("requiredVersion")
        #     if required_version:
        #         # the required version is a minimum version of the cli for a specific type of service to work
        #         # the required version uses semantic versioning, so if 0.3 is required anything 0.3.x should be ok,
        #         # otherwise we should give an error.
        #         if parse(service_info.required_cli_version) > parse(__version__):
        #             raise ServiceRegistryException(
        #                 url=service_config.get("url"),
        #                 msg=f"The service requires "
        #                 f"dnastack-client-library >= {service_info.required_cli_version} ."
        #                 f"Please update dnastack-client-library",
        #             )

        auth_methods = service_config.get("authentication")
        if auth_methods:
            auth_methods = [
                method for method in auth_methods if method.get("type") == "oauth2"
            ]

            if len(auth_methods) > 0:
                auth_config = auth_methods[0]
                try:
                    service_info.oauth_client = OAuthClientParams(
                        client_id=auth_config.get("clientId"),
                        client_secret=auth_config.get("clientSecret"),
                        client_redirect_url=auth_config.get("redirectUrl"),
                        authorization_url=auth_config.get("authorizationUrl"),
                        token_url=auth_config.get("accessTokenUrl"),
                        device_code_url=auth_config.get("deviceCodeUrl"),
                        scope=auth_config.get("scope"),
                    )
                except InvalidOAuthClientParamsError:
                    service_info.oauth_client = None

        return service_info


class ServiceRegistry:
    def __init__(self, url: AnyStr = DEFAULT_SERVICE_REGISTRY):
        self.url = url

    def get(self, service_url: AnyStr) -> ServiceInfo:
        if not self.url:
            return ServiceInfo()

        reg_res = requests.get(self.url + "services")
        if reg_res.ok:
            services_in_registry = reg_res.json()
            for service_config in services_in_registry:
                if service_config["url"] + "/" == service_url:
                    return ServiceInfo.parse(service_config)
        return ServiceInfo()
