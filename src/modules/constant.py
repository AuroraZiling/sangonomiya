APP_VERSION = "8.1.0"
UI_VERSION = "0.9.0"

UIGF_GACHATYPE = {"100": "100", "200": "200", "301": "301", "400": "301", "302": "302"}
UIGF_VERSION = ["UIGF(Json) v2.2", "UIGF(Json) v2.3"]
UIGF_VERSION_EXPORT = {"UIGF(Json) v2.2": "v2.2", "UIGF(Json) v2.3": "v2.3"}
UIGF_DATA_MODEL = {"info": {"uid": "", "lang": "zh-cn", "export_time": ""}, "list": []}
GACHATYPE = {"新手祈愿": "100", "常驻祈愿": "200", "角色活动祈愿": "301", "角色活动祈愿-2": "400", "武器祈愿": "302"}

SOFTWARE_ANNOUNCEMENT_URL = "https://raw.staticdn.net/AuroraZiling/sangonomiya.Metadata/main/announcement.txt"

CHARACTER_URL = "https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/home/content/list?app_sn=ys_obc&channel_id=25"
PERMANENT_CHARACTER_URL = "https://raw.staticdn.net/AuroraZiling/sangonomiya.Metadata/main/metadata.json"
WEAPON_URL = "https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/home/content/list?app_sn=ys_obc&channel_id=5"
UIGF_ITEM_ID_URL = "https://api.uigf.org/dict/genshin/{lang}.json"
UIGF_MD5_URL = "https://api.uigf.org/dict/genshin/md5.json"

COLOR_MAPPING = {"3": "#1E90FF", "4": "#7B68EE", "5": "#FFA500", "X": "#FF0000"}

ANNOUNCE_CURRENT_UP_URL = "https://api-takumi.mihoyo.com/common/blackboard/ys_obc/v1/gacha_pool?app_sn=ys_obc"

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

UPDATE_URL = "https://api.github.com/repos/AuroraZiling/sangonomiya/releases"

FONT_MAPPING = ["TeyvatNeue-Regular-1.002.otf", "InazumaNeue-Regular-1.000.otf", "SumeruNeue-Regular-0.007.otf", "DeshretNeue-Regular-1.002.otf", "KhaenriahNeue-Regular-2.000.otf", "KhaenriahNeue-Chasm-2.000.otf"]
FONT_NAME_MAPPING = ["Teyvat Neue", "Inazuma Neue", "Sumeru Neue", "Deshret Neue", "Khaenriah Neue", "Khaenriah Neue Chasm"]

GITHUB_RELEASE_URL = "https://api.github.com/repos/AuroraZiling/sangonomiya/releases/latest"

UPDATE_SCRIPT_MODEL = """
echo "DON'T CLOSE THIS WINDOW"
powershell -command \"Start-Sleep -s 3\"
powershell -command \"Get-childitem -Path .. -exclude *.json,*.zip,*.bat,temp,data -Recurse | Remove-Item -Force -Recurse\"
powershell -command \"Expand-Archive -Path .\\{filename} -DestinationPath ..\\ -Force\"
powershell -command \"Remove-Item -Path .\\{filename}\"
cd ../.
start .\\"Sangonomiya.exe\"
powershell -command \"Remove-Item -Path .\\temp\\update.bat\"
exit
"""

UIGF_3_JSON_SCHEMA = {

}