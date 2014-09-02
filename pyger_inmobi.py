#!/usr/bin/env python
""" PagerDuty Oncall List  """

import pygerduty
from datetime import datetime, timedelta

NOW = datetime.now().__str__()
ONE_HOUR = NOW + timedelta(hours=1).__str__()

API_USER = "inmobi.pagerduty.com"
API_PWD = "XXXXXXXXXX"
PAGER = pygerduty.PagerDuty(API_USER, API_PWD)

def get_contacts(userid):
    """ To get the contact number of the user using userid """

    userdesc = PAGER.users.show(userid)
    userdetail = userdesc.contact_methods.list()
    for userattr in userdetail:
        userphone = userattr.to_json()
        if not userphone.get("phone_number") is None:
            return userphone.get("phone_number")


for schedule in PAGER.schedules.list():
    shname = schedule.name
    teamdesc = PAGER.schedules.show(schedule.id)
    teams = teamdesc.entries.list(since=""+NOW+"", until=""+ONE_HOUR+"",
     overflow=False)
    for team in teams:
        on = team.to_json()
        oncall = on['user']['name']
        oncallid = on['user']['id']
        phone = get_contacts(oncallid)
        print(schedule.name+"\t Oncall:\t  "+oncall+" ("+phone+")")

