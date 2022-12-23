from django import forms

from .models import User, UserProfile
from .validators import allow_only_image_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "phone_number"]

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if confirm_password != password:
            raise forms.ValidationError("password does not match !!!")


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "start typing...", "required": "required"}))
    profile_picture = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_only_image_validator]
    )
    cover_photo = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_only_image_validator]
    )
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "cover_photo",
            "address",
            "country",
            "state",
            "city",
            "pin_code",
            "latitude",
            "longitude",
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == "longitude" or field == "latitude":
                self.fields[field].widget.attrs["readonly"] = "readonly"
