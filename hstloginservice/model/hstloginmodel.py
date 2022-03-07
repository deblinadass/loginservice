# encoding: UTF-8

from django.db import models
from django.utils import timezone
from django_bleach.models import BleachField
from django.contrib.postgres.fields import ArrayField


class LoginManager(models.Manager):
    def getmstusergroup(self, username):
        return self.get(username__iexact = username, useractive = 1)
    def updatelastlogintimestamp(self, userEmail):
        return self.filter(useremail = userEmail).update(userlastlogin = timezone.now())
    def getUser(self, pk):
        return self.get(gripid=pk)

class Login(models.Model):
    #id = models.AutoField(primary_key=True)
    useremail = models.EmailField()
    userlastlogin = models.DateTimeField(blank=True)
    useractive = models.IntegerField()
    usergroup = models.CharField(verbose_name=u'usergroup', max_length=10)
    username = models.CharField(verbose_name=u'username', max_length=10)
    createddate = models.DateTimeField(default = timezone.now)
    updateddate = models.DateTimeField(blank=True)
    gripid = models.CharField(max_length=255)
    
    def __str__(self):
        return '%s' % (self.usergroup)
    class Meta:
        db_table = "login"
    objects = LoginManager()

class UserroleManager(models.Manager):
    def getuserrole(self, usergroup):
        return self.get_queryset().filter(usergroupid = usergroup)

class Userrole(models.Model):
    operations = models.CharField(max_length=100)
    usergroupid = models.CharField(max_length=100)
    userrole = models.CharField(max_length=100)

    class Meta:
        db_table = "userrole"
    objects = UserroleManager()

class UserRoleAuthorisationManager(models.Manager):
    def gettabsectiondetails(self, tabname, userrole):
        return self.get_queryset().filter(tabname=tabname, userroles__contains=[userrole])
    def getUserRoleUrlsdetail(self, userrole):
        return self.get_queryset().filter(userroles__contains=[userrole])
    
class UserRoleAuthorisation(models.Model):
    tabname = BleachField(max_length=100)
    userroles = ArrayField(BleachField(max_length=255, blank=True, null=True))
    tabsectionname = BleachField(max_length=100)
    tabsectionfieldsauthorisation = BleachField(max_length=500)
    taburls = ArrayField(BleachField(max_length=255, blank=True, null=True))

    class Meta:
        db_table = "userroleauthorisation"
    objects = UserRoleAuthorisationManager()