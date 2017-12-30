from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            else:
                return redirect("/")

        else:
            return render(request, 'scout_leader/signin.html',
                          {"error": "Wrong Username or password!"})

    else:
        return render(request, 'scout_leader/signin.html')


def signout(request):
    logout(request)
    return redirect("/signin")


@login_required
def index(request):
    context = {"title": "Scout"}
    return render(request, 'scout_leader/index.html', context)


@login_required
def scout(request, match_num):
    context = {"title": "Scout"}
    context["match_num"] = match_num
    context["team_num"] = "211Z"
    return render(request, 'scout_leader/scout.html', context)


def save_data(request):
    return redirect("scout_leader:scout",
                    match_num=int(request.GET["match_num"]) + 1)
