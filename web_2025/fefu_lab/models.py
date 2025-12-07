from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """Модель профиля пользователя"""
    ROLE_CHOICES = [
        ('STUDENT', 'Студент'),
        ('TEACHER', 'Преподаватель'),
        ('ADMIN', 'Администратор'),
    ]
    
    FACULTY_CHOICES = [
        ('CS', 'Кибербезопасность'),
        ('SE', 'Программная инженерия'),
        ('IT', 'Информационные технологии'),
        ('DS', 'Наука о данных'),
        ('WEB', 'Веб-технологии'),
    ]
    
    ADMIN_LEVEL_CHOICES = [
        ('MODERATOR', 'Модератор'),
        ('MANAGER', 'Менеджер'),
        ('SUPER_ADMIN', 'Супер-админ'),
    ]
    
    # Связь с встроенной моделью User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='STUDENT',
        verbose_name='Роль'
    )
    
    # Общие поля для всех
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True, 
        blank=True,
        verbose_name='Аватар'
    )
    
    phone = models.CharField(
        max_length=20, 
        null=True, 
        blank=True,
        verbose_name='Телефон'
    )
    
    bio = models.TextField(
        null=True, 
        blank=True,
        verbose_name='О себе'
    )
    
    # Поля для студентов
    student_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Студенческий билет'
    )
    
    birth_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Дата рождения'
    )
    
    faculty = models.CharField(
        max_length=3, 
        choices=FACULTY_CHOICES, 
        null=True,
        blank=True,
        verbose_name='Факультет'
    )
    
    year_of_study = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Курс обучения',
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    
    # Поля для преподавателей
    specialization = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Специализация'
    )
    
    degree = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Ученая степень'
    )
    
    academic_rank = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Ученое звание'
    )
    
    department = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Кафедра'
    )
    
    office = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Кабинет'
    )
    
    # Поля для администраторов
    admin_level = models.CharField(
        max_length=50,
        choices=ADMIN_LEVEL_CHOICES,
        null=True,
        blank=True,
        verbose_name='Уровень доступа'
    )
    
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['user__last_name', 'user__first_name']
        db_table = 'profiles'

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    def get_role_display_name(self):
        return dict(self.ROLE_CHOICES).get(self.role, 'Неизвестно')

    def get_faculty_display_name(self):
        return dict(self.FACULTY_CHOICES).get(self.faculty, 'Неизвестно')

    def get_admin_level_display_name(self):
        return dict(self.ADMIN_LEVEL_CHOICES).get(self.admin_level, 'Неизвестно')

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})


# # Сигнал для автоматического создания профиля при создании пользователя
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'profile'):
#         instance.profile.save()


# @receiver(post_save, sender=Profile)
# def create_instructor_for_teacher(sender, instance, created, **kwargs):
#     """Автоматическое создание записи в Instructor для преподавателей"""
#     if instance.role == 'TEACHER':
#         Instructor.objects.get_or_create(profile=instance)


class Instructor(models.Model):
    """Модель преподавателя (отдельно для курсов)"""
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='instructor_info',
        verbose_name='Профиль преподавателя',
        limit_choices_to={'role': 'TEACHER'}
    )
    
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['profile__user__last_name']
        db_table = 'instructors'

    def __str__(self):
        return f"{self.profile.full_name}"

    @property
    def first_name(self):
        return self.profile.user.first_name

    @property
    def last_name(self):
        return self.profile.user.last_name

    @property
    def email(self):
        return self.profile.user.email

    @property
    def full_name(self):
        return self.profile.full_name

    @property
    def specialization(self):
        return self.profile.specialization

    @property
    def degree(self):
        return self.profile.degree


class Course(models.Model):
    """Модель курса"""
    LEVEL_CHOICES = [
        ('BEGINNER', 'Начальный'),
        ('INTERMEDIATE', 'Средний'),
        ('ADVANCED', 'Продвинутый'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название курса')
    slug = models.SlugField(unique=True, verbose_name='URL идентификатор')
    description = models.TextField(verbose_name='Описание')
    duration = models.PositiveIntegerField(
        verbose_name='Продолжительность (часов)',
        validators=[MinValueValidator(1), MaxValueValidator(500)]
    )
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='Преподаватель'
    )
    level = models.CharField(
        max_length=12,
        choices=LEVEL_CHOICES,
        default='BEGINNER',
        verbose_name='Уровень сложности'
    )
    max_students = models.PositiveIntegerField(
        default=30,
        verbose_name='Максимальное количество студентов',
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Стоимость'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title']
        db_table = 'courses'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    @property
    def enrolled_students_count(self):
        return self.enrollments.filter(status='ACTIVE').count()

    @property
    def available_slots(self):
        return self.max_students - self.enrolled_students_count


class Enrollment(models.Model):
    """Модель записи на курс"""
    STATUS_CHOICES = [
        ('ACTIVE', 'Активен'),
        ('COMPLETED', 'Завершен'),
        ('CANCELLED', 'Отменен'),
    ]
    
    student = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Студент',
        limit_choices_to={'role': 'STUDENT'}
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Курс'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        verbose_name='Статус'
    )
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    grade = models.CharField(
        max_length=5,
        null=True,
        blank=True,
        verbose_name='Оценка'
    )

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
        db_table = 'enrollments'

    def __str__(self):
        return f"{self.student} - {self.course}"

    def save(self, *args, **kwargs):
        if self.status == 'COMPLETED' and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)