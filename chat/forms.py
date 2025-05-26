from django import forms
from django.contrib.auth.models import User
from .models import Room

class RoomForm(forms.ModelForm):
    allowed_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Room
        fields = ['name', 'allowed_users']
