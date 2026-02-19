from rest_framework import serializers
from .models import SalaryComponent, SalaryStructure, SalaryStructureVersion, SalaryStructureComponent


class SalaryComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryComponent
        fields = "__all__"


class SalaryStructureComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructureComponent
        fields = ["salary_component", "calculation_type", "value"]


class SalaryStructureVersionSerializer(serializers.ModelSerializer):
    components = SalaryStructureComponentSerializer(many=True)

    class Meta:
        model = SalaryStructureVersion
        fields = ["id", "effective_from", "effective_to", "components"]


class SalaryStructureSerializer(serializers.ModelSerializer):
    versions = SalaryStructureVersionSerializer(many=True)

    class Meta:
        model = SalaryStructure
        fields = "__all__"

    def create(self, validated_data):
        versions_data = validated_data.pop("versions")
        structure = SalaryStructure.objects.create(**validated_data)

        for version_data in versions_data:
            components_data = version_data.pop("components")
            version = SalaryStructureVersion.objects.create(
                salary_structure=structure,
                **version_data
            )

            for component_data in components_data:
                SalaryStructureComponent.objects.create(
                    salary_structure_version=version,
                    **component_data
                )

        return structure
