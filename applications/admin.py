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
            raise ValidationError("Для статуса 'Выполнено' необходимо прикрепить изображение дизайна.")

        if status == 'in_progress' and not comment:
            raise ValidationError("Для статуса 'Принято в работу' необходимо указать комментарий.")

        return cleaned_data


class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationForm

    list_display = ('title', 'category', 'status', 'created_at', 'user')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username')

    def save_model(self, request, obj, form, change):
        if obj.status in ['in_progress', 'completed']:
            obj.status = form.cleaned_data['status']
        elif obj.is_status_change_allowed(form.cleaned_data['status']):
            obj.status = form.cleaned_data['status']
        else:
            raise ValidationError("Смена статуса невозможна.")

        super().save_model(request, obj, form, change)


admin.site.register(Application, ApplicationAdmin)


