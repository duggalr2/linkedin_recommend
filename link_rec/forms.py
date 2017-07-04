from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import Profile
from .models import Author, Book, Profile
from django.forms import ModelForm, MultiValueField, CharField
from django.core.validators import RegexValidator
import pickle


INDUSTRY_CHOICES = (
    ('software', 'software'),
    ('entrepreneur', 'entrepreneur'),
    ('research', 'research'),
    ('finance', 'finance'),
)

SCHOOL_NAMES = (
    ('uoft', 'university of toronto'),
    ('harvard', 'Harvard'),
    ('MIT', 'MIT'),
    ('waterloo', 'Univertsity of Waterloo'),
)

PROGRAM_CHOICES = (
    ('computer_science', 'computer_science'),
    ('commerce', 'commerce'),
    ('medicine_lifesci', 'medicine_lifesci'),
    ('math', 'math'),
)


class SignUpForm(UserCreationForm):
    # this will add additional fields to the built-in User Creation Form
    school = forms.ChoiceField(choices=SCHOOL_NAMES,)
    school_program = forms.ChoiceField(choices=PROGRAM_CHOICES, )
    industry_interest = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=INDUSTRY_CHOICES, )
    # url_of_interest =


    class Meta:
        model = User
        fields = ('name', 'username', 'password1', 'password2', 'school', 'school_program', 'industry_interest')


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']


class MultiWidgetBasic(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(),
                   forms.TextInput()]
        super(MultiWidgetBasic, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return pickle.loads(value)
        else:
            return ['', '']


class MultiExampleField(forms.fields.MultiValueField):
    widget = MultiWidgetBasic

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=31),
                       forms.fields.CharField(max_length=31)]
        super(MultiExampleField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        return pickle.dumps(values)


class FormForm(forms.Form):
    a = forms.BooleanField()
    b = forms.CharField(max_length=32)
    c = forms.CharField(max_length=32, widget=forms.widgets.Textarea())
    d = forms.CharField(max_length=32, widget=forms.widgets.SplitDateTimeWidget())
    e = forms.CharField(max_length=32, widget=MultiWidgetBasic())
    f = MultiExampleField()















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