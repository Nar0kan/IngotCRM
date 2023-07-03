from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from crispy_forms.helper import FormHelper
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from django.contrib.auth.forms import (
    UserCreationForm, UsernameField, AuthenticationForm, 
    PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)

from .models import Lead, User, Agent, Document, Category, LeadComment


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'description',
            'phone_number',
            'email',
            'photo',
            'category',
            'agent',
        )

    def __init__(self, *args, **kwargs):
        organisation = kwargs.pop('organisation', None)
        super().__init__(*args, **kwargs)
        
        if organisation:
            categories = Category.objects.filter(organisation=organisation)
            self.fields['category'].queryset = categories
            
            agents = Agent.objects.filter(organisation=organisation)
            self.fields['agent'].queryset = agents
        
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        #self.helper.label_class = "text-black dark:text-white bg-yellow-500"
        self.fields['photo'].label = 'Profile photo'


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", )
        field_classes = {"username": UsernameField, }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        self.helper = FormHelper(self)

        self.helper.form_show_labels = False

        self.fields["username"].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", )
        field_classes = {"username": UsernameField, }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

        self.fields['old_password'].help_text = ''
        self.fields['old_password'].label = ''
        self.fields['new_password1'].help_text = ''
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].help_text = ''
        self.fields['new_password2'].label = ''


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ("email", )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_show_labels = False


class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ("new_password1", "new_password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

        self.fields["new_password1"].help_text = ''


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )
    
    def __init__(self, *args, **kwargs):
        organisation = kwargs.pop('organisation', None)
        super().__init__(*args, **kwargs)
        
        if organisation:
            categories = Category.objects.filter(organisation=organisation)
            self.fields['category'].queryset = categories
        
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False


class UploadDocumentModelForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (
            'lead',
            'title',
            'description',
            'is_secret',
            'file',
            )

    def __init__(self, *args, **kwargs):
        organisation = kwargs.pop('organisation', None)
        super().__init__(*args, **kwargs)
        
        if organisation:
            leads = Lead.objects.filter(organisation=organisation)
            self.fields['leads'].queryset = leads
        
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.fields['file'].label = 'File'
        self.fields['file'].help_text = ''


class LeadCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        "class": "md-textarea form-control",
        "placeholder": "Write your comment here...",
        "rows": '4',
        }))
    text.label = ""

    class Meta:
        model = LeadComment
        fields = [
            "text",
        ]
