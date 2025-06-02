from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment,Booking

class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post    
        fields = ('body', )
        
        
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }
        
class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label="Username"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control'}),
        label="Email"
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password and Confirm Password do not match')
        return cleaned_data

class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )

# forms.py
# yourapp/forms.py

class BookingForm(forms.ModelForm):
    patient_name = forms.CharField(label="Name and family patient", max_length=100,
                                   widget=forms.TextInput(attrs={'class': 'input-class', 'placeholder': 'Name and family'}))
    phone_number = forms.CharField(label="Phone number", max_length=15,
                                   widget=forms.TextInput(attrs={'class': 'input-class', 'placeholder': 'Phone number'}))

    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'input-class'
        }),
        label="Date"
    )

    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'input-class'
        }),
        label="Time"
    )

    class Meta:
        model = Booking
        fields = ['patient_name', 'phone_number', 'doctor', 'date', 'time', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'input-class', 'placeholder': 'Description'}),
            'doctor': forms.Select(attrs={'class': 'input-class'}),
        }
