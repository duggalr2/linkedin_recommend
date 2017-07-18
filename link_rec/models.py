from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    ('uoft', 'University of Toronto'),
    ('harvard', 'Harvard University'),
    ('mit', 'Massachusetts Institute of Technology'),
    ('waterloo', 'Univertsity of Waterloo'),
    ('stanford', 'Stanford University'),
    ('western', 'Western University'),
    ('ucb', 'University of California, Berkeley'),
    ('caltech', 'Caltech'),
    ('cornell', 'Cornell University'),
    ('oxford', 'Oxford University'),
    ('cmu', 'Carnegie Mellon University'),
    ('upenn', 'University of Pennsylvania'),
    ('cambridge', 'University of Cambridge'),
    ('ucla', 'University of California, Los Angeles'),
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


# class ParsedProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=250)
#     header = models.CharField(max_length=500, null=True)
#     url = models.CharField(max_length=500)
#     school = models.CharField(max_length=500, null=True)
#     school_program = models.CharField(max_length=500, null=True)
#
#
# class JobTitle(models.Model):
#     profile = models.ForeignKey(ParsedProfile, on_delete=models.CASCADE)
#     job = models.CharField(max_length=500, null=True)
#
#
# class Location(models.Model):
#     profile = models.ForeignKey(ParsedProfile, on_delete=models.CASCADE)
#     loc = models.CharField(max_length=500, default=None)


# Below is All The Profiles that were originally in DB and added new ones by User
# Initial Profiles, only 2000 were in DB (mainly SE/CS focused)


class AllParsedProfile(models.Model):
    name = models.CharField(max_length=250)
    header = models.CharField(max_length=500, null=True)
    url = models.CharField(max_length=500)
    school = models.CharField(max_length=500, null=True)
    school_program = models.CharField(max_length=500, null=True)
    # url = models.CharField(max_length=500)


class AllJobTitle(models.Model):
    profile = models.ForeignKey(AllParsedProfile, on_delete=models.CASCADE)
    job = models.CharField(max_length=500, null=True)
    # job2 = models.CharField(max_length=500, null=True)
    # job3 = models.CharField(max_length=500, null=True)
    # job4 = models.CharField(max_length=500, null=True)
    # job5 = models.CharField(max_length=500, null=True)
    # job6 = models.CharField(max_length=500, null=True)
    # job7 = models.CharField(max_length=500, null=True)
    # job8 = models.CharField(max_length=500, null=True)
    # job9 = models.CharField(max_length=500, null=True)


class AllLocation(models.Model):
    profile = models.ForeignKey(AllParsedProfile, on_delete=models.CASCADE)
    loc = models.CharField(max_length=500, default=None)
    # profile_id = models.ForeignKey(AllParsedProfile, on_delete=models.CASCADE)
    # loc2 = models.CharField(max_length=500, null=True)
    # loc3 = models.CharField(max_length=500, null=True)
    # loc4 = models.CharField(max_length=500, null=True)
    # loc5 = models.CharField(max_length=500, null=True)
    # loc6 = models.CharField(max_length=500, null=True)
    # loc7 = models.CharField(max_length=500, null=True)
    # loc8 = models.CharField(max_length=500, null=True)
    # loc9 = models.CharField(max_length=500, null=True)
