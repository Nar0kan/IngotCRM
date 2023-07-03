from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, DeleteView, UpdateView, FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView,
)

from agents.mixins import OrganisorRequiredMixin

from .models import (
    Lead, Agent, Category, Document,
)
from .forms import (
    LeadModelForm, CustomUserCreationForm, AssignAgentForm,
    LeadCategoryUpdateForm, UploadDocumentModelForm,
    LeadCommentForm, CustomAuthenticationForm,
    CustomPasswordChangeForm, CustomPasswordResetForm,
    CustomSetPasswordForm, 
)
from .filters import DocumentFilter


DOCUMENTS_PER_PAGE = 5
LEADS_PER_PAGE = 5


def Error404View(request, exception):
    return render(request, '404.html', {})


class LandingPageView(TemplateView):
    template_name = "landing.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class PricingPageView(TemplateView):
    template_name = "pricing.html"


class LeadListView(LoginRequiredMixin, ListView):
    queryset = Lead.objects.all()
    template_name = "lead_list.html"
    context_object_name = "leads"

    paginate_by = LEADS_PER_PAGE

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            queryset = Lead.objects.filter(agent__user=user)
        
        ordered_qs = queryset.order_by("-date_added")

        return ordered_qs
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        
        return context


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "lead_details.html"
    queryset = Lead.objects.all()
    form = LeadCommentForm
    context_object_name = "lead"

    def post(self, request, *args, **kwargs):
        form = LeadCommentForm(request.POST)

        if form.is_valid():
            lead = self.get_object()
            form.instance.author = request.user
            form.instance.lead = lead #Lead.objects.get(id=self.kwargs['pk'])
            form.save()

            return redirect(reverse("leads:lead-detail", kwargs={"pk": lead.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        return context


class LeadCreateView(LoginRequiredMixin, CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm

    def get_form(self, form_class=LeadModelForm):
        form = super().get_form(form_class)
        user = self.request.user

        if user.is_organisor:
            form.fields['agent'].queryset = Agent.objects.filter(organisation=user.userprofile)
            form.fields['category'].queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            form.fields['category'].queryset = Category.objects.filter(organisation=user.agent.organisation)
            form.fields['agent'].queryset = Agent.objects.filter(user=user)

        return form

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        user = self.request.user

        if user.is_organisor:
            lead.organisation = user.userprofile
        else:
            lead.organisation = user.agent.organisation
        
        lead.save()
        
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )

        form.instance.organisation = lead.organisation
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = Lead.objects.filter(agent__user=user)
        
        return queryset
    
    def get_form(self, form_class=LeadModelForm):
        form = super().get_form(form_class)
        user = self.request.user

        if user.is_organisor:
            form.fields['agent'].queryset = Agent.objects.filter(organisation=user.userprofile)
            form.fields['category'].queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            form.fields['category'].queryset = Category.objects.filter(organisation=user.agent.organisation)
            form.fields['agent'].queryset = Agent.objects.filter(user=user)

        return form
    
    def form_valid(self, form):
        lead = form.save(commit=False)
        user = self.request.user

        if user.is_organisor:
            lead.organisation = user.userprofile
        else:
            lead.organisation = user.agent.organisation
        
        lead.save()

        form.instance.organisation = lead.organisation
        return super(LeadUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("leads:lead-list")


class LeadDeleteView(OrganisorRequiredMixin, DeleteView):
    template_name = "lead_delete.html"

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")


class AssignAgentView(OrganisorRequiredMixin, FormView):
    template_name = "assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()

        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            leads = Lead.objects.filter(organisation=user.userprofile)
        else:
            leads = Lead.objects.filter(organisation=user.agent.organisation)

        context.update({
            "leads": leads,
        })

        return context
    
    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        
        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "category_detail.html"
    context_object_name = "category"
    
    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = Lead.objects.filter(agent__user=user)
        
        return queryset
    
    def get_form(self, form_class=LeadCategoryUpdateForm):
        form = super().get_form(form_class)
        user = self.request.user

        if user.is_organisor:
            form.fields['category'].queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            form.fields['category'].queryset = Category.objects.filter(organisation=user.agent.organisation)

        return form
    
    def form_valid(self, form):
        category = form.save(commit=False)
        user = self.request.user

        if user.is_organisor:
            category.organisation = user.userprofile
        else:
            category.organisation = user.agent.organisation
        
        category.save()

        form.instance.organisation = category.organisation
        return super(LeadCategoryUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})


class SignupView(CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse("login")


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = CustomAuthenticationForm

    def get_success_url(self) -> str:
        return reverse("leads:lead-list")


class CustomPasswordChangeView(PasswordChangeView, LoginRequiredMixin):
    template_name = "registration/change_password.html"
    form_class = CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "registration/password_reset_email.html"
    #success_url = reverse_lazy("password_reset_done")
    template_name = "registration/password_reset_form.html"
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("password_reset_complete")
    template_name = "registration/password_reset_confirm.html"


class DocumentListView(LoginRequiredMixin, ListView):
    #queryset = Document.objects.all()
    template_name = "document_list.html"
    context_object_name = "documents"

    paginate_by = DOCUMENTS_PER_PAGE


    def get_queryset(self):
        #queryset = super().get_queryset()
        user = self.request.user

        if user.is_organisor:
            queryset = Document.objects.filter(organisation=user.userprofile)
        else:
            queryset = Document.objects.filter(organisation=user.agent.organisation, is_secret=False)
        
        self.filterset = DocumentFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        return context


class DocumentDetailView(LoginRequiredMixin, DetailView):
    template_name = "document_detail.html"
    context_object_name = "document"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Document.objects.filter(organisation=user.userprofile)
        else:
            queryset = Document.objects.filter(organisation=user.agent.organisation)
        
        return queryset


class DocumentUploadView(LoginRequiredMixin, CreateView):
    template_name = "upload_document.html"
    form_class = UploadDocumentModelForm

    def get_success_url(self) -> str:
        return reverse("leads:document-list")

    def get_form(self, form_class=UploadDocumentModelForm):
        form = super().get_form(form_class)
        user = self.request.user

        if user.is_organisor:
            form.fields['lead'].queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            form.fields['lead'].queryset = Lead.objects.filter(organisation=user.agent.organisation)

        return form
    
    def form_valid(self, form):
        document = form.save(commit=False)
        user = self.request.user

        if user.is_organisor:
            document.organisation = user.userprofile
        else:
            document.organisation = user.agent.organisation
        
        document.save()
        form.instance.organisation = document.organisation
        return super(DocumentUploadView, self).form_valid(form)


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "document_update.html"
    form_class = UploadDocumentModelForm

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Document.objects.filter(organisation=user.userprofile)
        else:
            queryset = Document.objects.filter(organisation=user.agent.organisation)
        
        return queryset
    
    def get_form(self, form_class=UploadDocumentModelForm):
        form = super().get_form(form_class)
        user = self.request.user

        if user.is_organisor:
            form.fields['lead'].queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            form.fields['lead'].queryset = Lead.objects.filter(organisation=user.agent.organisation)

        return form
    
    def form_valid(self, form):
        document = form.save(commit=False)
        user = self.request.user

        if user.is_organisor:
            document.organisation = user.userprofile
        else:
            document.organisation = user.agent.organisation
        
        document.save()
        form.instance.organisation = document.organisation
        return super(DocumentUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("leads:document-detail", kwargs={"pk": self.get_object().id})


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = "document_delete.html"
    context_object_name = "document"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        file_field = self.object.file
        if file_field:
            file_field.delete()
        return super(DocumentDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("leads:document-list")


def DonateView(request):
    context = {'client_id': settings.PAYPAL_RECEIVER_ID}
    return render(request, 'donate.html', context)


# import uuid

# from django.contrib import messages
# from paypal.standard.forms import PayPalPaymentsForm

# from leads.models import Rights, Order


# def OrderView(request):
#     user = self.request.user

#     if not user.is_organisor:
#         return redirect('landing')

#     host = request.get_host()

#     paypal_dict = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': '20.00',
#         'item_name': 'Subscription order',
#         'invoice': str(uuid.uuid4()),
#         'currency_code': 'USD',
#         'notify_url': f'http://{host}{reverse("paypal-ipn")}',
#         'return_url': f'http://{host}{reverse("leads:paypal-return")}',
#         'cancel_return': f'http://{host}{reverse("leads:paypal-cancel")}',
#     }
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     context = {'form': form}
#     return render(request, 'order_page.html', context)


# def paypal_return(request):
#     messages.success(request, 'You have successfully made a payment.')
#     return redirect('leads:order_page')


# def paypal_cancel(request):
#     messages.error(request, 'Your order has been cancelled!')
#     return redirect('leads:order_page')
