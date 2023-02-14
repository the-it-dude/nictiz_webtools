from unittest import mock
from django.test import Client, TestCase

from app.factories import UserFactory, GroupFactory
from mapping.factories import MappingProjectFactory, MappingTaskFactory


class MappingTargetsViewSetTestCase(TestCase):
    def setUp(self):
        self.project = MappingProjectFactory()
        self.task = MappingTaskFactory(project_id=self.project)
        self.client = Client()
        self.user = UserFactory()

        mapping_edit_group = GroupFactory(name="mapping | edit mapping")
        self.user.groups.add(mapping_edit_group)
        self.client.force_login(user=self.user)

    def test_create_auth_required(self):
        data = {}
        result = self.client.post(data)
        self.assertEqual(result.status_code, 404)

    @mock.patch("mapping.views.mappings.UpdateECL1Task")
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
        result = self.client.post(path='/api/1.0/mappings', data=data)
        self.assertEqual(result.status_code, 405)
