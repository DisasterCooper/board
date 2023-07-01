from django.urls import path

from . import views

#  /user/

app_name = "user"

urlpatterns = [
    path('<int:user_id>/', views.RedactUser.as_view(), name='redact_user'),
    ]
