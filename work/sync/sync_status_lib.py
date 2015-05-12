import os,sys,getopt,subprocess,time,re
from datetime import datetime
import cgitb

def status_value(BRANCH,REPO):
    result = os.system("/tools/swdev/devsup/bin/gitlock --check %s %s | grep -w 'LOCKED' >/dev/null 2>&1" %(REPO,BRANCH))
    if result == 0:
        status_name = "LOCKED"
        status_color = "#FF3030"
    elif os.path.exists ("/tools/swdev/bin/shortlist show %s-%s" %(BRANCH,REPO)):
        status_name = "SHORTLISTED"
        status_color = "#FFFF00"
    else:
        status_name = "OPEN FOR COMMITS"
        status_color = "#7CCF29"
    return status_name.rstrip(), status_color

def last_sync_ver(LAST_SYNC_DATE):

    last_sync_date = datetime.strptime(LAST_SYNC_DATE, '%Y-%m-%d %H:%M:%S')
    print last_sync_date
    last_sync_day = time.strftime("%A",time.strptime(str(LAST_SYNC_DATE),'%Y-%m-%d %H:%M:%S'))
    last_sync_date_value = last_sync_date.strftime('%b %d,%Y').rstrip()
    list_of_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    last_sync_day_value = list_of_days.index(last_sync_day)
    current_date = datetime.today()
    print current_date
    current_day_value = datetime.today().weekday()
    print "current day & last sync day"
    print current_day_value, last_sync_day_value,last_sync_day
    date_diff = (time.mktime(current_date.timetuple()) - time.mktime(last_sync_date.timetuple()))/3600
    try:
        date_diff = int(date_diff)
    except:
        date_diff = 0
    color = None
    color_desc = None
    if last_sync_day_value == 5 or last_sync_day_value == 6:
        date_diff = date_diff
    elif last_sync_day_value > current_day_value :
        date_diff = date_diff - 48
    else:
        date_diff =  date_diff
    if (date_diff > 48):
        color = "#FF3030"
        color_desc = "Indicates, sync from SSR to IPOS has happened > 48 hours"
    elif (date_diff < 24):
        color = "#7CCF29"
        color_desc = "Indicates, sync from SSR to IPOS has happened within the last 24 hours"
    elif (date_diff < 48):
        color = "#FFFF00"
        color_desc = "Indicates, sync from SSR to IPOS has happened within the last 48 hours"

    return color, color_desc, last_sync_date_value
