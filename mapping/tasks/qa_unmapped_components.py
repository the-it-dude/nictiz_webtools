
from celery import shared_task
from celery.utils.log import get_task_logger
from mapping.enums import ProjectAuditTypes
from mapping.models import MappingCodesystemComponent, MappingProject, MappingProjectAudit, MappingTask, MappingECLConcept


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

    for project in MappingProject.objects.filter(pk=9).all():
        # Clear all audits.
        MappingProjectAudit.objects.filter(project=project).exclude(sticky=True).delete()

        project_codes = []
        project_tasks = MappingTask.objects.filter(project_id=project).select_related("source_component").prefetch_related("mappingeclpartexclusion_set")
        for task in project_tasks:
            project_codes += get_concept_codes(task=task)

        components = MappingCodesystemComponent.objects.filter(codesystem_id=project.source_codesystem).exclude(component_id__in=project_codes)
        for component in components:
            MappingProjectAudit.objects.get_or_create(
                project=project,
                audit_type=ProjectAuditTypes.unmapped_component.value,
                hit_reason=f"Concept {component.component_id} is niet gemapt."
            )
