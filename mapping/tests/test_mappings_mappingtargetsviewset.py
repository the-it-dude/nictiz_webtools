from unittest import mock
from django.test import Client, TestCase

from mapping.factories import MappingProjectFactory, MappingTaskFactory


class MappingTargetsViewSetTestCase(TestCase):
    def setUp(self):
        self.project = MappingProjectFactory()
        self.task = MappingTaskFactory(project_id=self.project)
        self.client = Client()

    @mock.patch("mapping.views.mappins.UpdateECL1Task")
    def test_create_for_project_type_4(self, update_ecl1_task_mock):
        data = {
            "targets": {
                "queries": [
                    {
                        "id": "extra",
                        "description": "2342",
                        "query": "9847007 | Structure of hilum of adrenal gland (body structure) |",
                        "finished": False,
                        "error": False,
                        "failed": False,
                        "correlation": "447561005",
                    }
                ],
                "queries_unfinished": False,
                "duplicates_in_ecl": [],
                "errors": [],
                "mappings_unfinished": False,
            },
            "task": self.task.id,
        }
        result = client.post(data)
        self.assertEqual(result.status_code, 200)
