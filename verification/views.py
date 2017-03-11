from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.template.context_processors import csrf
from .models import LoginForm, User

from rest_framework import authentication, permissions, viewsets
from .serializers import UserSerializer


class DefaultsMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_parm = 'page_size'
    max_paginate_by = 100


class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    # API for listing users
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer


def register(request):
    # redirect to homepage if user is logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect('/homepage')

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        password = request.POST['pass']
        repass = request.POST['repass']

        if not (firstname and lastname and username and password):
            return render(request, 'registration/register.html',
                          {'register_message':
                              'Please Do Not Leave Fields Empty', },
                          RequestContext(request))
        if password != repass:
            return render(request, 'registration/register.html',
                          {'register_message': 'Passwords do not match!', },
                          RequestContext(request))

        try:
            user = User.objects.get(username=username)
            return render(request, 'registration/register.html',
                          {'register_message': 'User already exists!', },
                          RequestContext(request))
        except User.DoesNotExist:
            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            return HttpResponseRedirect('/register/complete')

    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response('registration/register.html', token)


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('homepage')
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            auth_login(request, user)
            return render_to_response('home/index.html')
    if form.errors:
        return render(request, 'registration/login.html', {'login_message':
            'Incorrect Username or Password', }, RequestContext(request))
    return render(request, 'registration/login.html', {'login_message':
        'Enter your Username and Password', }, RequestContext(request))


def registration_complete(request):
    return render_to_response('registration/registration_complete.html')


def loggedin(request):
    return render_to_response('registration/loggedin.html',
                              {'username': request.user.username})


def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
        template = loader.get_template('registration/loggedout.html')
        return HttpResponse(template.render(request))
    else:
        return HttpResponseRedirect('login')


@login_required
def homepage(request):
    return render_to_response('home/homepage.html')


def index(request):
    return render_to_response('home/index.html')
