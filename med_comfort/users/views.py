from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main:index')
    template_name = 'users/signup.html'


@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})
