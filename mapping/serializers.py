from rest_framework import serializers

from mapping.models import (
    MappingTask,
    MappingCodesystemComponent,
    MappingCodesystem,
    MappingTaskStatus,
    MappingRule,
    MappingEclPart,
    MappingECLConcept,
)


class MappingCodesystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingCodesystem
        fields = ("id", "version", "title")

    version = serializers.CharField(source="codesystem_version")
    title = serializers.CharField(source="codesystem_title")


class MappingCodesystemComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingCodesystemComponent
        fields = ("id", "title")

    id = serializers.CharField(source="component_id")
    title = serializers.CharField(source="component_title")


class MappingCodesystemExtendedComponentSerializer(serializers.ModelSerializer):
    """Component serializer that includes Codesystem definition."""

    class Meta:
        model = MappingCodesystemComponent
        fields = ("id", "title", "extra", "codesystem")

    id = serializers.CharField(source="component_id")
    title = serializers.CharField(source="component_title")
    extra = serializers.DictField(source="component_extra_dict")
    codesystem = MappingCodesystemSerializer(source="codesystem_id", read_only=True)


class MappingTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingTaskStatus
        fields = ("id", "title")

    title = serializers.CharField(source="status_title")


class MappingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingTask
        fields = ("id", "user", "component", "status")

    user = serializers.SerializerMethodField()
    component = MappingCodesystemExtendedComponentSerializer(
        source="source_component", read_only=True
    )
    status = MappingTaskStatusSerializer(read_only=True)

    def get_user(self, obj: MappingTask) -> dict:
        if obj.user is None:
            return {
                "id": "Niet toegewezen",
                "username": "Niet toegewezen",
                "name": "Niet toegewezen",
            }
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "name": obj.user.get_full_name(),
        }


class MappingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingRule
        fields = ("id", "source", "target", "correlation")

    source = MappingCodesystemComponentSerializer(
        source="source_component", read_only=True
    )
    target = MappingCodesystemExtendedComponentSerializer(
        source="starget_component", read_only=True
    )
    correlation = serializers.CharField(source="mapcorrelation")


class MappingECLPartSerializer(serializers.ModelSerializer):
    """Serialize Mapping ECL Part (query)."""

    class Meta:
        model = MappingEclPart
        fields = (
            "id",
            "description",
            "query",
            "finished",
            "error",
            "failed",
            "numResults",
            "correlation",
        )

    correlation = serializers.CharField(source="mapcorrelation")
    numResults = serializers.SerializerMethodField()

    def get_numResults(self, obj):
        """Get number of MappingECLConcepts for given part, use cached `concepts_count` if possible."""
        if hasattr(obj, "concepts_count"):
            return obj.concepts_count
        return obj.concepts.count()


class MappingECLConceptExclusionSerializer(serializers.ModelSerializer):
    """Exclusion serialiser for MappingECLConcepts."""

    class Meta:
        model = MappingECLConcept
        fields = ("key", "component")

    key = serializers.CharField(source="code")
    component = MappingCodesystemComponentSerializer(source="task__source_component")


class MappingECLConceptSerializer(serializers.ModelSerializer):
    """Mapping ECL Concept serializer."""

    class Meta:
        model = MappingECLConcept
        fields = (
            "code",
            "moduleId",
            "effectiveTime",
            "definitionStatus",
            "idAndFsnTerm",
            "active",
            "pt",
            "fsn",
            "queryId",
            "query",
            "description",
            "correlation",
        )

    moduleId = serializers.CharField(source="module_id")
    effectiveTime = serializers.CharField(source="effective_time")
    definitionStatus = serializers.CharField(source="definition_status")
    idAndFsnTerm = serializers.CharField(source="id_and_fsn_term")
    pt = serializers.SerializerMethodField()
    fsn = serializers.SerializerMethodField()
    queryId = serializers.CharField(source="ecl_id")
    query = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    correlation = serializers.SerializerMethodField()

    def get_pt(self, obj: MappingECLConcept) -> dict:
        """Get dictionary to represent legacy data as `pt` dictionary."""
        return {
            "term": obj.preferred_title,
            "lang": obj.pt_lang
        }

    def get_fsn(self, obj: MappingECLConcept) -> dict:
        """Get dictionary to represent legacy data as `fsn` dictionary."""
        return {
            "term": obj.fsn,
            "lang": obj.fsn_lang
        }

    def get_query(self, obj: MappingECLConcept) -> str:
        """Get ECL Query."""
        return obj.ecl.query

    def get_description(self, obj: MappingECLConcept) -> str:
        """Get Query description."""
        return obj.ecl.description

    def get_correlation(self, obj: MappingECLConcept) -> str:
        """Get Query correlation."""
        return obj.ecl.mapcorrelation