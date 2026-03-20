import os, requests, tzdata
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

def DownloadJson(JsonUrl, DownloadPath):
    rGetJson = requests.get(JsonUrl,
                          )
    if rGetJson.status_code != 200:
        print("Failed")
    else:
        print("Success")
        with open(DownloadPath + "sourcejson.json", "w", encoding="utf-8") as JsonFile:
            JsonFile.write(rGetJson.content)



GlobalPodFolder = FolderManagement()
LocalTime(GlobalPodFolder)
DownloadJson(SourceJson, GlobalPodFolder)


# DownloadJson(SourceJson)