
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
  path('Signup/',ClientSignup.as_view()),
  path('login/',Login.as_view()),
  path('reset-password/send-link/', SendResetLinkView.as_view(), name='send_reset_link'),
  path('reset-password/validate-code/<str:signed_data>/', ValidateResetCodeView.as_view(), name='validate_reset_code'),
  path('reset-password/reset/<str:signed_data>/', ResetPasswordView.as_view(), name='reset_password'),

]