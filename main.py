import os, requests, tzdata, json, pytz
# from ics import Calendar, Event
from pathlib import Path
from zoneinfo import ZoneInfo
from settings import SourceJson
from datetime import datetime, date, timezone, tzinfo
from string import Template # fuck me


# from pytz import timezone    


    # def is_dst(zonename):
    #     """Check if it is currently DST in a given timezone."""
    #     tz = pytz.timezone(zonename)
    #     # Get the current UTC time and make it aware
    #     now_utc = pytz.utc.localize(datetime.utcnow())
    #     # Convert to the target timezone and check the dst() offset
    #     return now_utc.astimezone(tz).dst() != timedelta(0)

    # # Usage examples (results depend on the current date and time)
    # print(f"Is DST active in Los Angeles? {is_dst('America/Los_Angeles')}")
    # print(f"Is DST active in London? {is_dst('Europe/London')}")

    # for JsonObject in range(0, RawJsonLen):
    #     print(JsonName[JsonObject][3], datetime.fromtimestamp(JsonName[JsonObject][3])) # the unix time is local and not UTC


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
PRODID:f1calendar.com
METHOD:PUBLISH
X-PUBLISHED-TTL:PT1H
BEGIN:VEVENT"""
    IcsFooter = """END:VEVENT
    END:VCALENDAR"""
    
    IcsFinal += IcsHeader
    # for JsonObject in range(0, RawJsonLen):
    for JsonObject in range(0, 10):
        # print(JsonName[JsonObject][3], datetime.fromtimestamp(JsonName[JsonObject][3]))
        EventTitle = "Red Alert in "
        for Place in JsonName[JsonObject][2]:
            EventTitle += Place
            EventUnixTime = JsonName[JsonObject][3]
            EventUid = str(EventUnixTime)+Place
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
LOCATION:$LOCATION
STATUS:CONFIRMED
END:VEVENT""")
            IcsTemplateFill = IcsTemplate.substitute(
                UID = EventUid,
                TITLE = EventSummary,
                DTSTART = EventDTSTART,
                DTEND = EventDTEND,
                LOCATION = EventLOCATION
            )
            IcsFinal += IcsTemplateFill
    IcsFinal += IcsFooter
    return(IcsFinal)

def WriteIcsToFile(IcsContent, Path, Filename):
    with open (Path / Filename, "w", encoding="utf-8") as IcsOnDisk:
        IcsOnDisk.write(IcsContent)


    FilePath = ""  
    return(FilePath)





GlobalProdFolder = FolderManagement()
GlobalTx = LocalTime(GlobalProdFolder)
GlobalJsonFile = DownloadJsonDict(SourceJson, GlobalProdFolder, "Test")
IcsContent = JsonIntoIcs(GlobalJsonFile)
WriteIcsToFile(IcsContent, GlobalProdFolder, "lol.ics")



print(IcsContent)
# TESTDATE = 1774011703
# testdate = datetime.fromtimestamp(TESTDATE+900)
# print(testdate)
# print(datetime.strftime(testdate, "%Y%m%dT%H%M%S"))