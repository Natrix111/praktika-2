from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class Place(models.Model):
    name = models.CharField(max_length=50, help_text="Выберите район")

    def __str__(self):
        return self.name

class User(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name='Имя', blank=False)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', blank=False)
    username = models.CharField(max_length=200, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=False, default='2005-01-01')

    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.first_name

class Category(models.Model):

    name = models.CharField(max_length=200, help_text="Выберите категорию")

    def __str__(self):
        return self.name

def validate_image(image):
    valid_mime_types = ['image/jpeg', 'image/png', 'image/bmp']
    mime_type = image.file.content_type
    if mime_type not in valid_mime_types:
        raise ValidationError("Формат файла должен быть: jpg, jpeg, png, bmp.")

    file_size = image.size
    if file_size > 2 * 1024 * 1024:
        raise ValidationError("Размер файла не должен превышать 2 МБ.")

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    title = models.CharField(verbose_name="Название",max_length=200)
    description = models.TextField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='applications/', validators=[validate_image])
    status = models.CharField(choices=STATUS_CHOICES, default='new', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



