from pyexpat.errors import messages

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views import generic
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


from . forms import ApplicationForm
from .models import Application, User


class index(generic.ListView):
    model = Application
    template_name = 'index.html'
    context_object_name = 'completed_applications'

    def get_queryset(self):
        return Application.objects.filter(status='completed').order_by('-created_at')[:4]

class Register(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

def logout_view(request):
    logout(request)
    return redirect('index')

class ApplicationCreate(LoginRequiredMixin, generic.CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'create_application.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class Profile(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'profile.html'
    context_object_name = 'user_applications'

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.GET.get('status')
        queryset = Application.objects.filter(user=user).order_by('-created_at')

        if status_filter in ['new', 'in_progress', 'completed']:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        return context

class ApplicationDelete(generic.DeleteView):
    model = Application
    template_name = 'delete_application.html'
    success_url = reverse_lazy('profile')

class UpdatePlaceView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ['place']
    template_name = 'change_place.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        applications = Application.objects.filter(user=self.request.user)

        if applications.filter(status__in=['new', 'in_progress']).exists():
            form.add_error('place', 'Вы можете изменить район только если все ваши заявки находятся в статусе "Выполнено".')
            return self.form_invalid(form)

        return super().form_valid(form)





