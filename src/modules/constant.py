UIGF_GACHATYPE = {"100": "100", "200": "200", "301": "301", "400": "301", "302": "302"}
UIGF_VERSION = "v2.2"
UIGF_DATA_MODEL = {"info": {"uid": "", "lang": "zh-cn", "export_time": ""}, "list": []}
GACHATYPE = {"新手祈愿": "100", "常驻祈愿": "200", "角色活动祈愿": "301", "角色活动祈愿-2": "400", "武器祈愿": "302"}

ANNOUNCE_REQUEST_URL = "https://hk4e-api-static.mihoyo.com/common/hk4e_cn/announcement/api/getAnnContent?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&bundle_id=hk4e_cn&platform=pc&region=cn_gf01&level=60&channel_id=1"
ANNOUNCE_ICON_REQUEST_URL = "https://hk4e-api.mihoyo.com/common/hk4e_cn/announcement/api/getAnnList?game=hk4e&game_biz=hk4e_cn&lang=zh-cn&auth_appid=announcement&authkey_ver=1&bundle_id=hk4e_cn&channel_id=1&level=60&platform=pc&region=cn_gf01&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&sign_type=2&uid=1"
HTML_MODEL = '''
<!DOCTYPE html>
<html>
  <head>
  <style>
    body::-webkit-scrollbar {display: none;}
    {css}
  </style>
  </head>
  <body style="background-color: transparent;">
    <article class="markdown-body" style="background-color: transparent;">
        {content}
    </article>
  </body>
</html>
'''