from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Course, Enrollment, Instructor


class CustomAuthenticationForm(AuthenticationForm):
    """Кастомная форма входа с поддержкой email"""
    username = forms.CharField(
        label='Email или имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class BaseUserRegistrationForm(UserCreationForm):
    """Базовая форма регистрации пользователя"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user


class StudentRegistrationForm(BaseUserRegistrationForm):
    """Форма регистрации студента - УПРОЩЕННАЯ ВЕРСИЯ"""
    faculty = forms.ChoiceField(
        choices=Profile.FACULTY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Факультет'
    )
    
    year_of_study = forms.IntegerField(
        min_value=1,
        max_value=6,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Курс обучения'
    )
    
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label='Дата рождения'
    )
    
    student_id = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Студенческий билет'
    )
    
    def save(self, commit=True):
        # 1. Сохраняем пользователя
        user = super().save(commit=False)
        if commit:
            user.save()
        
        # 2. Создаем профиль ВРУЧНУЮ
        profile = Profile.objects.create(
            user=user,
            role='STUDENT',
            faculty=self.cleaned_data['faculty'],
            year_of_study=self.cleaned_data.get('year_of_study', 1),
            birth_date=self.cleaned_data.get('birth_date'),
            student_id=self.cleaned_data.get('student_id'),
            is_active=True
        )
        
        return user


# Остальные формы оставляем без изменений
class TeacherRegistrationForm(BaseUserRegistrationForm):
    """Форма регистрации преподавателя"""
    invitation_code = forms.CharField(
        max_length=50,
        required=True,
        label='Код приглашения',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    specialization = forms.CharField(
        max_length=200,
        required=True,
        label='Специализация',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    degree = forms.CharField(
        max_length=100,
        required=False,
        label='Ученая степень',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    academic_rank = forms.CharField(
        max_length=100,
        required=False,
        label='Ученое звание',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    department = forms.CharField(
        max_length=200,
        required=False,
        label='Кафедра',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    def clean_invitation_code(self):
        code = self.cleaned_data['invitation_code']
        from django.conf import settings
        if hasattr(settings, 'TEACHER_INVITATION_CODE'):
            if code != settings.TEACHER_INVITATION_CODE:
                raise ValidationError("Неверный код приглашения")
        return code
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        
        profile = Profile.objects.create(
            user=user,
            role='TEACHER',
            specialization=self.cleaned_data['specialization'],
            degree=self.cleaned_data.get('degree', ''),
            academic_rank=self.cleaned_data.get('academic_rank', ''),
            department=self.cleaned_data.get('department', ''),
            is_active=True
        )
        
        # Создаем преподавателя
        Instructor.objects.create(profile=profile)
        
        return user


class ProfileForm(forms.ModelForm):
    """Форма редактирования профиля"""
    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'bio']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile = self.instance
        
        if profile.role == 'STUDENT':
            self.fields['faculty'] = forms.ChoiceField(
                choices=Profile.FACULTY_CHOICES,
                widget=forms.Select(attrs={'class': 'form-control'}),
                label='Факультет',
                required=False,
                initial=profile.faculty
            )
            self.fields['student_id'] = forms.CharField(
                max_length=20,
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label='Студенческий билет',
                initial=profile.student_id
            )
            self.fields['year_of_study'] = forms.IntegerField(
                min_value=1,
                max_value=6,
                widget=forms.NumberInput(attrs={'class': 'form-control'}),
                label='Курс обучения',
                required=False,
                initial=profile.year_of_study
            )
            self.fields['birth_date'] = forms.DateField(
                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                required=False,
                label='Дата рождения',
                initial=profile.birth_date
            )
        elif profile.role == 'TEACHER':
            self.fields['specialization'] = forms.CharField(
                max_length=200,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label='Специализация',
                required=True,
                initial=profile.specialization
            )
            self.fields['degree'] = forms.CharField(
                max_length=100,
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label='Ученая степень',
                initial=profile.degree
            )
            self.fields['academic_rank'] = forms.CharField(
                max_length=100,
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label='Ученое звание',
                initial=profile.academic_rank
            )
            self.fields['department'] = forms.CharField(
                max_length=200,
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label='Кафедра',
                initial=profile.department
            )
            self.fields['office'] = forms.CharField(
                max_length=50,
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label='Кабинет',
                initial=profile.office
            )


class FeedbackForm(forms.Form):
    """Форма обратной связи"""
    name = forms.CharField(max_length=100, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, label='Тема сообщения', widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Текст сообщения', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    
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


class EnrollmentForm(forms.ModelForm):
    """Форма записи на курс"""
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status', 'grade']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
        }