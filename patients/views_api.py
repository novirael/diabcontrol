# encoding: utf-8
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import Relationship
from patients.serializers import RelationshipUserSerializer


class RelationshipListView(APIView):
    def get(self, request, *args, **kwargs):
        is_doctor = self.request.user.groups.filter(name='Doctor').exists()

        if is_doctor:
            relations_users = Relationship.objects.get_doctor_relations(self.request.user)
        else:
            relations_users = Relationship.objects.get_patient_relations(self.request.user)

        serializer = RelationshipUserSerializer(relations_users, many=True)

        return Response(serializer.data)
