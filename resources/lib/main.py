from codequick import Route, Listitem, run, Script, utils
from resources.lib.EndPoints import EndPoints
from resources.lib.OnDemand import OnDemand
from resources.lib.LiveTv import LiveTv
import simplejson as json
import requests
import xbmcaddon
        
language_id = Script.setting["language"].upper()
addon = xbmcaddon.Addon()
_ = addon.getLocalizedString


@Route.register
def root(plugin):  
    # Live TV
    item = Listitem()
    item.label = _(32006)
    item.set_callback(LiveTv.get_live_tv_channels)
    yield item

    # Shows
    item = Listitem()
    item.label = _(32009)
    item.set_callback(OnDemand.get_program_list, language_id=language_id,content_type="video")
    yield item

    # Podcast
    item = Listitem()
    item.label = _(32023)
    item.set_callback(OnDemand.get_program_list, language_id=language_id, content_type="audio")
    yield item