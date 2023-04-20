from django.db.models import Count
import django_filters.rest_framework
from rest_framework import filters
from rest_framework.generics import ListAPIView, ListCreateAPIView

from mapping.models import (
    MappingECLConcept,
    MappingEclPart,
    MappingRule,
    MappingTask,
)
from mapping.permissions import (
    MappingProjectAccessPermission,
    MappingTaskAccessPermission,
)
from mapping.serializers import (
    MappingECLConceptExclusionSerializer,
    MappingECLConceptSerializer,
    MappingECLPartSerializer,
    MappingRuleSerializer,
)


class TaskRelatedView:
    permission_classes = [
        MappingProjectAccessPermission,
        MappingTaskAccessPermission,
    ]


class MappingTaskTargetsView(TaskRelatedView, ListCreateAPIView):
    """List and create mapping targets (MappingRules)."""

    serializer_class = MappingRuleSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        django_filters.rest_framework.DjangoFilterBackend
    ]

    ordering_fields = [
        "source_component__component_id",
        "source_component__component_title",
        "mapcorrelation",
    ]
    filterset_fields = [
        "source_component__component_title",
        "source_component__component_id"
    ]
    search_fields = [
        "^source_component__component_id",
        "^source_component__component_title"
    ]

    def get_queryset(self):
        task = MappingTask.objects.get(pk=self.kwargs["task_pk"])

        return (
            MappingRule.objects.filter(
                project_id=task.project_id,
                target_component=task.source_component,
            )
            .select_related(
                "source_component",
                "source_component__codesystem_id",
                "target_component",
                "target_component__codesystem_id",
            )
            .order_by("mapgroup", "mappriority")
        )


class MappingTaskExclusionsView(TaskRelatedView, ListAPIView):
    """List MappingTask exclusions."""

    serializer_class = MappingECLConceptExclusionSerializer

    def get_queryset(self):
        task = MappingTask.objects.get(pk=self.kwargs["task_pk"])
        # Filter empty and incorrect components.
        components = [] if task.exclusions is None else task.exclusions

        queryset = MappingECLConcept.objects.filter(
            task=task,
            task__source_component__component_id__in=components,
        ).select_related("task", "task__source_component")
        return queryset


class MappingTaskECLPartsView(TaskRelatedView, ListCreateAPIView):
    """List ECL Parts for given task."""

    serializer_class = MappingECLPartSerializer

    def get_queryset(self):
        return (
            MappingEclPart.objects.filter(task_id=self.kwargs["task_pk"])
            .annotate(concepts_count=Count("concepts"))
            .order_by("id")
        )



class MappingECLConceptsView(TaskRelatedView, ListAPIView):
    """List All results for a given MappingECLPart."""

    serializer_class = MappingECLConceptSerializer
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ["code", "ecl_id"]
    search_fields = ["^id", "^code"]

    def get_queryset(self):
        task = MappingTask.objects.get(pk=self.kwargs["task_pk"])
        exclusions = [] if task.exclusions is None else task.exclusions

        return MappingECLConcept.objects.filter(
            task_id=self.kwargs["task_pk"]
        ).exclude(task__source_component__component_id__in=exclusions).select_related("ecl")
