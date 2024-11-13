from django.urls import path

from .views import RegistrationView

urlpatterns = [
    path('v1/registration/',RegistrationView.as_view(), name='registration'),
    # path('v1/refresh/',),
    # path('v1/authorization/',)
]