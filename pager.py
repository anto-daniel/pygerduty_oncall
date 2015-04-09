#!/usr/bin/env python
""" PagerDuty Oncall List  """

import pygerduty
from datetime import datetime, timedelta
import argparse
import re

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--teamlist", help=
                    "Gets all the teams in subdomain")
PARSER.add_argument("--oncall", help=
                    "Specify the team name. It will give you the oncall name")
ARGS = PARSER.parse_args()
NOW = datetime.now().__str__()
ONE_HOUR = NOW + timedelta(minutes=1).__str__()
API_USER = "inmobi.pagerduty.com"
API_PWD = "f5CVg44Ho4UzkBNcdmag"
PAGER = pygerduty.PagerDuty(API_USER, API_PWD)


def get_contacts(userid):
    """ To get the contact number of the user using userid """

    userdesc = PAGER.users.show(userid)
    userdetail = userdesc.contact_methods.list()
    for userattr in userdetail:
        userphone = userattr.to_json()
        if not userphone.get("phone_number") is None:
            return userphone.get("phone_number")

def get_teams():
    """ Team List  """

    teamlist = {}
    for schedule in PAGER.schedules.list():
        teamlist[schedule.name] = schedule.id
    return teamlist

def get_oncall(teamid):
    """ To get oncall name """

    oncall_list = PAGER.schedules.show(teamid)
    oncalls = oncall_list.entries.list(since=""+NOW+"", until=""+ONE_HOUR+"",
                                      overflow=False)

    for oncall in oncalls:
        onj = oncall.to_json()
        oname = onj['user']['name']
        oid = onj['user']['id']
        phone = get_contacts(oid)
        return oname, phone

def main():
    """ Main Function """

    if ARGS.teamlist:
        team_list = get_teams()
        for team in  team_list.iteritems():
            print team

    if ARGS.oncall:
        teamlist = get_teams()
        for team in teamlist.keys():
            match = re.search( ARGS.oncall, team, re.M|re.I)
            if match:
                print team
                team_id = teamlist[team]
                oncall = get_oncall(team_id)
                print team+": Oncall: "+oncall[0]
                print team+": Phone: "+oncall[1]+"\n\n"



if __name__ == "__main__":
    main()


