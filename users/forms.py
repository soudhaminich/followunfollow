from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Profile
import os
from ckeditor.widgets import CKEditorWidget


class PasswordReset(PasswordResetForm):
    email = forms.EmailField()

    def clean_email(self):
        username_email = self.cleaned_data['email']
        email_match = User.objects.filter(email=username_email).count()
        if email_match == 0:
            raise forms.ValidationError(
                'This is not valid registered Email Id. !!!')
        return username_email


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        # print(self.cleaned_data['username'])
        username = self.cleaned_data['username']
        match = User.objects.filter(email=username)
        if len(username) <= 3:
            raise forms.ValidationError("Username minimum length should be 4")
        if match.exists():
            raise forms.ValidationError('Username already taken')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        match = User.objects.filter(email=email)
        if match.exists():
            raise forms.ValidationError(
                'This email address is already in use.May be you can try login with your username !!!')
        return email


class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        # print(self.cleaned_data['username'])
        username = self.cleaned_data['username']
        match = User.objects.filter(email=username)
        if len(username) <= 3:
            raise forms.ValidationError("Username minimum length should be 4")
        if match.exists():
            raise forms.ValidationError('Username already taken')

        return username

    # def clean_email(self):
    #     email = self.cleaned_data['email']

    #     match = User.objects.filter(email=email)
    #     if match.exists():
    #         raise forms.ValidationError('This email address is already in use.')
    #     return email
        # try:
        #     match = User.objects.get(email=email)

        # except User.DoesNotExist:
        #     # return email
        #     # Unable to find a user, this is fine
        #     raise forms.ValidationError('This email address is already in use.')
        # return email

        # A user was found with this as a username, raise an error.


class ProfileUpdateForm(forms.ModelForm):
    dob = forms.DateField(label='Date Of Birth(Optional)',
                          widget=forms.DateInput(
                              attrs={
                                  'type': 'date',
                                  'class': 'form-control',
                                  "placeholder": "DOB"
                              }
                          ),
                          required=False
                          )
    fb_url = forms.URLField(label='Facebook', required=False)
    tw_url = forms.URLField(label='Twitter', required=False)
    lki_url = forms.URLField(label='Linked In', required=False)
    skillset = forms.CharField(label="Skill Set", help_text='Provide your skill sets(Ex: python,html))', widget=forms.TextInput(attrs={
        'placeholder': 'Enter your skill set(Ex: python,html)'}), required=False)
    # bio = forms.Textarea(label='Biography',
    #         widget=forms.DateInput(
    #             attrs={
    #                     "placeholder": "About yourself & experiences !!!"
    #                 }
    #             ),
    #             required=False
    #         )
    # skillset = forms.CharField(label='Skills',
    #         widget=forms.DateInput(
    #             attrs={
    #                     "placeholder": "Enter your skill set with separated by ,"
    #                 }
    #             ),
    #             required=False
    #         )

    class Meta:
        model = Profile

        fields = ['display_name', 'first_name', 'last_name', 'professional_summary', 'skillset',
                  'dob', 'image', 'fb_url', 'tw_url', 'lki_url', 'website', 'paypal_account', 'preferences']

       

    # def clean_image(self):

    #     image = self.cleaned_data['image']
    #     print(image)
    #     print(image.size)
    #     file_size = image.size
    #     limit_kb = 150
    #     ext = os.path.splitext(image.name)[1]
    #     valid_extensions = ['.jpg', '.png']
    #     if file_size > limit_kb * 1024:
    #         raise forms.ValidationError("Max size of file is %s KB" % limit_kb)
    #     if not ext.lower() in valid_extensions:
    #         raise forms.ValidationError('Unsupported file extension.')
    #     return image

        # file_size = image.size
        # print(file_size)

        # limit_kb = 3
        # ext = os.path.splitext(file.name)[1]
        # valid_extensions = ['.jpg', '.png']
        # return True


#     class Meta:
#          model = User
#         fields = ['username', 'password1']
class FollowForm(forms.Form):
    firstname = forms.CharField(required=False)
    lastname = forms.CharField(required=False)


class ForgotPassword(forms.Form):
    username_email = forms.CharField(label='Enter your Username or Email to reset the password',
                                     widget=forms.TextInput(
                                         attrs={
                                             "class": "form-control",
                                             "placeholder": "Username or Email"
                                         }
                                     )
                                     )

    def clean_username_email(self):
        username_email = self.cleaned_data['username_email']

        email_match = User.objects.filter(email=username_email).count()
        user_match = User.objects.filter(username=username_email).count()
        print(email_match)
        if email_match == 0 and user_match == 0:
            raise forms.ValidationError(
                'This is not valid registered Mail/Username !!!')
        return username_email
