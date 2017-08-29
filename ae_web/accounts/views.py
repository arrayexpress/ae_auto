from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, FormView
from django.shortcuts import redirect
from django.db.models import Q
from django.core.exceptions import ValidationError

from braces.views import JSONResponseMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from .forms import RegistrationForm
from .serializers import UserSerializer
from .models import User
from .permissions import IsSuperAdminOrManager


class LoginView(JSONResponseMixin, View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/api/me')

        return self.render_json_response({
            'error': 'username and password combination doesn\'t exist'
        }, status=status.HTTP_400_BAD_REQUEST)


class LoggedInMixIn(object):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return self.render_json_response({
                'error': 'Log in required !'
            }, status=status.HTTP_403_FORBIDDEN)
        if not self.request.user.is_admin and not self.request.user.is_super_admin:
            return self.render_json_response({
                'error': 'User not admin !'
            }, status=status.HTTP_403_FORBIDDEN)
        return super(LoggedInMixIn, self).dispatch(*args, **kwargs)


class RegistrationView(JSONResponseMixin, FormView):
    form_class = RegistrationForm
    template_name = 'notemplate.html'

    def form_invalid(self, form):
        return self.render_json_response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def form_valid(self, form):
        form.create()
        return self.render_json_response({}, status.HTTP_201_CREATED)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class MeView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_super_admin:
            return User.objects.all()
        return User.objects.filter(
            Q(manager=self.request.user) |
            Q(id=self.request.user.id)
        )


class UserDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsSuperAdminOrManager,)
    queryset = User.objects.all()
    model = User

    def destroy(self, request, *args, **kwargs):
        try:
            return super(UserDetailView, self).destroy(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': e.message}
            )

    def pre_delete(self, obj):
        if obj.analysts.count() > 0:
            raise ValidationError('can\'t delete an admin with analysts')
        if obj.id == self.request.user.id:
            raise ValidationError('you can\'t delete yourself')
        return super(UserDetailView, self).pre_delete(obj)


class EditView(JSONResponseMixin, View):
    def post(self, request):
        password = request.POST.get('password')
        analyst_id = request.POST.get('id')
        if not int(analyst_id) == int(self.request.user.id) and not self.request.user.is_super_admin:
            return self.render_json_response({
                'error': 'you dont have enough permissions to change the password'
            }, status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(id=analyst_id)
        user.set_password(password)
        user.save()
        return self.render_json_response({}, 200)

#
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer

#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
