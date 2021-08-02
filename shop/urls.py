from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'shop'

urlpatterns = [
    # path('',views.home,name='home'),

    path('', views.product_list, name='product_list'),
    # path('', views.login,name='login'),
    path('<slug:category_slug>/', views.product_list, 
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
    path('signup', views.CustomerSignUpView,name='signup'),
    path('signup/signup_successful', views.signup_successful, name='signup_successful'),
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name='password_reset'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/reset_email_sent.html"),
         name='reset_email_sent'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/reset_confirm.html"),
         name='reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/reset_complete.html"),
         name='reset_complete'),
    path('accounts/password_change/',
         auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"),
         name='password_change'),
    path('accounts/password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_changed.html"),
         name='password_changed'),
]