import pygerduty
from datetime import datetime, timedelta

now = datetime.now()
onehour = now + timedelta(hours=1)

API_USER = "inmobi.pagerduty.com"
API_PWD = "f5CVg44Ho4UzkBNcdmag"
pager = pygerduty.PagerDuty(API_USER, API_PWD)

for schedule in pager.schedules.list():
    shname = schedule.name
    teamdesc = pager.schedules.show(schedule.id)
    for team in teamdesc.entries.list(since=""+now.__str__()+"", until=""+onehour.__str__()+"", overflow=False):
        on = team.to_json()
        oncall = on['user']['name']
        print schedule.name+": "+oncall
    
