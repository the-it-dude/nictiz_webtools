import factory

from mapping.enums import ProjectTypes, RuleCorrelations
from mapping.models import MappingEclPart, MappingProject, MappingTask


class MappingProjectFactory(factory.django.DjangoModelFactory):
    """Mapping Project Factory."""

    class Meta:
        model = MappingProject

    title = factory.Sequence(lambda n: f"Project #{n}")
    project_type = ProjectTypes.snomed_ecl_to_one.value
    active = True


class MappingTaskFactory(factory.django.DjangoModelFactory):
    """Mapping Task Factory."""

    class Meta:
        model = Mappingtask

    project_id = factory.SubFactory(MappingProjectFactory)
    category = factory.Sequence(lambda n: f"Category #{n}")


class MappingECLPartFactory(factory.django.DjangoModelFactory):
    """Mapping ECL Part Factory."""

    class Meta:
        model = MappingEclPart


    task = factory.SubFactory(MappingTaskFactory)
    mapcorrelation = RuleCorrelations.exact_match.value
