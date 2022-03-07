"""hstloginservice URL Configuration"""
from django.urls import path
from hstloginservice.service.hstloginservice import login, refresh, checkUserRole, getPageSectionAuthorisation, getUserURLAuthorisation
from hstloginservice.service.hstloginviagripservice import LoginViaGrip, UpdateViaGrip, DeleteViaGrip


urlpatterns = [
    path('loginservice/login', login),
    path('loginservice/refresh', refresh),
    path('loginservice/checkuserrole/<str:useraction>/', checkUserRole),
    path('loginservice/getauthorisations/<str:page>/', getPageSectionAuthorisation),
    path('loginservice/getauthorisationsurls/<str:userrole>/', getUserURLAuthorisation),
    path('createuserviagrip/', LoginViaGrip),
    path('updateuserviagrip/', UpdateViaGrip),
    path('deleteuserviagrip/<str:pk>', DeleteViaGrip),
]
