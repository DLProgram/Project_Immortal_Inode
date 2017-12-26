from django.shortcuts import render
import json
from lxml import html
import requests
from django.http import HttpResponse

EVENT_URL = "https://www.robotevents.com/robot-competitions/vex-robotics-competition/{}.html"
TEAM_URL = "https://api.vexdb.io/v1/get_events?team={}&season=current&status={}"


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


def event(request, event_id):
    context = {"title": "Event:{}".format(event_id), "event_id": event_id}
    data = json.loads(html.fromstring(requests.get(EVENT_URL.format(
        event_id)).content).xpath('//results[@program="VRC"]/@data')[0])
    round2 = [x for x in data if x['round'] == 2]
    context["matches"] = round2
    return render(request, 'spider/match.html', context)


def add_to_db(request, event_id):
    data = json.loads(html.fromstring(requests.get(EVENT_URL.format(
        event_id)).content).xpath('//results[@program="VRC"]/@data')[0])
    return HttpResponse("OK")
