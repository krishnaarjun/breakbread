from .models import PotluckSurvey, HowYouHeard, PotluckGroup, PotluckFood, PotluckFoodGroup
from .serializers import PotluckSurveySerializer, HowYouHeardSerializer, PotluckGroupListSerializer, PotluckGroupCreateSerializer, PotluckSurveyCsvCreateSerializer, PotluckFoodSerializer, PotluckFoodGroupSerializer, PotluckGroupLockSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status, generics
import json
import csv
import io
import uuid
from itertools import zip_longest, chain
from math import ceil
from faker import Faker
from rest_framework import mixins
from django.http import HttpResponse
from breakbread.utils import is_valid_uuid
from potluck.tasks import email_on_potluck_publish


class ViewsetBaseFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_dict = {key.strip(): value.strip()
                       for (key, value) in request.query_params.items()}
        for entry in ("ordering", "page"):
            if entry in filter_dict:
                del filter_dict[entry]
        return queryset.filter(**filter_dict)


class PotluckSurveyViewset(viewsets.ModelViewSet):
    queryset = PotluckSurvey.objects.all()
    serializer_class = PotluckSurveySerializer
    filter_backends = (ViewsetBaseFilter, filters.OrderingFilter,)

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny(), ]
        else:
            return [IsAuthenticated(), ]
    ordering_fields = '__all__'


class HowYouHeardViewset(viewsets.ModelViewSet):
    queryset = HowYouHeard.objects.all()
    serializer_class = HowYouHeardSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [AllowAny(), ]
        elif self.action == 'update':
            return [IsAuthenticated(), ]


class SurveyCSVViewset(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        csv_file = request.FILES['file']
        csv_file.seek(0)
        readers = csv.DictReader(io.StringIO(
            csv_file.read().decode('utf-8')), delimiter=',', quotechar='"')
        for reader in readers:
            data = dict(reader)
            if 'heard_from' in data and data['heard_from'] not in (None, '') and bool(data['heard_from'].strip()):
                data['heard_from'] = data['heard_from'].split(',')
            data['is_agreed'] = True if data['is_agreed'] in (
                'True', 'true', 't', 'TRUE') else False
            potluck_survey_serializer = PotluckSurveySerializer(
                data=data)
            if potluck_survey_serializer.is_valid():
                potluck_survey_serializer.save()
            else:
                return Response(potluck_survey_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'successfully uploaded csv file'}, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="surveys.csv"'
        queryset = PotluckSurvey.objects.all()
        serializer = PotluckSurveyCsvCreateSerializer(queryset, many=True)
        header = PotluckSurveyCsvCreateSerializer.Meta.fields
        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        return response


class GroupsList(APIView):
    """
    List all randomised Potluck groups
    """

    def get(self, request, format=None):
        group_size = 5
        faker = Faker()
        baa_qset = PotluckSurvey.objects.filter(
            ethnic_persuasion='black or african american', potluckgroup=None).order_by('?')
        w_qset = PotluckSurvey.objects.filter(
            ethnic_persuasion='white', potluckgroup=None).order_by('?')
        pns_qset = PotluckSurvey.objects.filter(
            ethnic_persuasion='prefer not to say', potluckgroup=None).order_by('?')

        def zip_ethnic_qsets(seq):
            return [list(x for x in item if x is not None) for item in zip_longest(*seq)]

        attendees_count = baa_qset.count() + w_qset.count() + pns_qset.count()
        if attendees_count == 0:
            return Response([], status=status.HTTP_200_OK)
        groups_count = ceil(attendees_count/group_size)
        potluck_groups = zip_ethnic_qsets(
            [baa_qset, w_qset, pns_qset])
        remaining_group_members = potluck_groups[groups_count:]
        potluck_groups = potluck_groups[:groups_count]
        if len(potluck_groups[-1]) > attendees_count % group_size:
            remaining_group_members += [potluck_groups[-1]
                                        [attendees_count % group_size:]]
            potluck_groups[-1] = potluck_groups[-1][:attendees_count %
                                                    group_size]
        remaining_group_members = list(
            chain.from_iterable(remaining_group_members))
        group_results = []
        for gid in range(groups_count):
            try:
                group = potluck_groups[gid]
            except:
                potluck_groups.append([])
                group = potluck_groups[gid]
            group_count = len(group)
            if group_count < group_size:
                group += remaining_group_members[0: group_size - group_count]
                group = json.loads(JSONRenderer().render(
                    PotluckSurveySerializer(group, many=True).data))
                group_results.append({"name": faker.name(), "results": group})
                remaining_group_members = remaining_group_members[group_size - group_count:]
        return Response(group_results, status=status.HTTP_200_OK)


class PotluckGroupViewSet(generics.ListCreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = PotluckGroup.objects.all()
    serializer_class = PotluckGroupListSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        survey_qset = PotluckSurvey.objects.filter(
            pk__in=request.data['attendees'])
        for survey in survey_qset.iterator():
            if survey.survey_meta_data is None:
                survey.survey_meta_data = {}
            survey.survey_meta_data['avatar_gradient'] = request.data['attendees_avatar_gradients'].pop(
            )
            survey.save()
        write_serializer = PotluckGroupCreateSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        created_instance = write_serializer.save()
        # created_instance = self.perform_create(write_serializer)
        read_serializer = PotluckGroupListSerializer(created_instance)
        return Response(read_serializer.data)

    def partial_update(self, request, potluck_id=None):

        try:
            potluck_group_obj = self.queryset.get(id=potluck_id)
            update_serializer = PotluckGroupLockSerializer(
                potluck_group_obj, data=request.data, partial=True)
            if update_serializer.is_valid():
                updated_instance = update_serializer.save()
                data = PotluckGroupListSerializer(updated_instance).data
                group_info = {
                    'id': data['id'], 'name': data['name'], 'hosting_on': data['hosting_on']}
                guests = data['attendees']
                orign = request.META['HTTP_ORIGIN']
                email_on_potluck_publish.delay(
                    origin=orign, group_info=group_info, user_info=data['manager'], guests=guests)
                for guest in guests:
                    email_on_potluck_publish.delay(
                        origin=orign, group_info=group_info, user_info=guest)
                return Response({'message': 'Potluck successfully published'}, status=status.HTTP_200_OK)
            else:
                return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Error publishing potluck group"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, potluck_id=None, *args, **kwargs):
        if potluck_id is None:
            self.queryset.delete()
        else:
            self.queryset.filter(id=potluck_id).delete()
        return Response({'message': 'Potluck successfully deleted'}, status=status.HTTP_200_OK)


class PotluckSelectFoodViewset(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None, group_id=None, user_id=None):
        if is_valid_uuid(group_id) == None:
            return Response({"message": "group id is not a valid uuid"}, status=status.HTTP_400_BAD_REQUEST)
        elif is_valid_uuid(user_id) == None:
            return Response({"message": "user id is not a valid uuid"}, status=status.HTTP_400_BAD_REQUEST)
        group_query = get_object_or_404(PotluckGroup, pk=group_id)
        user_query = get_object_or_404(group_query.attendees, pk=user_id)
        available_foods = [{'id': fd['id'].hex, 'name':fd['name'],
                            'type': fd['type']} for fd in group_query.foods.values()]
        food_group_qset = PotluckFoodGroup.objects.filter(group_id_id=group_id)
        registered_foods = [i.food_id_id.hex for i in food_group_qset]

        current_user_foods = [
            i.food_id_id.hex for i in food_group_qset if i.guest_id_id == uuid.UUID(user_id)]
        return Response({'group_info': {'group_id': group_query.id.hex, 'group_name': group_query.name}, 'user_info': {'user_id': user_query.id.hex, 'user_name': user_query.name}, 'food_info': {'available_foods': available_foods, 'registered_foods': registered_foods, 'current_user_foods': current_user_foods}}, status=status.HTTP_200_OK)

    def post(self, request, format=None, group_id=None, user_id=None):
        selected_foods = request.data.get('selected_foods')
        if selected_foods == None or len(selected_foods) == 0:
            return Response({"message": "foods are required"}, status=status.HTTP_400_BAD_REQUEST)
        elif is_valid_uuid(group_id) == None:
            return Response({"message": "group id is not a valid uuid"}, status=status.HTTP_400_BAD_REQUEST)
        elif is_valid_uuid(user_id) == None:
            return Response({"message": "user id is not a valid uuid"}, status=status.HTTP_400_BAD_REQUEST)
        group_query = get_object_or_404(PotluckGroup, pk=group_id)
        user_query = get_object_or_404(group_query.attendees, pk=user_id)
        for food_id in selected_foods:
            food_group_query, created = PotluckFoodGroup.objects.update_or_create(
                food_id_id=food_id, group_id_id=group_id, guest_id_id=user_id)
        return Response({'message': 'foods have been submitted successfully'}, status=status.HTTP_200_OK)


class PotluckFoodViewset(viewsets.ModelViewSet):
    queryset = PotluckFood.objects.all()
    serializer_class = PotluckFoodSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (ViewsetBaseFilter, filters.OrderingFilter,)
    ordering_fields = '__all__'


class PotluckFoodGroupViewset(viewsets.ModelViewSet):
    queryset = PotluckFoodGroup.objects.all()
    serializer_class = PotluckFoodGroupSerializer
    permission_classes = [AllowAny]
