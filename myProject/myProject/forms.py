from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from myApp.models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Custom_User
        fields = UserCreationForm.Meta.fields + ('display_name', 'email','city','user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].help_text = None

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Custom_User  
        fields = ['username', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'age', 'gender', 'height', 'weight', 'profile_picture']

class ConsumedCaloriesForm(forms.ModelForm):
    class Meta:
        model = ConsumedCalories
        fields = ['date', 'item_name', 'calorie_consumed']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
