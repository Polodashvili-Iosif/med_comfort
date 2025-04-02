from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserCreationForm

User = get_user_model()


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main:index')
    template_name = 'users/signup.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = [
        "first_name",
        "last_name",
        "patronymic",
        "gender",
        "birth_date",
        "phone_number"
    ]
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})
