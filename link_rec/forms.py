from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import formset_factory, ModelForm


INDUSTRY_CHOICES = (
    ('software', 'Software'),
    ('engineering', 'Engineering, excluding Software'),
    ('research', 'Research'),
    ('design', 'Design'),
    ('data_science', 'Data Science'),
    ('product_manager', 'Product Manager'),
    ('business_finance', 'Business and Finance'),
    ('startup_founder', 'Startup Founders/Executives'),
    ('admin_coordination', 'Startup Founders/Executives'),
    ('startup_founder', 'Admin/Coordination/IT/HR'),
    ('crypto_blockchain', 'Cryptography/Blockchain')
)

SCHOOL_NAMES = (
    ('university_of_toronto', 'University of Toronto'),
    ('harvard', 'Harvard University'),
    ('massachusetts_institute_of_technology', 'Massachusetts Institute of Technology'),
    ('waterloo', 'University of Waterloo'),
    ('stanford', 'Stanford University'),
    ('western', 'Western University'),
    ('university_of_california_berkeley', 'University of California, Berkeley'),
    ('caltech', 'Caltech'),
    ('cornell', 'Cornell University'),
    ('oxford', 'Oxford University'),
    ('carnegie_mellon_university', 'Carnegie Mellon University'),
    ('university_of_pennsylvania', 'University of Pennsylvania'),
    ('cambridge', 'University of Cambridge'),
    ('university_of_california_los_angeles', 'University of California, Los Angeles'),
    ('queens', "Queen's University"),
    ('columbia', 'Columbia University')
)

PROGRAM_CHOICES = (
    ('computer_science', 'Computer Science'),
    ('commerce_business', 'Commerce/Business/Finance'),
    ('humanities_lifesci', 'Humanities/LifeSci/HealthSci'),
    ('math_physics_statistics', 'Math/Physics/Statistics'),
    ('engineering', 'Engineering'),
)


class SignUpForm(UserCreationForm):
    # this will add additional fields to the built-in User Creation Form
    school = forms.ChoiceField(choices=SCHOOL_NAMES,)
    school_program = forms.ChoiceField(choices=PROGRAM_CHOICES, )
    industry_of_interest = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=INDUSTRY_CHOICES, )
    school_of_interest = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SCHOOL_NAMES, )
    name = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('name', 'username', 'password1', 'password2', 'school', 'school_program', 'industry_of_interest', 'school_of_interest')


MISCLASSIFY_SELECTION = (
    ('education_program', 'Education Program'),
    ('job_industry', 'Job Industry'),
)


class MisClassify(forms.Form):
    first_selection = forms.ChoiceField(choices=MISCLASSIFY_SELECTION, )


class InitialEduClassify(forms.Form):
    pass


class JobMisClassify(forms.Form):
    # edu_correct = forms.ChoiceField(choices=MISCLASSIFY_SELECTION,)

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(JobMisClassify, self).__init__(*args, **kwargs)
        for i, job in enumerate(extra):
            self.fields['custom_%s' % i] = forms.ChoiceField(label=job, choices=INDUSTRY_CHOICES, required=False)
            # self.fields['custom_%s' % i] = forms.CharField(label=job, max_length=250, required=False)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)

        # super(EducationMisClassify, self).__init__(*args, **kwargs)
        # for i in range(0, n):
        #     self.fields["edu_correct %d" % i] = forms.ChoiceField(choices=MISCLASSIFY_SELECTION,)

    # edu_correct = forms.CharField(max_length=250)


class EducationMisClassify(forms.Form):
    edu_correct = forms.ChoiceField(choices=MISCLASSIFY_SELECTION,)
    # job_selection = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=(('job1', 'Default Job 1'),))










#class AuthorForm(ModelForm):
#    class Meta:
#        model = Author
#        fields = ['name', 'title', 'birth_date']
#
#
#class BookForm(ModelForm):
#    class Meta:
#        model = Book
#        fields = ['name', 'authors']
#
#
#class MultiWidgetBasic(forms.widgets.MultiWidget):
#    def __init__(self, attrs=None):
#        widgets = [forms.TextInput(),
#                   forms.TextInput()]
#        super(MultiWidgetBasic, self).__init__(widgets, attrs)
#
#    def decompress(self, value):
#        if value:
#            return pickle.loads(value)
#        else:
#            return ['', '']
#
#
#class MultiExampleField(forms.fields.MultiValueField):
#    widget = MultiWidgetBasic
#
#    def __init__(self, *args, **kwargs):
#        list_fields = [forms.fields.CharField(max_length=31),
#                       forms.fields.CharField(max_length=31)]
#        super(MultiExampleField, self).__init__(list_fields, *args, **kwargs)
#
#    def compress(self, values):
#        return pickle.dumps(values)
#
#
#class FormForm(forms.Form):
#    a = forms.BooleanField()
#    b = forms.CharField(max_length=32)
#    c = forms.CharField(max_length=32, widget=forms.widgets.Textarea())
#    d = forms.CharField(max_length=32, widget=forms.widgets.SplitDateTimeWidget())
#    e = forms.CharField(max_length=32, widget=MultiWidgetBasic())
#    f = MultiExampleField()
#














# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')
#
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('bio', 'location', 'birth_date')
