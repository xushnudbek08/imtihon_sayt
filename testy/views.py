from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.conf import settings
import random
from .forms import RegisterStepOneForm, EmailCodeForm
from .message import to_sms
from .models import *
from .forms import TimeSelectForm
from django.utils import timezone
import openpyxl
from .models import Category, Question, AnswerOption
from .forms import UploadTestForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .news import fetch_kunuz
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required




def firstpage(request):
    if request.user.is_authenticated:
        return redirect('home')  # login bo‘lsa avtomatik home ga
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

            return redirect('email')
    else:
        form = RegisterStepOneForm()
    return render(request, 'register.html', {'form': form})



def verify_email_code(request):
    reg_data = request.session.get('reg_data')
    if not reg_data:
        messages.error(request, "Ro‘yxatdan o‘tish ma’lumotlari topilmadi.")
        return redirect('register_step_one')

    if request.method == 'POST':
        form = EmailCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip()
            if code == request.session.get('email_code'):

                if User.objects.filter(username=reg_data['username']).exists():
                    messages.error(request, "Bu username allaqachon mavjud. Iltimos, boshqa username tanlang.")
                    return redirect('register_step_one')

                try:
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

                    messages.success(request, "Ro‘yxatdan muvaffaqiyatli o‘tdingiz.")
                    return redirect('home')

                except IntegrityError:
                    messages.error(request, "Foydalanuvchi yaratishda xatolik: Username yoki Email band.")
                    return redirect('register_step_one')

            else:
                messages.error(request, "Tasdiqlash kodi noto‘g‘ri.")
    else:
        form = EmailCodeForm()

    return render(request, 'email.html', {
        'form': form,
        'email': reg_data.get('email')
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("redirect_user")  # ← mana bu muhim o‘zgarish!
        else:
            return render(request, "login.html", {"error": "Login yoki parol xato"})

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    messages.success(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('login')  

@login_required
def profile_view(request):
    user = request.user
    results = TestResult.objects.filter(user=user).order_by('-date')  # so‘nggi natijalar birinchi

    return render(request, 'profil.html', {
        'user': user,
        'results': results
    })



def home(request):
    return render(request, 'home.html')


def NewsListView(request):
    fetch_kunuz()  # kunuz.com dan yangiliklarni olish
    News = news.objects.order_by('-published')[:20]
    return render(request, 'news_list.html', {'news': News})

def is_superuser(user):
    return user.is_superuser

def contact(request):


    return render(request, 'contact.html')

def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            if len(row) != 7:
                messages.error(request, f"{i}-qatorda xato: {row}")
                continue

            subject, question, a, b, c, d, correct = row

            category, _ = TestCategory.objects.get_or_create(name=subject)

            TestQuestion.objects.create(
                category=category,
                question=question,
                a=a,
                b=b,
                c=c,
                d=d,
                correct=correct.strip().lower()
            )

        messages.success(request, "✅ Excel fayldan savollar muvaffaqiyatli yuklandi.")
        return redirect('upload_excel')

    # DB dagi barcha kategoriyalar va savollar soni
    categories = TestCategory.objects.all()
    for cat in categories:
        cat.question_count = TestQuestion.objects.filter(category=cat).count()

    return render(request, 'admin/upload_excel.html', {
        'categories': categories
    })


#test uchun viewlar




from django.db.models import Count

def category_list(request):
    categories = TestCategory.objects.annotate(
        question_count=Count('testquestion')
    )
    return render(request, 'tests/category_list.html', {'categories': categories})


@login_required
def start_test(request, category_id):
    category = get_object_or_404(TestCategory, id=category_id)
    questions = TestQuestion.objects.filter(category=category)

    if request.method == 'POST':
        correct = 0
        total = questions.count()

        for q in questions:
            user_answer = request.POST.get(f'q{q.id}')
            if user_answer and user_answer.lower().strip() == q.correct.lower().strip():
                correct += 1

        score = round((correct / total) * 100)

        # Saqlash
        TestResult.objects.create(
            user=request.user,
            subject=category.name,
            score=score,
            total_questions=total,
            correct_answers=correct
        )

        messages.success(request, f"Siz testni yakunladingiz! {correct}/{total} to‘g‘ri.")
        return redirect('profile_stats')

    return render(request, 'tests/test_page.html', {'questions': questions, 'category': category})

@login_required
def profile_stats(request):
    test_results = TestResult.objects.filter(user=request.user).order_by('-date')  # oxirgi ishlanganlar tepa
    return render(request, 'statistika.html', {'results': test_results})








def redirect_user(request):
    if not request.user.is_authenticated :
        return redirect('firstpage')  # foydalanuvchi login bo‘lsa, firstpage ga
    elif request.user.is_superuser:
        return redirect('upload_excel')  # superuser yuklash sahifasiga
    else:
        return redirect('home')