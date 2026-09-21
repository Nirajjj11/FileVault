from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import RegisterForm, LoginForm

class RegisterView(FormView):
      template_name = 'accounts/register.html'
      form_class = RegisterForm
      success_url = reverse_lazy("accounts:login")
      
      def form_valid(self, form):
            form.save()
            messages.success(self.request, "Account Created Successfully.")
            return super().form_valid(form)
      
      def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                  return redirect("storage:dashboard")
            return super().dispatch(request, *args, **kwargs)
      
class UserLoginView(LoginView):
      template_name = "accounts/login.html"
      authentication_form = LoginForm
      redirect_authenticated_user = True

class UserLogoutView(LogoutView):
      next_page = reverse_lazy("accounts:login")