# urls.py
from django.urls import path, include
from .views import UserProfile

urlpatterns = [
    path('user/profile/', UserProfile.as_view(), name='user_home'),
    path('messaging/', include('messaging.urls'))
]
