
from celery import shared_task
from celery.utils.log import get_task_logger
from mapping.models import MappingProject, MappingTask, MappingECLConcept


@shared_task
def unmapped_components():
    def get_concept_codes(task: MappingTask) -> list[str]:
        """Get list of concepts codes for any given task.

        Args:
            task (MappingTask): Task instance.

        Returns:
            List of concept codes.
        """
        exclude_components = [] if task.exclusions is None else task.exclusions

        try:
            remote_exclusion = task.mappingeclpartexclusion_set.all()[0]
        except IndexError:
            remote_exclusion = None
        if remote_exclusion is not None:
            exclude_components = list(set(exclude_components + remote_exclusion.components))

        exclusions = MappingECLConcept.objects.filter(
            task__project_id=task.project_id_id,
            task__source_component__codesystem_id_id=task.source_component.codesystem_id_id,
            task__source_component__component_id__in=exclude_components,
        ).values_list("code", flat=True)

        return MappingECLConcept.objects.filter(
            task_id=task.id
        ).exclude(
            code__in=exclusions
        ).values_list("code", flat=True)

    for project in MappingProject.objects.filter(pk=1).all():
        project_codes = []
        project_tasks = MappingTask.objects.filter(project_id=project).select_related("source_component").prefetch_related("mappingeclpartexclusion_set")
        for task in project_tasks:
            project_codes += get_concept_codes(task=task)

        print(project, len(project_codes))
