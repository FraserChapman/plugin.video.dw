from codequick import Route, Listitem, run, Script, utils, Resolver
from resources.lib.dw_api import DWGraphQL
from resources.lib.dw_service import DWService
from resources.lib.EndPoints import EndPoints
import simplejson as json
import requests

api = DWGraphQL()
svc = DWService(api)

class LiveTv:
    @Route.register
    def get_live_tv_channels(plugin):
        channels = svc.get_live_tv()
        for channel in channels:
            item = Listitem()
            item.label = channel.get("name", "")
            timeslots = channel.get("nextTimeSlots", [])
            if timeslots:
                first_slot = timeslots[0]
                program = first_slot.get("program", {})
                program_element = first_slot.get("programElement", {})

                title = program.get("title", "")
                subtitle = program.get("subTitle", "").strip()
                teaser = program.get("teaser", "")

                # Construir plot bonito tipo EPG
                plot = f"[B]{title}[/B]\n"
                if subtitle:
                    plot += f"{subtitle}\n\n"

                plot += teaser

                item.info["plot"] = plot

                # Imagen
                image = program.get("mainContentImage", {})
                if image:
                    img_url = image.get("staticUrl", "").replace("${formatId}", "605")
                    item.art["thumb"] = img_url
                    item.art["fanart"] = img_url
            
            item.property["IsLive"] = "true"
            item.set_path(channel.get("livestreamUrl"))
            yield item