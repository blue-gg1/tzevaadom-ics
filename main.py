import os, requests, tzdata, json
# from ics import Calendar, Event
from pathlib import Path
from zoneinfo import ZoneInfo
from settings import SourceJson
from datetime import datetime, date, timezone, tzinfo
# from pytz import timezone    



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


def JsonIntoIcs(JsonName, IcsName):
    RawJsonLen = len(JsonName)
    for JsonObject in range(0, RawJsonLen):
        print(JsonName[JsonObject][3], datetime.fromtimestamp(JsonName[JsonObject][3])) # the unix time is local and not UTC




GlobalPodFolder = FolderManagement()
GlobalTx = LocalTime(GlobalPodFolder)
GlobalJsonFile = DownloadJsonDict(SourceJson, GlobalPodFolder, "Test")
JsonIntoIcs(GlobalJsonFile, "test2")