from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile, Feedback, Student

class FeedbackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        max_length=200,
        label='Тема сообщения',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='Текст сообщения',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.strip()) < 2:
            raise ValidationError("Имя должно содержать минимум 2 символа")
        return name.strip()
    
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message.strip()) < 10:
            raise ValidationError("Сообщение должно содержать минимум 10 символов")
        return message.strip()


class StudentRegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'faculty']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Введите вашу фамилию'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия', 
            'email': 'Email',
            'birth_date': 'Дата рождения',
            'faculty': 'Факультет',
        }
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name.strip()) < 2:
            raise ValidationError("Имя должно содержать минимум 2 символа")
        return first_name.strip()
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name.strip()) < 2:
            raise ValidationError("Фамилия должна содержать минимум 2 символа")
        return last_name.strip()
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 8:
            raise ValidationError("Пароль должен содержать минимум 8 символов")
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают")
        
        return cleaned_data

# Оставляем старую форму для обратной совместимости, но не используем ее
RegistrationForm = StudentRegistrationForm


# class RegistrationForm(forms.Form):
#     username = forms.CharField(
#         max_length=50,
#         label='Логин',
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#     email = forms.EmailField(
#         label='Email',
#         widget=forms.EmailInput(attrs={'class': 'form-control'})
#     )
#     password = forms.CharField(
#         label='Пароль',
#         widget=forms.PasswordInput(attrs={'class': 'form-control'})
#     )
#     password_confirm = forms.CharField(
#         label='Подтверждение пароля',
#         widget=forms.PasswordInput(attrs={'class': 'form-control'})
#     )
    
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if UserProfile.objects.filter(username=username).exists():
#             raise ValidationError("Пользователь с таким логином уже существует")
#         return username
    
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if UserProfile.objects.filter(email=email).exists():
#             raise ValidationError("Пользователь с таким email уже существует")
#         return email
    
#     def clean_password(self):
#         password = self.cleaned_data['password']
#         if len(password) < 8:
#             raise ValidationError("Пароль должен содержать минимум 8 символов")
#         return password
    
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         password_confirm = cleaned_data.get('password_confirm')
        
#         if password and password_confirm and password != password_confirm:
#             raise ValidationError("Пароли не совпадают")
        
#         return cleaned_data
    


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            try:
                user = UserProfile.objects.get(username=username)
                if user.password != password:  # В реальном проекте используйте check_password!
                    raise ValidationError("Неверный логин или пароль")
            except UserProfile.DoesNotExist:
                raise ValidationError("Неверный логин или пароль")
        
        return cleaned_data