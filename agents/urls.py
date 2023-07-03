from django.urls import path
from .views import (AgentListView, AgentCreateView, AgentDetailView, 
                AgentDeleteView, AgentUpdateView, AgentProfileView, 
                AgentProfileUpdateView, )


app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent-list'),
    path('create/', AgentCreateView.as_view(), name='agent-create'),
    path('<int:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    path('<int:pk>/profile/', AgentProfileView.as_view(), name='agent-profile'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('<int:pk>/profile/update/', AgentProfileUpdateView.as_view(), name='profile-update'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='agent-delete'),
]