from codequick import Route, Listitem, run, Script, utils, Resolver
from resources.lib.dw_api import DWGraphQL
from resources.lib.dw_service import DWService
from resources.lib.EndPoints import EndPoints
import simplejson as json
import requests

api = DWGraphQL()
svc = DWService(api)

class OnDemand:
    @Route.register
    def get_program_list(plugin, language_id, content_type):
        content_type = "videoPrograms" if content_type == "video" else "audioPrograms"
        shows = svc.get_show_list(language_id)[content_type]
        for show in shows:
            item = Listitem()
            item.label = show.get("name", "")
            item.info["plot"] = show.get("teaser") or ""

            img = (show.get("mainContentImage") or {}).get("staticUrl")
            img = img.replace("${formatId}", "604")
            if img:
                item.art["thumb"] = img
                item.art["fanart"] = img

            program_id = show.get("id")

            item.set_callback(OnDemand.get_video_list, program_id=program_id)

            yield item

    @Route.register
    def get_video_list(plugin, program_id):
        videos = svc.get_show_episodes(program_id)
        for video in videos:
            item = Listitem()
            item.label = video.get("name", "")
            item.info["plot"] = video.get("teaser") or ""
            item.info["duration"] = video.get("duration") or ""
            item.info["premiered"] = video.get("contentDate") or ""

            img = video.get("posterImageUrl") or {}
            if img:
                item.art["thumb"] = img
                item.art["fanart"] = img

            video_id = video.get("id", "")
            item.set_callback(OnDemand.play_video, video_id=video_id)
            yield item

    @Resolver.register
    def play_video(plugin, video_id):
        return svc.get_video_details(video_id).get("hlsVideoSrc") or svc.get_video_details(video_id).get("mp3Src")