from rest_framework import serializers

from mapping.models import MappingTask, MappingCodesystemComponent, MappingCodesystem, MappingTaskStatus


class MappingCodesystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingCodesystem
        fields = ('id', "version", "title")

    version = serializers.CharField(source="codesystem_version")
    title = serializers.CharField(source="codesystem_title")


class MappingCodesystemComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingCodesystemComponent
        fields = ("id", "title", "codesystem")

    id = serializers.CharField(source="component_id")
    title = serializers.CharField(source="component_title")
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
    component = MappingCodesystemComponentSerializer(source="source_component", read_only=True)
    status = MappingTaskStatusSerializer(read_only=True)

    def get_user(self, obj: MappingTask) -> dict:
        if obj.user is None:
            return {
                "id": "Niet toegewezen",
                "username":
                "Niet toegewezen",
                "name": "Niet toegewezen"
            }
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "name": obj.user.get_full_name()
        }
