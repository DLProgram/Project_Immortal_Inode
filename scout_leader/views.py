from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from pymongo import MongoClient
import json


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
    context = {"title": "Home"}

    client = MongoClient()
    db = client.pi2
    matches = [m for m in db['matches'].find()]

    context["matches"] = matches
    return render(request, 'scout_leader/index.html', context)


@login_required
def scout(request, match_num):
    context = {"title": "Scout"}

    client = MongoClient()
    db = client.pi2

    match = db['matches'].find_one({'matchnum': match_num})

    context["match_num"] = match_num
    context["team_num"] = match[str(list(request.user.groups.all())[0])]

    return render(request, 'scout_leader/scout.html', context)


def save_data(request):
    client = MongoClient()
    db = client.pi2

    # match_data = request.GET.dict()
    match_data = dict(request.GET.lists())

    for key, value in match_data.items():
        if len(value) == 1:
            if key != "team_num":
                match_data[key] = float(value[0])
            else:
                match_data[key] = value[0]
    score = match_data['finesse'] + match_data['defence'] + match_data['lift'] + \
        match_data['speed'] + match_data['intake'] + \
        match_data['gl'] + (match_data['cone'] if 'cone' in match_data else 0)

    match_data["username"] = request.user.username
    match_data["score"] = score
    db.data.insert_one(match_data)

    print(match_data)

    return redirect("scout_leader:scout",
                    match_num=int(request.GET["match_num"]) + 1)


def list_data(request):
    context = {"title": "Data"}

    client = MongoClient()
    db = client.pi2
    match_data = [m for m in db['data'].find()]

    context["data"] = match_data
    return render(request, 'scout_leader/list_data.html', context)


def team_detail(request, team_num):
    context = {"title": team_num}

    client = MongoClient()
    db = client.pi2
    match_data = [m for m in db['data'].find({"team_num": team_num})]

    context["data"] = match_data
    return render(request, 'scout_leader/team_detail.html', context)
