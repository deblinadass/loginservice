
from rest_framework import serializers
from hstloginservice.model.hstloginmodel import Userrole, UserRoleAuthorisation, Login

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userrole
        fields = ('id','operations','usergroupid','userrole')
        ordering = ['id']
        
class UserRoleAuthorisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleAuthorisation
        fields = ('tabsectionname','tabsectionfieldsauthorisation')
        ordering = ['tabsectionname']

class UserRoleURLAuthorisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleAuthorisation
        fields = ('userroles','taburls')

class LoginViaGripSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='gripid')
    emails = serializers.CharField(source='useremail')
    ruisnaam = serializers.CharField(source='username')
    
    class Meta:
        model = Login
        fields = ('id','emails','ruisnaam','updateddate')
    
