import requests
import os
from django.core.management.base import BaseCommand

from mapping.tasks.tasks import import_snomed_snowstorm


class Command(BaseCommand):
    help = "Create base groups in fresh DB"

    def fetch_headers(self, username, password):
        data = {
            "grant_type": "password",
            "client_id": "cli_client",
            "username": username,
            "password": password,
        }
        token = requests.post(
            "https://terminologieserver.nl/auth/realms/nictiz/protocol/openid-connect/token",
            data=data,
        ).json()
        print(repr(token))
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token['access_token']}",
        }

    def handle(self, *args, **options):
        # result = import_snomed_snowstorm.apply()
        headers = self.fetch_headers(username=os.environ.get("TERMINOLOGIE_USERNAME"), password=os.environ.get("TERMINOLOGIE_PASSWORD"))
        print(repr(headers))

        data = requests.get(
            "https://terminologieserver.nl/fhir/ValueSet/$expand?url=http://snomed.info/sct?fhir_vs=refset",
            # "https://terminologieserver.nl/fhir/CodeSystem/$lookup?system=http://snomed.info/sct&code=99999003&property=child",
            headers=headers,
        )
        print("*" * 80)
        print(repr(data))
        breakpoint()
