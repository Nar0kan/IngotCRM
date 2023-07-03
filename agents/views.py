from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail
from leads.models import Agent, User
from .mixins import OrganisorRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AgentCreateModelForm, AgentProfileUpdateModelForm, CustomAgentUpdateForm
from secrets import randbelow
from crispy_forms.helper import FormHelper


class AgentListView(OrganisorRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    context_object_name = "agents"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentCreateModelForm

    def get_success_url(self) -> str:
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        
        password = ''.join([str(randbelow(10000)) for i in range(20)])
        user.set_password(password)
        user.save()

        Agent.objects.create(
            user = user,
            organisation=self.request.user.userprofile,
        )

        send_mail(
            from_email=f"{self.request.user.userprofile}",
            recipient_list=[user.email],
            subject="You are invited to be an Agent",
            message=f"You were added as an agent on Ingot CRM.\n\n\
                Log in form: https://127.0.0.1:8000/login \n\n\
                User this password to log in the system: {password}."
        )

        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganisorRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = CustomAgentUpdateForm
    context_object_name = "agent"

    def get_success_url(self) -> str:
        return reverse("agents:agent-detail", kwargs={"pk": self.get_object().id})

    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get('pk')
        agent = Agent.objects.get(id=pk)
        initial['username'] = agent.user.username
        initial['first_name'] = agent.user.first_name
        initial['last_name'] = agent.user.last_name
        initial['position'] = agent.user.position
        initial['photo'] = agent.user.photo
        initial['email'] = agent.user.email
      
        return initial

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.user.username = form.cleaned_data['username']
        agent.user.first_name = form.cleaned_data['first_name']
        agent.user.last_name = form.cleaned_data['last_name']
        agent.user.position = form.cleaned_data['position']
        agent.user.photo = form.cleaned_data['photo']
        agent.user.email = form.cleaned_data['email']
        agent.save()
        agent.user.save()

        return super(AgentUpdateView, self).form_valid(form)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        agent = Agent.objects.filter(id=pk)
        return agent
    

class AgentDeleteView(OrganisorRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self) -> str:
        return reverse("agents:agent-list")


class AgentProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_profile.html"
    context_object_name = "agent"
    
    def get_queryset(self):
        agent = self.request.user.id
        return User.objects.filter(id=agent)


class AgentProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_profile_update.html"
    form_class = AgentProfileUpdateModelForm
    context_object_name = "agent"
    
    def get_queryset(self):
        agent = self.request.user.id
        queryset = User.objects.filter(id=agent)
        print(queryset)
        return queryset
    
    def form_valid(self, form):
        return super(AgentProfileUpdateView, self).form_valid(form)

    def get_success_url(self) -> str:
        return reverse("agents:agent-profile", kwargs={"pk": self.get_object().id})
