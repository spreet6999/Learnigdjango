from django.shortcuts import render

from basic_app.forms import UserForm, UserProfileInfoForm
from basic_app.models import UserProfileInfo

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')


@login_required # decorator to check if user is signed in or not for a logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
    # reverse is just like a template tag which we use in .html files
    # {% url 'index' %}

def register(request):
    registered = False
    
    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password) # this is basically hashing that password
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user # setting one to one relationship in views only

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        # Since we are using only html in our template login.html
        # and we are naming our imput as username and password
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
                # reverse is just like a template tag which we use in .html files
                # {% url 'index' %}


            else:
                return HttpResponse("Account NOT Active")

            
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("invalid login details supplied!")
        
    else:
        return render(request, 'basic_app/login.html', {})