import enum
import typing
import requests
import urllib.parse

class TerminologieRequestError(Exception):
    pass


class TerminiologieClient:
    """
    Terminologie Client.

    Set of tools used to fetch data from terminologie.nl(or otherwise) server.

    """

    class OutputFormat(enum.Enum):
        default = "Default"
        snowstorm = "Snowstorm compatible"

    uri: typing.Optional[str] = None  # Contains base URI for terminologie server
    session: typing.Optional[requests.Session] = None  # Contains request session with auth headers

    def __init__(self, uri: str) -> None:
        """Init class by storing base URI and starting requests.Session.

        Args:
            uri (str): Base URI for terminologie server. Usually corresponds to settings.TERMINOLOGIE_URI
            output_format (OutputFormat): Output format to use.
        """
        self.uri = uri
        self.session = requests.Session()

    def login(self, username: str, password: str) -> None:
        """
        Fetch Login details using login and password.
        AUTH Details will be stored to self.session.headers.

        Args:
            username (str): Username
            password (str): Password

        Raises:
            TerminologieRequestError in case login is unsuccessul or another error occured.
        """
        try:
            response = requests.post(
                url=f"{self.uri}/auth/realms/nictiz/protocol/openid-connect/token",
                data={
                    "grant_type": "password",
                    "client_id": "cli_client",
                    "username": username,
                    "password": password
                }
            )
        except requests.RequestException as e:
            raise TerminologieRequestError from e
        else:
            if "access_token" not in response.json():
                raise TerminologieRequestError(f"Incorrect response from server: {response.json()}")
        
            token = response.json()['access_token']
            self.session.headers = {
                "Content-Type" : "application/json",
                "Authorization": f"Bearer {token}"
            }

    def expand_snomed_ecl_valueset(self, ecl_query: str) -> dict:
        """
        Expand Snomed ECL Value Set.
        
        Args:
            ecl_query (str): ECL query string.
            
        Returns:
            dictionary containing response data.
        """
        url = f"{self.uri}/fhir/ValueSet/$expand?url=http://snomed.info/sct?fhir_vs=ecl/{urllib.parse.quote_plus(ecl_query)}"
        
        response = self.session.get(url=url)

        return response.json()

    def lookup_code(self, system: str, code: str) -> typing.Union[None, dict]:
        """Retrieves the properties for a code within a CodeSystem.
        
        Args:
            system (str): Code System to Use
            code (str): Code ID.

        Returns:
            either dictionary with details or None if code is not found.
        """
        url = f"{self.uri}/fhir/CodeSystem/$lookup?system={system}&code={code}"

        response = self.session.get(url=url)

        return response.json()