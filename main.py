import os, requests, json, random, pytz, itertools
# from ics import Calendar, Event
from pathlib import Path
from zoneinfo import ZoneInfo
from settings import SourceJson
from datetime import datetime
from string import Template # fuck me

# Measure-Command {& "python.exe" "main.py"}

# it takes this long to run for a 4kb file.
# Days              : 0
# Hours             : 0
# Minutes           : 0
# Seconds           : 4
# Milliseconds      : 944
# Ticks             : 49448624
# TotalDays         : 5.72322037037037E-05
# TotalHours        : 0.00137357288888889
# TotalMinutes      : 0.0824143733333333
# TotalSeconds      : 4.9448624
# TotalMilliseconds : 4944.8624

# have some work todo: https://icalendar.org/validator.html.html?url=https://tzevaadom-ics.pages.dev/Test_2_CF.ics#results
# Measure-Command {& "python.exe" "main.py"}


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
    local = pytz.timezone("Asia/Jerusalem")
    
    RawJsonLen = len(JsonName)
    IcsFinal = ""
    IcsHeader = """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
PRODID:redalert.local
METHOD:PUBLISH
VTIMEZONE:"""
    IcsFooter = """
END:VCALENDAR"""
    
    IcsFinal += IcsHeader
    for JsonObject in range(0, RawJsonLen):
    # for JsonObject in range(0, 10):
        EventTitle = "Red Alert in "
        # for Place in JsonName[JsonObject][2]:
        #     EventTitle += Place
        EventTitle += JsonName[JsonObject][2][0]
        EventUnixTime = JsonName[JsonObject][3]

        EventUid = str(JsonObject)+"@"+str(EventUnixTime)+"."+str(JsonName[JsonObject][0])+"."+str(JsonName[JsonObject][1])        
        
        # EventUid = str(EventUnixTime)+"@"+str(len(JsonName[JsonObject][2]))+"."+str(JsonName[JsonObject][1])
        # EventUtcTime = (datetime.fromtimestamp(JsonName[JsonObject][3]))
        EventLocalTime = datetime.fromtimestamp(JsonName[JsonObject][3])

        # local_dt = local.localize(EventLocalTime, is_dst=None)
        local_dt = local.localize(EventLocalTime)
        EventUtcTime = local_dt.astimezone(pytz.utc)

        EventSummary = EventTitle
        EventDTSTART = datetime.strftime(EventUtcTime, "%Y%m%dT%H%M%S")
        EventDTEND = datetime.strftime(datetime.fromtimestamp((JsonName[JsonObject][3]+15)), "%Y%m%dT%H%M%S")
        IcsTemplate = Template("""
BEGIN:VEVENT
UID:$UID
SUMMARY:$TITLE
DTSTAMP:19700101T000000Z
DTSTART:$DTSTART
DTEND:$DTEND
SEQUENCE:0
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
GlobalJsonFile = DownloadJsonDict(SourceJson, GlobalProdFolder, "Prod")
IcsContent = JsonIntoIcs(GlobalJsonFile)
WriteIcsToFile(IcsContent, GlobalProdFolder, "Prod.ics")
# GitAddGitPush(SourceJson, """https://tzevaadom-ics.pages.dev/Prod.ics""") # need to add check if ics os over 100mb

# print(IcsContent)
# TESTDATE = 1774011703
# testdate = datetime.fromtimestamp(TESTDATE+900)
# print(testdate)
# print(datetime.strftime(testdate, "%Y%m%dT%H%M%S"))