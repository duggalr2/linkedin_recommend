from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm


INDUSTRY_CHOICES = (
    ('software', 'software'),
    ('entrepreneur', 'entrepreneur'),
    ('data_science', 'data science'),
    ('research', 'research'),
    ('finance', 'finance'),
    ('medicine', 'medicine'),
)

SCHOOL_NAMES = (
    ('uoft', 'University of Toronto'),
    ('harvard', 'Harvard'),
    ('MIT', 'MIT'),
    ('waterloo', 'Univertsity of Waterloo'),
)

PROGRAM_CHOICES = (
    ('computer_science', 'Computer Science'),
    ('commerce', 'Commerce'),
    ('medicine_lifesci', 'Medicine/Lifesci/Healthsci'),
    ('math_statistics', 'Math/Statistics/Physics'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One To One Field explains the One to One link
    name = models.CharField(max_length=250, default='name')
    current_school = models.CharField(max_length=100, choices=SCHOOL_NAMES, default='uoft')
    school_program = models.CharField(max_length=100, choices=PROGRAM_CHOICES, default='computer_science')
    school_of_interest = models.CharField(max_length=100, choices=SCHOOL_NAMES, default='uoft')
    industry_of_interest = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='software')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


#TITLE_CHOICES = (
#    ('MR', 'Mr.'),
#    ('MRS', 'Mrs.'),
#    ('MS', 'Ms.'),
#)
#
#
#class Author(models.Model):
#    name = models.CharField(max_length=100)
#    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
#    birth_date = models.DateField(blank=True, null=True)
#
#    def __str__(self):
#        return self.name
#
#
#class Book(models.Model):
#    name = models.CharField(max_length=100)
#    authors = models.ManyToManyField(Author)

