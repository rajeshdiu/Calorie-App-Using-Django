from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signupPage, name='signupPage'),
    path('logoutPage/', logoutPage, name='logoutPage'),
    path('mySigninPage/', mySigninPage, name='mySigninPage'),
    path('ProfilePage/', ProfilePage, name='ProfilePage'),
    path('activate/<uid64>/<token>', activate,name='activate'),
    path('forget_pass/', forget_pass, name='forget_pass'),
    path('update_pass/', update_pass, name='update_pass'),
    path('add_consumed_calories/', add_consumed_calories, name='add_consumed_calories'),
    path('calorie_summary/', calorie_summary, name='calorie_summary'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('dashboardPage/', dashboardPage, name='dashboardPage'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)