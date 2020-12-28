from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_process
from django.contrib.auth import logout as logout_process
from django.contrib.auth.decorators import login_required
from .models import PollsUser, Poll, Choices, Vote, Follow
from django.template import loader
from django.utils import timezone
import datetime


def home(request):
    return render(request, 'home.html', {})


def register(request):

    context = {}

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            if User.objects.filter(username=username).exists():
                context["error"] = "Username already exists"
                context["form"] = form

                return render(request, 'register.html', context)

            else:
                if User.objects.filter(email=email).exists():
                    context["error"] = "Email already exists"
                    context["form"] = form

                    return render(request, 'register.html', context)

                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()

                u = User.objects.get(username=username)
                pu = PollsUser(user=u, vote_count=0, question_count=0, follower_count=0, following_count=0)
                pu.save()

                return redirect('Polls')
        else:
            context["error"] = "Username or email already exists"
            context["form"] = form

            return render(request, 'register.html', context)
    form = RegisterForm()
    context["form"] = form
    return render(request, 'register.html', context)


def login(request):
    context = {}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            u = authenticate(request, username=username, password=password)

            if u is not None:
                login_process(request, u)
                return redirect(request.GET.get('next'))

            else:
                context["error"] = "Invalid Username or password"
                context["form"] = LoginForm(request.POST)

                return render(request, 'login.html', context)

    form = LoginForm()
    context["form"] = form
    return render(request, 'login.html', context)


def logout(request):
    logout_process(request)

    return redirect("Polls")


@login_required(login_url='/login')
def polls(request):
    polls_list = Poll.objects.all().order_by('date_published', 'votes')
    main_list = []
    sub_list = []
    for poll in polls_list:
        if Follow.objects.filter(user=request.user).filter(follow_user=poll.user).exists():
            if poll.date_published >= timezone.now() - datetime.timedelta(days=5):
                main_list.append(poll)
        else:
            sub_list.append(poll)

    context = {
        "main_polls": main_list,
        "sub_polls": sub_list,
    }

    if len(main_list) == 0:
        context["main_is_empty"] = True

    return render(request, 'polls.html', context)


@login_required(login_url='/login')
def add_poll(request):
    context = {
         "nums": [1, 2],
         "total": 2
    }
    if request.method == 'POST':
        num = int(request.POST["number_choices"])
        nums = []
        for i in range(num):
            nums.append(i+1)
        context["nums"] = nums
        context["total"] = len(nums)

        return render(request, 'add_poll.html', context)

    return render(request, 'add_poll.html', context)


def add_poll_process(request):
    user = request.user
    text = request.POST["text"]
    total = int(request.POST["number_of_choices"])

    q = Poll(user=user, text=text, date_published=timezone.now())
    q.save()
    pu = PollsUser.objects.get(user=user)
    pu.question_count += 1
    pu.save()

    for i in range(total):
        text = request.POST[f"{i+1}"]
        c = Choices(question=q, text=text, votes=0)
        c.save()

    return redirect('Polls')


@login_required(login_url='/login')
def my_polls(request):
    polls_list = Poll.objects.filter(user=request.user)
    context = {
        "polls": polls_list
    }
    if len(polls_list) == 0:
        context["empty"] = True

    if request.method == 'POST':
        p_id = request.POST['poll_id']
        p = Poll.objects.get(pk=p_id)
        p.delete()
        polls_list = Poll.objects.filter(user=request.user)
        context["polls"] = polls_list

        pu = PollsUser.objects.get(user=request.user)
        pu.question_count -= 1
        pu.save()

    return render(request, 'my_polls.html', context)


@login_required(login_url='/login')
def vote(request, poll_id):

    poll = Poll.objects.get(pk=poll_id)
    context = {
        "poll": poll
    }

    if Vote.objects.filter(user=request.user).filter(Question=poll).exists():
        context["already_voted"] = True

    if request.method == 'POST':
        option_id = request.POST["option"]
        choice = Choices.objects.get(pk=option_id)

        choice.votes += 1
        choice.save()

        v = Vote(user=request.user, Question=poll, Option=choice, date=timezone.now())
        v.save()

        poll.votes += 1
        poll.save()

        pu = PollsUser.objects.get(user=request.user)
        pu.vote_count += 1
        pu.save()

        return redirect('Result', poll.id)

    return render(request, 'vote.html', context)


@login_required(login_url='/login')
def result(request, poll_id):
    p = Poll.objects.get(pk=poll_id)
    context = {
        "poll": p
    }
    return render(request, 'result.html', context)


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    pu = PollsUser.objects.get(user=user)
    users_polls = Poll.objects.filter(user=user)

    context = {
        "user": user,
        "polluser": pu,
        "polls": users_polls
    }
    if len(users_polls) == 0:
        context["empty"] = True
    if user != request.user:
        context["other"] = True
        if Follow.objects.filter(user=request.user).filter(follow_user=user).exists():
            context["following"] = True

    return render(request, 'profile.html', context)


@login_required(login_url='/login')
def result_map(request):
    votes = Vote.objects.filter(user=request.user)

    questions = []
    for i in votes:
        questions.append(i.Question)

    context = {
        "questions": questions,
        "length": len(questions)
    }

    return render(request, 'result_map.html', context)


@login_required(login_url='/login')
def follow(request, followed_id, follower_id):
    followed = User.objects.get(pk=followed_id)
    follower = User.objects.get(pk=follower_id)

    f = Follow(user=follower, follow_user=followed, date=timezone.now())
    f.save()

    pu = PollsUser.objects.get(user=follower)
    pu.following_count += 1
    pu.save()

    pu = PollsUser.objects.get(user=followed)
    pu.follower_count += 1
    pu.save()

    return redirect('Profile', followed_id)


@login_required(login_url='/login')
def unfollow(request, followed_id, follower_id):

    follower = User.objects.get(pk=follower_id)
    followed = User.objects.get(pk=followed_id)
    f = Follow.objects.filter(user=follower).filter(follow_user=followed)
    f = f[0]
    f.delete()

    pu = PollsUser.objects.get(user=follower)
    pu.following_count -= 1
    pu.save()

    pu = PollsUser.objects.get(user=followed)
    pu.follower_count -= 1
    pu.save()

    return redirect('Profile', followed_id)


@login_required(login_url='/login')
def discover(request):
    pu = PollsUser.objects.exclude(user=request.user).order_by('question_count', 'vote_count', 'follower_count', 'following_count')

    context = {
        "poll_users": pu
    }
    return render(request, 'discover.html', context)


def search(request):

    search_text = request.GET["search"]
    s_polls = Poll.objects.filter(text__icontains=search_text)

    context = {
        "search_polls": s_polls
    }

    if len(s_polls) == 0:
        context["empty"] = True

    return render(request, 'search.html', context)
