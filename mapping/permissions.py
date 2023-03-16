from django.contrib.auth.models import Group
from rest_framework import permissions

from mapping.models import MappingProject


class MappingProjectAccessPermission(permissions.BasePermission):
    """
    Global permission check rights to use the RC Audit functionality.
    """
    def has_permission(self, request, view):
        try:
            request.user.groups.get(name="mapping | access")
        except Group.DoesNotExist:
            pass
        else:
            if "project_pk" in view.kwargs:
                try:
                    request.user.access_users.get(pk=view.kwargs["project_pk"])
                except MappingProject.DoesNotExist:
                    pass
                else:
                    return True
            else:
                # TODO: Needs revision.
                return True
