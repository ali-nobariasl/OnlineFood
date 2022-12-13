from django import forms

from .models import User , UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields =['username', 'first_name', 'last_name', 'email', 'password', 'phone_number']
   
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            raise forms.ValidationError( "password does not match !!!")
        
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model= UserProfile
        fields = "__all__"