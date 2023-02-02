from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('me/', views.UserView.as_view(), name='user-detail'),
    #path('<uuid:pk>/', views.EventDetail.as_view(), name='event-detail'),
]
