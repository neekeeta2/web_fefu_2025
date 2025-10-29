from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('instructors/', views.instructor_list, name='instructor_list'),
    path('courses/', views.course_list, name='course_list'),
    path('enrollment/<int:course_id>/', views.enrollment_view, name='enrollment'),
     path('students/', views.student_list, name='student_list'), 
     
]