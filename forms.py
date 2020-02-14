from django import forms
from accounts.models import UserProfile, User


class UsersManageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name']