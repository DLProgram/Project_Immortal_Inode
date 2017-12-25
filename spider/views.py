from django.shortcuts import render
import json
from lxml import html
import requests
from django.http import HttpResponse

URL = "https://www.robotevents.com/robot-competitions/vex-robotics-competition/{}.html"


def index(request):
    pass


def search_by_team(request, team):
    # TODO: chnage past to current
    current = requests.get(
        "https://api.vexdb.io/v1/get_events?team={}&season=current&status=past".format(team)).json()
    future = requests.get(
        "https://api.vexdb.io/v1/get_events?team={}&season=current&status=future".format(team)).json()

    result = ""
    for d in current["result"]:
        result = result + str(d["key"]) + "<br/>"
    for d in future["result"]:
        result = result + str(d["key"]) + "<br/>"
    return HttpResponse(result)


def event(request, event_id):
    # event_id = "RE-VRC-17-3628"
    data = json.loads(html.fromstring(requests.get(URL.format(
        event_id)).content).xpath('//results[@program="VRC"]/@data')[0])

    result = ""
    for d in data:
        result = result + str(d) + "<br/>"
    return HttpResponse(result)


def add_to_db(request, event_id):
    pass
