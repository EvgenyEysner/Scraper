from django.urls import path
from .views import IndexView, ApartmentDeleteView, ApartmentDetailView, ApartmentUpdateView, ImageDeleteView, ImageUpdateView, apartments_render_pdf_view, ProfileUpdateView, UserProfile

app_name = 'apartments'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('apartment/<int:pk>/delete', ApartmentDeleteView.as_view(), name='delete'),
    path('image/<int:pk>/delete', ImageDeleteView.as_view(), name='delete-image'),
    path('apartment/<int:pk>/details', ApartmentDetailView.as_view(), name='apartment'),
    path('apartment/<int:pk>/update', ApartmentUpdateView.as_view(), name='update'),
    path('image/<int:pk>/update', ImageUpdateView.as_view(), name='update-image'),
    path('apartment/<int:pk>/create_pdf', apartments_render_pdf_view, name='create_pdf'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('<int:pk>/edit', ProfileUpdateView.as_view(), name='edit'),
    ]