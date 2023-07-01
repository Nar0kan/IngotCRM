from django.urls import path
from .views import (
    LeadDeleteView,
    LeadListView,
    LeadDetailView,
    LeadCreateView,
    LeadUpdateView,
    AssignAgentView,
    CategoryListView,
    CategoryDetailView,
    LeadCategoryUpdateView,
    DocumentListView,
    DocumentDetailView,
    DocumentUploadView,
    DocumentUpdateView,
    DocumentDeleteView,
    )

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign_agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('upload_document/', DocumentUploadView.as_view(), name='document-upload'),
    path('documents/<int:pk>/update/', DocumentUpdateView.as_view(), name='document-update'),
    path('documents/<int:pk>/delete/', DocumentDeleteView.as_view(), name='document-delete'),
]
