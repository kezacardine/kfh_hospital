from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    path('patient/<str:patient_id>/', views.patient_detail, name='patient_detail'),
    path('generate-sample-data/', views.generate_sample_data, name='generate_sample_data'),
]
