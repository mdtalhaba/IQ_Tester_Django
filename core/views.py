from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserUpdateForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from quiz.models import Quiz, Category, Question, Choice, UserResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import QuizScore



def home(req, category_slug = None) :
    data = Quiz.objects.all()
    if category_slug is not None :
        cate = Category.objects.get(slug=category_slug)
        data = Quiz.objects.filter(category=cate)
    category = Category.objects.all()
    return render(req, 'index.html', {'data' : data, 'category' : category})


def quizes(req, category_slug = None) :
    data = Quiz.objects.all()
    if category_slug is not None :
        cate = Category.objects.get(slug=category_slug)
        data = Quiz.objects.filter(category=cate)
    
    category = Category.objects.all()
    return render(req, 'quizes.html', {'data' : data, 'category' : category})


@login_required(login_url="/login/")
def quizHistory(req) :
    data = UserResponse.objects.filter(user=req.user)
    return render(req, 'quiz_history.html', {'data' : data})


@login_required(login_url="/login/")
def quiz_page(request, quiz_id):
    queryset = Question.objects.filter(quiz=quiz_id)
    quiz = Quiz.objects.get(id=quiz_id)
    qn_id = queryset.first().id

    items_per_page = 1
    paginator = Paginator(queryset, items_per_page)

    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    qn_id += current_page.number-1 
    question = Question.objects.get(id=qn_id)
    ans = None
    if request.method == 'POST' :
        ansId = request.POST.get(question.text)
        if ansId is not None :
            ansObj = Choice.objects.get(id=ansId)
            ans = ansObj
            UserResponse.objects.create(user=request.user, quiz=quiz, question=question, selected_choice=ansObj)
            data = UserResponse.objects.filter(user=request.user)
            total = len(data)
            score = sum(1 for userRes in data if userRes.selected_choice.is_correct) * 10
            percent = (score / (total * 10) * 100) if total > 0 else 0
            request.user.quiz_score.score = percent
            request.user.quiz_score.quiz_count = len(data)
            request.user.quiz_score.save()
    
    return render(request, 'quiz_page.html', {'current_page': current_page, 'question' : question, 'quiz': quiz, 'ans': ans})


def leaderboard(req):
    data = QuizScore.objects.all().order_by('-score')
    return render(req, 'leader_board.html', {'data': data})


@login_required(login_url="/login/")
def updateInfo(req) :
    if req.method == 'POST' :
        form = UserUpdateForm(req.POST, instance=req.user)
        if form.is_valid() :
            messages.success(req, 'Your Information is Successfully Changed')
            form.save()
            return redirect('home')
    else : 
        form = UserUpdateForm(instance=req.user)
    return render(req, 'update_info.html', {'form' : form})

@login_required(login_url="/login/")
def pass_change(req) :
    if req.method == 'POST' :
        pass_change_form = PasswordChangeForm(req.user, data=req.POST)
        if pass_change_form.is_valid() :
            messages.success(req, 'Your Password is Successfully Changed')
            pass_change_form.save()
            update_session_auth_hash(req, pass_change_form.user)
            return redirect('update_info')
    else : 
        pass_change_form = PasswordChangeForm(req.user)
    return render(req, 'pass_change.html', {'form' : pass_change_form})


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None

    if user is not None :
        user.is_active = True
        user.save()
        QuizScore.objects.create(user=user, score=0)
        return redirect('login')
    else:
        return redirect('register')


class RegistrationView(CreateView):
    model = User
    template_name = 'register_login.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Register'
        return context

    def form_valid(self, form):
        user = form.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f"http://127.0.0.1:8000/register/active/{uid}/{token}"
        message = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
        send_email = EmailMultiAlternatives("Registration Message", '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

        messages.success(self.request, 'Your Registration is Successfull, Check Your Email and Activate Your Account.')
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'profile.html'


class BlogView(TemplateView):
    template_name = 'blog.html'


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class UserLoginView(LoginView) :
    template_name = 'register_login.html'

    def get_success_url(self) :
        return reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Log In'
        return context


class UserLogoutView(LogoutView) :
    def get_success_url(self):
        return reverse_lazy('login')