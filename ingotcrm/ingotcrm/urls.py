from django.contrib import admin
from django.urls import path, include
from leads.views import (
    LandingPageView, AboutPageView, 
    PricingPageView,  SignupView, 
    CustomLoginView, CustomPasswordChangeView, 
    CustomPasswordResetView, CustomPasswordResetConfirmView,
    DonateView, 
)

from django.conf import settings
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView,
    PasswordChangeDoneView
    )
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name="landing-page"),
    path('about/', AboutPageView.as_view(), name="about-page"),
    path('pricing/', PricingPageView.as_view(), name="pricing-page"),
    path('leads/', include('leads.urls', namespace="leads")),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', SignupView.as_view(), name='register'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('agents/', include('agents.urls', namespace='agents')),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('donate/', DonateView, name='donate'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('ecom/', include('ecom.urls')),
]

handler404 = 'leads.views.Error404View'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
