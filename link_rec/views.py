from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from link_rec.forms import SignUpForm
from .models import Profile
import ast


@login_required(login_url='login/')
def home(request):
    y = Profile.objects.all()
    return render(request, "home.html", {'content': y})


#@login_required(login_url='login/')
def personal_view(request):
#    if request.method == 'GET':

    return render(request, 'button.html')


def parse_to_list(form_input):
    l = ast.literal_eval(form_input)
    l = [i.strip() for i in l]
    return l

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.name = form.cleaned_data.get('name')
            current_school = form.cleaned_data.get('school')
            school_program = form.cleaned_data.get('school_program')
            school_of_interest = form.cleaned_data.get('school_of_interest')
            industry_of_interest = form.cleaned_data.get('industry_of_interest')
            # TODO: type's for both below are already lists.. just pass directly to
            # TODO: script and don't need to have the parse_to_list function!
            #print(type(industry_of_interest), type(school_of_interest))
            #parsed_school_of_interest = parse_to_list(school_of_interest)
            #parsed_industry_of_interest = parse_to_list(industry_of_interest)
            user.profile.current_school = current_school
            user.profile.school_program = school_program
            user.profile.school_of_interest = school_of_interest
            user.profile.industry_of_interest = industry_of_interest
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


#def ind(request):
    # if request.method == 'POST':
    #     form = AuthorForm(request.POST)
    #     if form.is_valid():
    #         y = form.save()
    #         print(form.cleaned_data.get('title'))
    #         return redirect('home')
    # else:
    #     form = AuthorForm()
#    if request.method == 'POST':
#        form = FormForm(request.POST)
#        if form.is_valid():
#            print(form['e'])
#            return redirect('home')
#    else:
#        form = FormForm()
#    return render(request, 'index.html', {'form': form})
#

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


