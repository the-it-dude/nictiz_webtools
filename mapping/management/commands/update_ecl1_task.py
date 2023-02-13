from django.core.management.base import BaseCommand


import pprint

from mapping.tasks.tasks import UpdateECL1Task
from terminologieserver.client import TerminiologieClient

class Command(BaseCommand):
    help = 'Create base groups in fresh DB'

    def handle(self, *args, **options):
        data = UpdateECL1Task(
            record_id=3,
            query="9847007 | Structure of hilum of adrenal gland (body structure) |"
        )
        print("*" * 80)
        print(repr(data))

        client = TerminiologieClient(
            uri="https://terminologieserver.nl",
        )
        client.login(username="", password="")

        expanded = client.expand_snomed_ecl_valueset(
            ecl_query="9847007 | Structure of hilum of adrenal gland (body structure) |"
        )

        pprint.pprint(expanded)
        for code in expanded['expansion'].get("contains", []):
            pprint.pprint(client.lookup_code(code=code["code"], system=code["system"]))

        breakpoint()
