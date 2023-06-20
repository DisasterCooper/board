"""
URL configuration for board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todolist.views_class import PostsList
from user.views import Registration, RedactUser, ShowUser

urlpatterns = [
    path('', PostsList.as_view()),
    path('admin/', admin.site.urls),
    # path('post1/', include('todolist.urls_func')),
    path('posts/', include(('todolist.urls_class', 'posts'), namespace='posts')),
    path('accounts/register', Registration.as_view(), name='registration'),
    path('user_redact/', RedactUser.as_view(), name='redact_user'),
    path('accounts/', include(('django.contrib.auth.urls', 'django.contrib.auth'), namespace='accounts')),
    path('captcha/', include('captcha.urls')),
    path('avatar/', include('avatar.urls')),
]
