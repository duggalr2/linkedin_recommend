from django.shortcuts import render, redirect, get_object_or_404, reverse, get_list_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from link_rec.forms import SignUpForm, MisClassify, EducationMisClassify, JobMisClassify
from .models import Profile, AllParsedProfile, AllJobTitle
import ast
from link_rec.link_new.temp_jobtitle_classifier import nb_classification
from link_rec.link_new.temp_jobtitle_classifier import edu_classification

# TODO: Rank the profiles so when the intersection is made, rank further based on program/companies/jobtitles!!

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
    # form = MisClassify(request.GET or None)
    # # if request.method == 'GET':
    # #     form = MisClassify(request.GET)
    # if form.is_valid():
    #     choice = form.cleaned_data
    #     if choice == 'education_program':
    #         return redirect('edu_misclassify')
    #     else:
    #         return redirect('job_misclassify')

    industry_rec = request.user.profile.industry_of_interest
    x = ast.literal_eval(industry_rec)
    for n in x:  # TODO: FIX THIS LATER!
        if type(n) == int:
            x = [n for n in x]
        else:
            x = [n.strip() for n in x]  # converting str representation of list to python list
    li_industry = nb_classification.recommend_industry(x)
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


# ('Software Development Engineering in Test (Co-op)', '')
# ('Software Test Engineer (Co-op)', '')
# ('Swim Instructor/Life Guard', '')
# ('C++ Software Developer, Projection Mapping', 'software')

@login_required(login_url='login/')
def job_misclassify(request, id):
    instance = get_list_or_404(AllJobTitle, profile_id=id)
    id_instance = [job.id for job in instance]
    instance = [job.job for job in instance]
    form = JobMisClassify(request.POST or None, extra=instance)
    industry_map = {'software': 0, 'engineering': 1, 'research': 2, 'design': 3, 'data_science': 4,
                    'product_manager': 5, 'business_finance': 6, 'startup_founder': 7,
                    'admin_it': 8, 'crypto': 9}

    if form.is_valid():
        for i in form.extra_answers():
            i = list(i)
            if len(i[-1]) > 0:
                if i[-1] in industry_map.keys():
                    i[-1] = industry_map.get(i[-1])
                    index = instance.index(i[0])
                    job_id = id_instance[index]
                    j = AllJobTitle.objects.get(id=job_id)
                    j.job_classification = i[-1]
                    j.save()

        return redirect('home')
    return render(request, 'job_misclassify.html', {'form':form})


@login_required(login_url='login/')
def edu_misclassify(request, id):
    instance = get_list_or_404(AllParsedProfile, id=id)
    # program = instance.school_program
    form = EducationMisClassify(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        return redirect('home')
    return render(request, 'edu_misclassify.html', {'form':form, 'education':instance})







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


