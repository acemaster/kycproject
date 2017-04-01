from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def getfilepath(instance, filename):
	return '/'.join(['blueprints',str(instance.user.id),filename,])

class UploadIdentification(models.Model):
    """
    Description: Identification
    """
    user = models.ForeignKey(User,null=True)
    identification_doc = models.FileField(upload_to=getfilepath)
    is_accepted = models.IntegerField(default=0)
    reason_to_move = models.TextField(null=True)
    reason_to_reject = models.TextField(null=True)
    applicant_score = models.CharField(max_length=200,null=True)
    class Meta:
        pass

class UserProfile(models.Model):
    """
    Description: User Profile
    """
    user = models.OneToOneField(User)
    organisation = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    dob = models.DateField()
    address = models.TextField(null=True)
    native_lang = models.CharField(max_length=200)
    lang = models.CharField(max_length=200)
    passport_no = models.TextField(max_length=200)
    def __unicode__(self):
    	return self.user.first_name


