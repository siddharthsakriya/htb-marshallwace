from django.urls import path
from .views import RegisterView, LoginView, LogoutView, echo_view

urlpatterns = [
    # ===== echo (for testing connections) =====
    path('echo/', echo_view, name='echo'),
    
    # ===== API endpoints =====
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
