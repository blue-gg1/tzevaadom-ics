import os, requests, tzdata, json, pytz, random
# from ics import Calendar, Event
from pathlib import Path
from zoneinfo import ZoneInfo
from settings import SourceJson
from datetime import datetime, date, timezone, tzinfo
from string import Template # fuck me


# it takes this long to run and the file is 105 MB (110,669,824 bytes) big
# Days              : 0
# Hours             : 0
# Minutes           : 11
# Seconds           : 34
# Milliseconds      : 638
# Ticks             : 6946384871
# TotalDays         : 0.00803979730439815
# TotalHours        : 0.192955135305556
# TotalMinutes      : 11.5773081183333
# TotalSeconds      : 694.6384871
# TotalMilliseconds : 694638.4871

# have some work todo: https://icalendar.org/validator.html.html?url=https://tzevaadom-ics.pages.dev/Test_2_CF.ics#results

def FolderManagement():
    script_directory = Path(os.path.dirname(os.path.abspath(__file__)))
    LocalProdFolder = "Prod"
    GlobalPodFolder = script_directory / LocalProdFolder
    
    print(script_directory.parent)
    if os.path.exists(GlobalPodFolder) == False:
        print("Folder is not real. Making now.")
        os.mkdir(GlobalPodFolder)
    else:
        print("Folder is real.")
    return GlobalPodFolder

def LocalTime(Folder):
    LocalTz = ZoneInfo("Asia/Jerusalem")
    dt = datetime.now(LocalTz)
    return dt

def DownloadJsonDict(JsonUrl, DownloadPath, JsonName):
    rGetJson = requests.get(JsonUrl,
                          )
    if rGetJson.status_code != 200:
        print("Failed")
    else:
        print("Success")
        with open(DownloadPath / "sourcejson.json", "wb") as RawJsonFile:
            RawJsonFile.write(rGetJson.content)
    
    JsonName = json.loads(rGetJson.content)
    return(JsonName)


def JsonIntoIcs(JsonName):
    RawJsonLen = len(JsonName)
    IcsFinal = ""
    IcsHeader = """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
PRODID:redalert.local
METHOD:PUBLISH"""
    IcsFooter = """
END:VCALENDAR"""
    
    IcsFinal += IcsHeader
    for JsonObject in range(0, RawJsonLen):
    # for JsonObject in range(0, 10):
        EventTitle = "Red Alert in "
        for Place in JsonName[JsonObject][2]:
            EventTitle += Place
        EventUnixTime = JsonName[JsonObject][3]
        EventUid = str(EventUnixTime)+"@redalert.local"+str(random.randint(0, 10))
        EventLocalTime = datetime.fromtimestamp(JsonName[JsonObject][3])
        EventSummary = EventTitle
        EventDTSTART = datetime.strftime(EventLocalTime, "%Y%m%dT%H%M%S")
        EventDTEND = datetime.strftime(datetime.fromtimestamp((JsonName[JsonObject][3]+15)), "%Y%m%dT%H%M%S")
        EventLOCATION = str(Place)
        IcsTemplate = Template("""
BEGIN:VEVENT
UID:$UID
SUMMARY:$TITLE
DTSTAMP:19700101T000000Z
DTSTART:$DTSTART
DTEND:$DTEND
SEQUENCE:0
STATUS:CONFIRMED
END:VEVENT""")
        IcsTemplateFill = IcsTemplate.substitute(
            UID = EventUid,
            TITLE = EventSummary,
            DTSTART = EventDTSTART,
            DTEND = EventDTEND,
            )
        IcsFinal += IcsTemplateFill
    IcsFinal += IcsFooter
    return(IcsFinal)

def WriteIcsToFile(IcsContent, Path, Filename):
    with open (Path / Filename, "w", encoding="utf-8", newline='\r\n') as IcsOnDisk:
        IcsOnDisk.write(IcsContent)

    FilePath = ""  
    return(FilePath)


def GitAddGitPush(JsonUrl, LiveUrl):
    print("making the git commit")
    GitCommitMessage = "Updated the json from " + JsonUrl + " live now here: "+ LiveUrl
    print(os.system("git add ."))
    print(os.system("git commit -am "+chr(34)+GitCommitMessage+chr(34)))
    print(os.system("git push"))
    pass

GlobalProdFolder = FolderManagement()
GlobalTx = LocalTime(GlobalProdFolder)
GlobalJsonFile = DownloadJsonDict(SourceJson, GlobalProdFolder, "Test")
IcsContent = JsonIntoIcs(GlobalJsonFile)
WriteIcsToFile(IcsContent, GlobalProdFolder, "Test_2_CF.ics")
# GitAddGitPush(SourceJson, """https://tzevaadom-ics.pages.dev/Test_2_CF.ics""") # need to add check if ics os over 100mb





# print(IcsContent)
# TESTDATE = 1774011703
# testdate = datetime.fromtimestamp(TESTDATE+900)
# print(testdate)
# print(datetime.strftime(testdate, "%Y%m%dT%H%M%S"))