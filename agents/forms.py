from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from leads.models import Agent, User
from crispy_forms.helper import FormHelper


USER = get_user_model()


class AgentCreateModelForm(forms.ModelForm):
    class Meta:
        model = USER
        fields = (
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'position',
            'photo',
            'email',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

        self.fields['photo'].label = 'Profile photo'
        self.fields["username"].help_text = ''


# class AgentUpdateModelForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'first_name',
#             'last_name',
#             'position',
#             'email',
#         )
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         self.helper = FormHelper(self)
#         self.helper.form_show_labels = False

#         self.fields['username'].help_text = ""
#         self.fields['first_name'].label = ""
#         self.fields['last_name'].label = ""


class AgentProfileUpdateModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'photo',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        
        self.fields['photo'].label = 'Profile photo'


class CustomAgentUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username", 
            "first_name", 
            "last_name", 
            "position", 
            "photo",
            "email",
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        
        self.fields['photo'].label = 'Profile photo'
        self.fields["username"].help_text = ''
