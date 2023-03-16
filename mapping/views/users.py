from django.contrib.auth.models import User
import json

from rest_framework.generics import ListCreateAPIView
from rest_framework import status, viewsets
from rest_framework.response import Response

from mapping.tasks import *
from mapping.models import *
from mapping.permissions import MappingProjectAccessPermission



class MappingUsers(viewsets.ViewSet):
    permission_classes = [MappingProjectAccessPermission]

    def retrieve(self, request, pk=None):
        print(f"[users/MappingUsers retrieve] requested by {request.user} - {pk}")

        current_user = User.objects.get(id=request.user.id)
        project = MappingProject.objects.get(id=pk, access__username=current_user)
        users = User.objects.all().order_by('username').prefetch_related(
            'groups'
        )
        tasks = MappingTask.objects.all()
        output = []
        # For each user
        for user in users:
            # Check if they have access, or have any tasks to their name. If so, add to list.
            if tasks.filter(user=user).exists() or user.groups.filter(name='mapping | access').exists():
                output.append({
                    'value' : user.id,
                    'text' : user.username,
                    'name': f"{user.first_name} {user.last_name}"
                })     

        return Response(output)

    def create(self, request):
        print(f"[users/MappingUsers create] requested by {request.user} - data: {str(request.data)[:500]}")

        task = MappingTask.objects.get(id=request.data.get('task'))
        current_user = User.objects.get(id=request.user.id)
        if MappingProject.objects.filter(id=task.project_id.id, access__username=current_user).exists():

            newuser = User.objects.get(id=request.data.get('user'))
            if task.user == None:    
                source_user = User.objects.get(id=1)
            else:
                source_user = User.objects.get(id=task.user.id)
            target_user = User.objects.get(id=request.data.get('user'))
            current_user = User.objects.get(id=request.user.id)
            task.user = newuser
            task.save()

            # Save snapshot to database
            source_component = MappingCodesystemComponent.objects.get(id=task.source_component.id)
            mappingquery = MappingRule.objects.filter(source_component_id=source_component.id)
            mappingrules = []
            for rule in mappingquery:
                bindings = []
                for binding in rule.mapspecifies.all():
                    bindings.append(binding.id)
                mappingrules.append({
                    'Rule ID' : rule.id,
                    'Project ID' : rule.project_id.id,
                    'Project' : rule.project_id.title,
                    'Target codesystem' : rule.target_component.codesystem_id.codesystem_title,
                    'Target component ID' : rule.target_component.component_id,
                    'Target component Term' : rule.target_component.component_title,
                    'Mapgroup' : rule.mapgroup,
                    'Mappriority' : rule.mappriority,
                    'Mapcorrelation' : rule.mapcorrelation,
                    'Mapadvice' : rule.mapadvice,
                    'Maprule' : rule.maprule,
                    'Active' : rule.active,
                    'Bindings' : bindings,
                })            
            # print(str(mappingrules))
            event = MappingEventLog.objects.create(
                    task=task,
                    action='user_change',
                    action_user=current_user,
                    action_description='Gebruiker:',
                    old_data='',
                    new_data=json.dumps(mappingrules),
                    old=str(source_user),
                    new=str(target_user),
                    user_source=source_user,
                    user_target=target_user,
                )
            event.save()
            print(str(task))

            # Disabled due to resource management -> usual workflow changes user+status, triggering 2 simultaneous audits.
            # audit_async.delay('multiple_mapping', task.project_id.id, task.id)

            return Response([])
        else:
            return Response('Geen toegang', status=status.HTTP_401_UNAUTHORIZED)
