class EndPoints:
    BASE_URL = "https://api.dw.com/api"
    NAVIGATION = f"{BASE_URL}/navigation/{{language}}?product=smarttv&platform=androidtv"
    VIDEO_DETAIL = f"{BASE_URL}/detail/video/{{video_id}}"
    TOPICS = f"{BASE_URL}/epg/programgroups/topics/{{language_id}}"
    VIDEO_LIST = f"{BASE_URL}/list/video/recent/{{language_id}}/program/{{program_id}}?pageIndex={{page_number}}"
    PROGRAM_LIST = f"{BASE_URL}/epg/list/program/{{language_id}}"