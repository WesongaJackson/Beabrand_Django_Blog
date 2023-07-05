from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm ,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
           form.save()
           first_name = form.cleaned_data.get('first_name')
           last_name = form.cleaned_data.get('last_name')
           email= form.cleaned_data.get('email')
           messages.success(request,f'your account has been created you can login now!')
           subject= f'Hi {first_name}  {last_name} Welcome, to Our Website!'
           message='Thank You for signing up on our Website'
           from_email=[settings.EMAIL_HOST_USER]
           recipient_list=[email]
           send_mail(subject,message,from_email,recipient_list)
           return redirect('login')
    else:
     form=UserRegisterForm()
    return render(request,'UsersApp/register.html',{'form':form})
#profile function
@login_required
def profile(request):
   if request.method == 'POST': 
      u_form=UserUpdateForm( request.POST,request.FILES ,instance=request.user)
      p_form=ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
      if u_form.is_valid()and p_form.is_valid():
         u_form.save()
         p_form.save()
         messages.success(request,f'profile updated!')
         return redirect('profile')
   else:
      u_form=UserUpdateForm( instance=request.user)
      p_form=ProfileUpdateForm(instance=request.user.profile)
   context={
      'u_form':u_form,
      'p_form':p_form,
   }
   return render(request,'UsersApp/profile.html',context)
@login_required
def delete_profile(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['password'])
            if user is not None:
                user.delete()
                messages.success(request, 'Your account has been deleted.')
                return redirect('blog-home')  # Redirect to the home page or any other page after deletion
            else:
                messages.error(request, 'Invalid password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'UsersApp/profile_confirm_delete.html', {'form': form})

