from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'homepage.html'


def loginpage(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        #request.session['username']=username
        if user:
             login(request,user)
             request.session['username']=username
             return redirect('profile')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'profile.html', {"query":query})
    else:
        return render(request, 'login.html', {})



def logout(request):
    try:
        del request.session['username']
        logout(request)
    except:
     pass
    return render(request, 'login.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=User.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
