from django.shortcuts import render
import json
from lxml import html
import requests
from django.http import HttpResponse
from pymongo import MongoClient
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


EVENT_URL = "https://www.robotevents.com/robot-competitions/vex-robotics-competition/{}.html"
TEAM_URL = "https://api.vexdb.io/v1/get_events?team={}&season=current&status={}"


def staff_check(user):
    print(user)
    return user.is_staff


@user_passes_test(staff_check)
def index(request):
    context = {"title": "Search"}
    if "team" in request.GET:
        team = request.GET["team"]
        # TODO: chnage past to current
        current = requests.get(TEAM_URL.format(team, "past")).json()["result"]
        future = requests.get(TEAM_URL.format(team, "future")).json()["result"]
        matches = current + future
        context["matches"] = matches

    return render(request, 'spider/index.html', context)


@user_passes_test(staff_check)
def event(request, event_id):
    context = {"title": "Event:{}".format(event_id), "event_id": event_id}
    data = json.loads(html.fromstring(requests.get(EVENT_URL.format(
        event_id)).content).xpath('//results[@program="VRC"]/@data')[0])
    round2 = [x for x in data if x['round'] == 2]
    context["matches"] = round2
    return render(request, 'spider/match.html', context)


@user_passes_test(staff_check)
def add_to_db(request, event_id):
    try:
        client = MongoClient()
        db = client.pi2

        db.matches.drop()

        data = json.loads(html.fromstring(requests.get(EVENT_URL.format(
            event_id)).content).xpath('//results[@program="VRC"]/@data')[0])
        round2 = [x for x in data if x['round'] == 2]

        db.matches.insert_many(round2)
        result = db.matches.count()
    except:
        result = False

    return HttpResponse(json.dumps({"success": result}), content_type="application/json")
