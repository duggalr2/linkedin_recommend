from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from link_rec.forms import SignUpForm, AuthorForm, BookForm, FormForm
from .models import Profile


@login_required(login_url='login/')
def home(request):
    y = Profile.objects.all()
    return render(request, "home.html", {'content': y})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.school = form.cleaned_data.get('school')
            user.profile.school_program = form.cleaned_data.get('school_program')
            user.profile.industry_interest = form.cleaned_data.get('industry_interest')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def ind(request):
    # if request.method == 'POST':
    #     form = AuthorForm(request.POST)
    #     if form.is_valid():
    #         y = form.save()
    #         print(form.cleaned_data.get('title'))
    #         return redirect('home')
    # else:
    #     form = AuthorForm()
    if request.method == 'POST':
        form = FormForm(request.POST)
        if form.is_valid():
            print(form['e'])
            return redirect('home')
    else:
        form = FormForm()
    return render(request, 'index.html', {'form': form})


# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})


