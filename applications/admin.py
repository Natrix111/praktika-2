from django.contrib import admin

from .models import User, Application, Category, Place
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Place)

from django import forms
from django.core.exceptions import ValidationError
from .models import Application, Category

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'image', 'category', 'status', 'design_image', 'comment', 'user']

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        design_image = cleaned_data.get('design_image')
        comment = cleaned_data.get('comment')

        if status == 'completed' and not design_image:
            raise ValidationError("Для статуса 'Выполнено' необходимо прикрепить изображение дизайна")

        if status == 'in_progress' and not comment:
            raise ValidationError("Для статуса 'Принято в работу' необходимо указать комментарий")

        return cleaned_data


class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationForm
    list_display = ('title', 'category', 'status', 'created_at', 'user')
    readonly_fields = ['title', 'description', 'category', 'created_at', 'user', 'image']

admin.site.register(Application, ApplicationAdmin)


