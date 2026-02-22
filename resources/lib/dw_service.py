from resources.lib.dw_api import DWGraphQL
from resources.lib.gql_queries import *

app_name="kodi"

class DWService:
    def __init__(self, api: DWGraphQL):
        self.api = api

    def get_show_list(self, language_id):
        variables = {"lang": language_id, "appName": app_name} 
        data = self.api.execute("getShowList", GET_SHOW_LIST, variables)

        overview = (data.get("programsOverview") or {})
        video = overview.get("videoPrograms") or []
        audio = overview.get("audioPrograms") or []
        return {"videoPrograms": video, "audioPrograms": audio}

    def get_show_episodes(self, show_id: int):
        variables = {
            "keys": [{"id": int(show_id), "type": "UNIFIED_PROGRAM"}],
            "amount": 16,
            "appName": app_name,
        }

        data = self.api.execute("getShowEpisodes", GET_SHOWS_EPISODES, variables)

        contents = data.get("contents") or []
        if not contents:
            return []

        return (contents[0] or {}).get("moreContentsFromUnifiedProgram") or []

    def get_video_details(self, tracking_id: int):
        variables = {"id": tracking_id, "app_name": app_name}
        data = self.api.execute("getVideoDetails", GET_VIDEO_DETAILS, variables)

        content = data.get("content") or []
        if not content:
            return []
        
        return content

    def get_live_tv(self):
        variables = {"channelNames": [], "app_name": app_name}
        data = self.api.execute("getLiveTV", GET_LIVE_TV, variables)

        livestream_channels = data.get("livestreamChannels") or []
        if not livestream_channels:
            return []

        return livestream_channels