from django.urls import path
from django.contrib.auth import views as auth_views
from apps.users.views import logout_view, register, profile_view, manage_addresses, add_address, edit_address, delete_address

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', register, name='register'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='users/login.html',
            redirect_authenticated_user=True,
        ),
        name='login'
    ),
    path('logout/', logout_view, name='logout'),
    
    # User Profile
    path('profile/', profile_view, name='profile'),
    
    # Address Management
    path('addresses/', manage_addresses, name='manage_addresses'),
    path('addresses/add/', add_address, name='add_address'),
    path('addresses/<int:address_id>/edit/', edit_address, name='edit_address'),
    path('addresses/<int:address_id>/delete/', delete_address, name='delete_address'),
    
    # Password Reset Flow
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            email_template_name='emails/auth/password_reset_email.txt',
            subject_template_name='emails/auth/password_reset_subject.txt',
            success_url='/auth/password-reset/done/',
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url='/auth/password-reset-complete/',
        ),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]