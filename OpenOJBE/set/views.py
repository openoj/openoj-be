import django_filters
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from set.models import Set, SetProblem, SetUser
from set.permissions import SetPermission, SetProblemPermission
from set.serializers import (SetDetailSerializer, SetProblemDetailSerializer,
                             SetProblemSerializer, SetSerializer)


class SetFilter(django_filters.FilterSet):
    class Meta:
        model = Set
        fields = {
            'id': ['icontains'],
            'title': ['icontains'],
            'type': ['exact'],
        }


class SetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    filter_class = SetFilter
    permission_classes = (SetPermission,)

    def get_serializer_class(self):
        if self.detail:
            return SetDetailSerializer
        return SetSerializer


class SetProblemFilter(django_filters.FilterSet):
    class Meta:
        model = SetProblem
        fields = {
            'st': ['exact'],
        }


class SetProblemViewSet(viewsets.ModelViewSet):
    queryset = SetProblem.objects.all()
    serializer_class = SetProblemSerializer
    filter_class = SetProblemFilter
    permission_classes = (SetProblemPermission,)

    def get_serializer_class(self):
        if self.detail:
            return SetProblemDetailSerializer
        return SetProblemSerializer


class CheckSetPermission(APIView):
    def post(self, request):
        st = request.POST.get('set')
        password = request.POST.get('password')
        st = Set.objects.filter(id=int(st))
        if not st:
            return Response({
                "result": "error",
                "msg": "Set does not exist"
            })
        else:
            st = st[0]
        if password != st.password:
            return Response({
                "result": "error",
                "msg": "Wrong password"
            })
        set_user = SetUser.objects.filter(st=st, user=request.user)
        if not set_user:
            set_user = SetUser()
            set_user.user = request.user
            set_user.st = st
        else:
            set_user = set_user[0]
        set_user.password = password
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        set_user.ip = ip
        set_user.save()
        return Response({
            "result": "success"
        })
