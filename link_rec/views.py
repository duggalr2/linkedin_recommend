from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from link_rec.forms import SignUpForm
from .models import Profile
import ast
from link_rec.link_new.temp_jobtitle_classifier import nb_classification
from link_rec.link_new.temp_jobtitle_classifier import edu_classification


#@login_required(login_url='login/')
def personal_view(request):
#    if request.method == 'GET':
    return render(request, 'button.html')


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
            # print(industry_of_interest)  # ['software', 'data_science', 'research']
            # li_industry = nb_classification.recommend_industry(industry_of_interest)
            # s = school_program.split()
            # edu_li = edu_classification.recommend_program(s)
            user.profile.current_school = current_school
            user.profile.school_program = school_program
            user.profile.school_of_interest = school_of_interest
            user.profile.industry_of_interest = industry_of_interest
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            # request.session['industry_rec'] = li_industry
            # request.session['edu_rec'] = edu_li
            # request.session['user_school'] = current_school
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login/')
def home(request):
    industry_rec = request.user.profile.industry_of_interest
    li_industry = nb_classification.recommend_industry(industry_rec)
    edu_rec = request.user.profile.school_program
    edu_li = edu_classification.recommend_program(edu_rec.split())
    current_school = request.user.profile.current_school
    ind_profile_info = [nb_classification.get_profile_info(id) for id in li_industry]
    edu_profile_info = [nb_classification.get_profile_info(id) for id in edu_li]
    new_int = edu_classification.find_intersection(ind_profile_info, edu_profile_info)
    cosine_sim_list = edu_classification.cosine_school(edu_classification.intersection_school_name(new_int), current_school)
    big_profile_info = [nb_classification.get_profile_info(row[0]) for row in cosine_sim_list]
    return render(request, "home.html", {'industry_recommend': ind_profile_info, 'edu_recommend': edu_profile_info,
                                         'intersection': big_profile_info})


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


