from rest_framework.test import APITestCase

from app.factories import UserFactory, GroupFactory

from mapping.enums import MappingGroups
from mapping.factories import MappingProjectFactory, MappingTaskFactory
from mapping.models import MappingEventLog


class MappingProjectUsersViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.project_access_group = GroupFactory(name=MappingGroups.project_access)
        self.user.groups.add(self.project_access_group)
        self.client.force_login(self.user)
        self.project = MappingProjectFactory()
        self.project.access.add(self.user)
        self.task = MappingTaskFactory(project_id=self.project)

        self.url = "/mapping/api/1.0/users/"
        self.project_url = f"{self.url}{self.project.pk}/"

    def test_access_success(self):
        result = self.client.get(self.project_url)
        self.assertEqual(result.status_code, 200)

    def test_access_no_group_access(self):
        self.user.groups.clear()
        result = self.client.get(self.project_url)
        self.assertEqual(result.status_code, 403)

    def test_access_no_project_access(self):
        self.project.access.clear()

        result = self.client.get(self.project_url)
        self.assertEqual(result.status_code, 403)

    def test_users_list(self):
        user_has_access_to_task = UserFactory()
        user_has_access_to_task.groups.add(self.project_access_group)
        self.task.user = user_has_access_to_task
        user_has_no_access_to_tasks = UserFactory()
        user_has_access_to_other_project = UserFactory()
        user_has_access_to_other_project.groups.add(self.project_access_group)
        MappingTaskFactory(user=user_has_access_to_other_project)

        result = self.client.get(self.project_url)

        users_in_result = [user["value"] for user in result.data]
        self.assertIn(user_has_access_to_task.pk, users_in_result)
        self.assertIn(self.user.pk, users_in_result)
        self.assertNotIn(user_has_no_access_to_tasks.pk, users_in_result)
        self.assertNotIn(user_has_access_to_other_project.pk, users_in_result)

    def test_output(self):
        result = self.client.get(self.project_url)

        self.assertEqual(result.data, [
            {'value': 1, 'text': self.user.username, 'name': " "}
        ])

    def test_create_no_group_access(self):
        user = UserFactory()

        self.client.force_login(user)
        result = self.client.post(self.url, {"task": self.task.pk}, format="json")

        self.assertEqual(result.status_code, 403)

    def test_create_no_project_access(self):
        user = UserFactory()
        user.groups.add(self.project_access_group)

        self.client.force_login(user)
        result = self.client.post(self.url, {"task": self.task.pk}, format="json")

        self.assertEqual(result.status_code, 401)

    def test_create_success(self):
        user = UserFactory()
        result = self.client.post(self.url, {"task": self.task.pk, "user": user.pk}, format="json")

        self.assertEqual(result.status_code, 200)

        self.task.refresh_from_db()
        self.assertEqual(self.task.user, user)

        event_log = MappingEventLog.objects.last()
        self.assertEqual(event_log.task, self.task)
        self.assertEqual(event_log.action, "user_change")
        self.assertEqual(event_log.action_user, self.user)
        self.assertEqual(event_log.action_description, "Gebruiker:")
        self.assertEqual(event_log.old_data, "")
        self.assertEqual(event_log.new_data, "[]")
        self.assertEqual(event_log.old, str(self.user))
        self.assertEqual(event_log.new, str(user))
        self.assertEqual(event_log.user_source, self.user)
        self.assertEqual(event_log.user_target, user)
