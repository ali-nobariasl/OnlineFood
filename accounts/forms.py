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
    
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}))
    cover_photo = forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}))
    
    class Meta:
        model= UserProfile
        fields = ['profile_picture', 'cover_photo','address_line_1','address_line_2','country','state','city',
                  'pin_code', 'longitude','longitude' ]