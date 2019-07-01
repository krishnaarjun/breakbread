from rest_framework import serializers, fields
from .models import HowYouHeard, PotluckSurvey, PotluckGroup, PotluckFood, PotluckFoodGroup


class HowYouHeardSerializer(serializers.ModelSerializer):

    class Meta:
        model = HowYouHeard
        fields = '__all__'


class PotluckFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PotluckFood
        fields = '__all__'


class PotluckFoodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PotluckFoodGroup
        fields = '__all__'


class HeardFromArrayField(serializers.RelatedField):
    def to_representation(self, obj):
        serializer = HowYouHeardSerializer(obj)
        return serializer.data

    def to_internal_value(self, data):
        return data

    class Meta:
        model = HowYouHeard
        queryset = HowYouHeard.objects.all()


class PotluckSurveySerializer(serializers.ModelSerializer):
    heard_from = HeardFromArrayField(
        many=True, queryset=HowYouHeard.objects.all(), required=False)

    class Meta:
        model = PotluckSurvey
        fields = ["id", "name", "email", "phone", "zipcode", "ethnic_persuasion", "involved", "church_affiliation", "availability",
                  "hosting_at", "dietary_restrictions_or_allergies", "comments_and_queries", "is_agreed", "heard_from"]

    def create(self, validated_data):
        if 'heard_from' in validated_data:
            heard_from = validated_data.pop('heard_from')
            instance, created = PotluckSurvey.objects.get_or_create(
                **validated_data)
            new_heard_from_qset = set(heard_from) - set(HowYouHeard.objects.filter(
                medium__in=heard_from).values_list('medium', flat=True))
            HowYouHeard.objects.bulk_create([HowYouHeard(
                type="other", medium=heard_from_item) for heard_from_item in new_heard_from_qset])
            instance.heard_from.add(
                *HowYouHeard.objects.filter(medium__in=heard_from).values_list('id', flat=True))
        else:
            instance = PotluckSurvey.objects.create(**validated_data)
        return instance


class HeardFromStringField(serializers.RelatedField):
    def to_representation(self, obj):
        return ",".join([query['medium'] for query in obj.values()])

    class Meta:
        model = HowYouHeard
        queryset = HowYouHeard.objects.all()


class PotluckSurveyCsvCreateSerializer(serializers.ModelSerializer):
    heard_from = HeardFromStringField(
        queryset=HowYouHeard.objects.all(), required=False)

    class Meta:
        model = PotluckSurvey
        fields = ["name", "email", "phone", "zipcode", "ethnic_persuasion", "involved", "church_affiliation", "availability",
                  "hosting_at", "dietary_restrictions_or_allergies", "comments_and_queries", "is_agreed", "heard_from"]


class PotluckGroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PotluckGroup
        fields = ('id', 'name', 'attendees', 'foods', 'group_meta_data',
                  'manager', 'status', 'hosting_on')
        depth = 1


class PotluckGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PotluckGroup
        fields = ('name', 'attendees', 'group_meta_data', 'manager')

    def create(self, validated_data):
        attendees = validated_data.pop('attendees')
        instance = PotluckGroup.objects.create(**validated_data)
        instance.attendees.add(*attendees)
        return instance


class PotluckGroupLockSerializer(serializers.ModelSerializer):
    # hosting_on = serializers.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])
    class Meta:
        model = PotluckGroup
        fields = ('name', 'foods', 'hosting_on', 'status')

    def update(self, instance, validated_data):
        foods = validated_data.pop('foods')
        for item in validated_data:
            setattr(instance, item, validated_data[item])
        instance.save()
        # PotluckGroup.objects.update(**validated_data)
        instance.foods.add(*foods)
        return instance
