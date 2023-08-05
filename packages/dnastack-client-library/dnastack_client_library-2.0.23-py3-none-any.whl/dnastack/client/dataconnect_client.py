from pprint import pformat
from pydantic import BaseModel, ValidationError
from requests import Session
from typing import Optional, Any, Dict, List, Iterator
from urllib.parse import urljoin

from dnastack.auth import OAuthTokenAuth
from dnastack.client.base_client import BaseServiceClient
from dnastack.client.base_exceptions import UnauthenticatedApiAccessError, UnauthorizedApiAccessError, ApiError, \
    MissingResourceError, ServerApiError
from dnastack.client.result_iterator import ResultLoader, ResultIterator
from dnastack.constants import DEFAULT_SERVICE_REGISTRY


class InactiveQuerySessionError(StopIteration):
    """ Raised when the query loader has ended its session """


class Table(BaseModel):
    name: str
    description: Optional[str]
    data_model: Dict[str, Any]
    errors: Optional[List[Dict[str, Any]]]


class Pagination(BaseModel):
    next_page_url: Optional[str]


class TableDataResponse(BaseModel):
    data: List[Dict[str, Any]]
    data_model: Optional[Dict[str, Any]] = list()
    pagination: Optional[Pagination]
    errors: Optional[List[Dict[str, Any]]]


class ListTablesResponse(BaseModel):
    tables: Optional[List[Table]]
    pagination: Optional[Pagination]
    errors: Optional[List[Dict[str, Any]]]


class TableListLoader(ResultLoader):
    def __init__(self, session: Session, initial_url: str):
        self.__session = session
        self.__initial_url = initial_url
        self.__current_url: Optional[str] = None
        self.__active = True

    def load(self) -> List[Table]:
        if not self.__active:
            raise InactiveQuerySessionError(self.__initial_url)

        session = self.__session
        response = session.get(self.__current_url or self.__initial_url)
        status_code = response.status_code
        response_body = response.json()

        if status_code == 401:
            raise UnauthenticatedApiAccessError(self.__generate_api_error_feedback())
        elif status_code == 403:
            raise UnauthorizedApiAccessError(self.__generate_api_error_feedback())
        elif status_code >= 400:  # Catch all errors
            raise ApiError(self.__initial_url, status_code, response_body)

        try:
            api_response = ListTablesResponse(**response_body)
        except ValidationError:
            raise ServerApiError(f'Invalid Response Body: {response_body}')

        self.logger.debug(f'Response:\n{pformat(response_body, indent=2)}')

        if api_response.errors:
            extracted_errors = [
                f'{e["title"]} ({e["source"]})'
                for e in api_response.errors
            ]

            self.__active = False

            if self.__current_url:
                # The iterator encounters an unexpected error while iterating the result. Return an empty list.
                self.logger.warning(
                    f'While listing tables from {self.__initial_url}, the server failed to respond to the request to '
                    f'{self.__current_url} due to errors and the client will return the data received so far.'
                )
            else:
                # The iterator encounters an error on the first request.
                self.logger.error(f'The server responds an error while making a request to {self.__initial_url}.')

            self.logger.warning(f'The errors are: {extracted_errors}')
            return []

        ########################################################################################################################################################
        # FIXME The failed build is due that listing table from publisher_data fails. The code should throw an exception if all requests during listing fails. #
        ########################################################################################################################################################

        self.__current_url = api_response.pagination.next_page_url if api_response.pagination else None
        if not self.__current_url:
            self.__active = False

        return api_response.tables

    def has_more(self) -> bool:
        return self.__active or self.__current_url

    def close(self):
        self.__active = False

    def __generate_api_error_feedback(self) -> str:
        if self.__current_url:
            return f'Failed to load a follow-up page of the table list from {self.__current_url}'
        else:
            return f'Failed to load the first page of the table list from {self.__initial_url}'


class QueryLoader(ResultLoader):
    def __init__(self, session: Session, initial_url: str, query: Optional[str] = None):
        self.__session = session
        self.__initial_url = initial_url
        self.__current_url: Optional[str] = None
        self.__query = query
        self.__active = True

    def load(self) -> List[Dict[str, Any]]:
        if not self.__active:
            raise InactiveQuerySessionError(self.__initial_url)

        session = self.__session

        if not self.__current_url:
            # Load the initial page.
            if self.__query:
                # Send a search request
                response = session.post(urljoin(self.__initial_url, r'search'), json=dict(query=self.__query))
            else:
                # Fetch the table data
                response = session.get(self.__initial_url)
        else:
            # Load a follow-up page.
            response = session.get(self.__current_url)

        status_code = response.status_code
        response_body = response.json()

        self.logger.debug(f'Response:\n{pformat(response_body, indent=2)}')

        if status_code == 401:
            raise UnauthenticatedApiAccessError(self.__generate_api_error_feedback())
        elif status_code == 403:
            raise UnauthorizedApiAccessError(self.__generate_api_error_feedback())
        elif status_code == 404:
            raise MissingResourceError(self.__generate_api_error_feedback())
        elif status_code >= 400:  # Catch all errors
            raise ApiError(self.__initial_url, status_code, response_body)

        api_response = TableDataResponse(**response_body)

        if api_response.errors:
            extracted_errors = [
                f'{e["title"]} ({e["source"]})'
                for e in api_response.errors
            ]

            self.__active = False

            if self.__current_url:
                # The iterator encounters an unexpected error while iterating the result. Return an empty list.
                self.logger.warning(
                    f'While listing tables from {self.__initial_url}, the server failed to respond to the request to '
                    f'{self.__current_url} due to errors and the client will return the data received so far.'
                )
            else:
                # The iterator encounters an error on the first request.
                self.logger.error(f'The server responds an error while making a request to {self.__initial_url}.')

            self.logger.warning(f'The errors are: {extracted_errors}')
            return []

        self.__current_url = api_response.pagination.next_page_url if api_response.pagination else None
        if not self.__current_url:
            self.__active = False

        return api_response.data

    def has_more(self) -> bool:
        return self.__active or self.__current_url

    def close(self):
        self.__active = False

    def __generate_api_error_feedback(self) -> str:
        if self.__current_url:
            if self.__query:
                return f'Failed to load a follow-up page of the result from this query: {self.__query}'
            else:
                return f'Failed to load a follow-up page of {self.__current_url}'
        else:
            if self.__query:
                return f'Failed to load the first page of the result from this query: {self.__query}'
            else:
                return f'Failed to load the first page of {self.__initial_url}'


class DataConnectClientV2(BaseServiceClient):
    """
    A Client for the GA4GH Data Connect standard
    """

    def __init__(self, url: str, auth: Optional[OAuthTokenAuth] = None, registry_url: str = DEFAULT_SERVICE_REGISTRY):
        if not url.endswith('/'):
            url = url + r'/'

        super().__init__(url=url, auth=auth, registry_url=registry_url)

    def query(self, q: str) -> Iterator:
        """
        Run an SQL query against a Data Connect instance

        :param q: The SQL query to be executed
        :return: The formatted result of the SQL query
        """

        return ResultIterator(QueryLoader(self.client, self.url, q))

    def list_tables(self) -> Iterator:
        """
        Return the list of tables available at the Data Connect instance

        :return: A dict of available tables' metadata.
        """
        return ResultIterator(TableListLoader(self.client, urljoin(self.url, r'tables')))

    def get_table(self, table_name: str) -> Table:
        """
        Get table metadata for a specific table

        :param table_name: The name of the table
        :return: A dict of table metadata.
        """
        response = self.client.get(urljoin(self.url, fr'table/{table_name}/info'))
        status_code = response.status_code
        response_body = response.json()

        if status_code == 401:
            raise UnauthenticatedApiAccessError('Authentication required')
        elif status_code == 403:
            raise UnauthorizedApiAccessError('Insufficient privilege')
        elif status_code == 404:
            raise MissingResourceError(table_name)
        elif status_code >= 400:  # Catch all errors
            raise ApiError(self.url, status_code, response_body)

        return Table(**response_body)
