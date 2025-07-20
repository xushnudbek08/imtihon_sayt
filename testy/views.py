from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
import random
from .forms import RegisterStepOneForm, EmailCodeForm
from .message import to_sms






def firstpage(request):
    return render(request, 'firstpage.html')





def register_step_one(request):
    if request.method == 'POST':
        form = RegisterStepOneForm(request.POST)
        if form.is_valid():
            
            request.session['reg_data'] = form.cleaned_data

            code = str(random.randint(100000, 999999))
            request.session['email_code'] = code

            
            email = form.cleaned_data['email']
            message_text = f"Sizning tasdiqlash kodingiz: {code} Iltimos,bu kodni tsdiqlash shifasiga yozing./nQodni hech kimga aytmang!"
            to_sms(to_email=email, message_text=message_text)

            return redirect('verify_email_code')
    else:
        form = RegisterStepOneForm()
    return render(request, 'register.html', {'form': form})


def verify_email_code(request):
    reg_data = request.session.get('reg_data')
    if not reg_data:
        messages.error(request, "Royxatdan otish malumotlari topilmadi.")
        return redirect('register_step_one')

    if request.method == 'POST':
        form = EmailCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip()
            if code == request.session.get('email_code'):

                if User.objects.filter(username=reg_data['username']).exists():
                    messages.error(request, "Bu username allaqachon mavjud.")
                    return redirect('register_step_one')

                user = User(
                    username=reg_data['username'],
                    email=reg_data['email'],
                    first_name=reg_data['first_name'],
                    last_name=reg_data['last_name']
                )
                user.set_password(reg_data['password1'])
                user.save()

                login(request, user)

               
                request.session.pop('reg_data', None)
                request.session.pop('email_code', None)

                messages.success(request, "Royxatdan muvaffaqiyatli otdingiz.")
                return redirect('home')
            else:
                messages.error(request, "Tasdiqlash kodi notogri.")
    else:
        form = EmailCodeForm()

    return render(request, 'email.html', {
        'form': form,
        'email': reg_data.get('email')
    })


def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    return render(request, 'logout.html')


def profile_view(request):
    return render(request, 'profile.html')


def home(request):
    return render(request, 'home.html')


def test(request):
    return render(request, 'test.html')


def email(request):
    return render(request, 'email.html')
