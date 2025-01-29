# views.py

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login , logout as auth_logout
from .forms import CustomUserCreationForm
from .models import Question
from django.contrib.auth.decorators import login_required

OTP_CONSTANT = "9876"

def verification_required(view_func):
    """
    Decorator to ensure that the user is logged in and has a verified status.
    If the user is not verified, they are redirected to a 'not verified' page or login page.
    """
    # First, ensure the user is logged in by using `login_required` decorator.
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is verified
        if not request.user.verified:
            # If the user is not verified, redirect them to a page of your choice.
            return redirect('verify')  # Change this to a suitable page URL or view
        
        # If the user is logged in and verified, continue to the original view.
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def index(request):
    return render(request, "index.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Use auth_login instead of login
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')  # Redirect to the homepage or another page
        else:
            print(request)
            messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/login.html')  # Render the login template if GET r


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, 'There was an error creating your account.')

    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})




@login_required
def verify(request):
    
    # If the user is already verified, redirect to the home page
    if request.user.verified:
        return redirect('index')

    if request.method == 'POST':
        # Get the OTP values from the form
        otp_1 = request.POST.get('otp_1')
        otp_2 = request.POST.get('otp_2')
        otp_3 = request.POST.get('otp_3')
        otp_4 = request.POST.get('otp_4')

        # Concatenate the OTP digits entered by the user
        entered_otp = otp_1 + otp_2 + otp_3 + otp_4

        # Check if the entered OTP matches the constant OTP
        if entered_otp == OTP_CONSTANT:
            request.user.verified = True
            request.user.save()
            messages.success(request, "OTP verified successfully! Your account is now verified.")
            return redirect('index')  # Redirect to the homepage or desired page
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'auth/verify.html')


# View for the quiz page, showing 5 random questions
@login_required
@verification_required
def quiz(request):
    if not request.user.verified:
        return redirect("verify")
    # Check if the questions are already stored in the session
    if 'quiz_questions' not in request.session:
        # Fetch 5 random questions and store their IDs in the session
        questions = Question.objects.order_by('?')[:5]
        request.session['quiz_questions'] = [question.id for question in questions]
    else:
        # Retrieve the question IDs from the session and fetch the questions
        question_ids = request.session['quiz_questions']
        questions = Question.objects.filter(id__in=question_ids)

    if request.method == 'POST':
        score = 0
        # Iterate through the questions and check answers
        for question in questions:
            user_answer = request.POST.get(f'answer_{question.id}')
            correct_answer = str(question.correct_answer).strip()
            user_answer = str(user_answer).strip()

            if user_answer == correct_answer:
                score += 1

        # Clear the stored questions in the session after the quiz is completed
        del request.session['quiz_questions']

        # Render the result page
        return render(request, 'result.html', {'score': score, 'total_questions': len(questions)})

    # If it's a GET request, render the quiz page with the questions
    return render(request, 'quiz.html', {'questions': questions})


# View for result page (after submitting the quiz)
@login_required
@verification_required
def results(request, score):
    return render(request, 'result.html', {'score': score})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("login")