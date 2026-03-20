import os, requests
from pathlib import Path
from settings import SourceJson
from datetime import datetime, date, timezone, tzinfo
from pytz import timezone    



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

def FileName(Folder):
    now = datetime.now(timezone."Asia/Jerusalem")



def DownloadJson(JsonUrl, DownloadPath):
    rGetJson = requests.get(JsonUrl,
                          )
    if rGetJson.status_code != 200:
        print("Failed")
    else:
        # print(rGetJson.content)
        print("Success")

FolderManagement()
DownloadJson(SourceJson)