import os, requests, tzdata, json, pytz
# from ics import Calendar, Event
from pathlib import Path
from zoneinfo import ZoneInfo
from settings import SourceJson
from datetime import datetime, date, timezone, tzinfo
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


def JsonIntoIcs(JsonName, IcsName):
    RawJsonLen = len(JsonName)
    for JsonObject in range(0, RawJsonLen):
        # print(JsonName[JsonObject][3], datetime.fromtimestamp(JsonName[JsonObject][3]))
        EventTitle = "Red Alert in "
        for Place in JsonName[JsonObject][2]:
            EventTitle += Place
        EventUnixTime = JsonName[JsonObject][3]
        EventLocalTIme = datetime.fromtimestamp(JsonName[JsonObject][3])
        print(EventTitle, EventUnixTime, EventLocalTIme)

    IcsHeader = """
    BEGIN:VCALENDAR
    PRODID:-//BlueGG1 Cal//GG1 Calendar 1.0//EN
    VERSION:2.0
    CALSCALE:GREGORIAN
    METHOD:PUBLISH
    X-WR-CALNAME:Red Alerts
    X-WR-TIMEZONE:UTC
    X-WR-CALDESC:Duck and Cover
    """ #keep it utc and add the +2 later(??)
    


    #         PodcastEpisodeTitle = str(abs(i-EpisodesInJson))+" "+RawJson["podcast"]["episodes"][i]["title"]
    #         PodcastEpisodeNotes = RawJson["podcast"]["episodes"][i]["show_notes"]
    #         PodcastEpisodePatUrl = RawJson["podcast"]["episodes"][i]["url"]
    #         PodcastEpisodeFileName = str(abs(i-EpisodesInJson)) + " " + PodcastEpisodeTitle.strip() + ".mp3"
    #         PodcastEpisodePublished = RawJson["podcast"]["episodes"][i]["published"]
    #         ExampleRssFromBBC = Template("""    <item>
    #         <title>$TemplateTitle</title>
    #         <description>$TemplateDescription</description>
    #         <itunes:subtitle>pod feed.</itunes:subtitle>
    #         <itunes:summary>pod feed.</itunes:summary>
    #         <itunes:explicit>true</itunes:explicit>
    #         <itunes:author>BBC</itunes:author>
    #         <link>https://www.bbc.co.uk</link>
    #         <pubDate>$TemplatePubDate</pubDate>
    #         <enclosure url="$TemplateUrl" type="audio/mpeg"/>
    #     </item>\r\n""")
    #         # print(ExampleRssFromBBC)
    #         ReadTemplateRss = ExampleRssFromBBC.substitute(
    #             TemplateTitle = PodcastEpisodeTitle.replace("&","&amp;"),
    #             # TemplateDescription = (PodcastEpisodeNotes.replace("&","&amp;")),
    #             TemplateDescription = re.sub('<[^<]+?>', "  ", PodcastEpisodeNotes),
    #             TemplatePubDate = PodcastEpisodePublished,
    #             # TemplateUrl = PodcastEpisodePatUrl
    #             TemplateUrl = PodcastEpisodePatUrl.replace("&","&amp;")
    #             )
    #         XmlRssFinal += ReadTemplateRss
    #     XmlRssFooter = """    </channel>
    # </rss>"""
    #     XmlRssFinal +=XmlRssFooter


    IcsFooter = """
    END:VEVENT
    END:VCALENDAR
    """

    return()




GlobalPodFolder = FolderManagement()
GlobalTx = LocalTime(GlobalPodFolder)
GlobalJsonFile = DownloadJsonDict(SourceJson, GlobalPodFolder, "Test")
JsonIntoIcs(GlobalJsonFile, "test2")