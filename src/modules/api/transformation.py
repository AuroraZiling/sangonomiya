import pickle

UIGF_GACHATYPE = {"100": "100", "200": "200", "301": "301", "400": "301", "302": "302"}


def jsonToOriginal(uigf_data):
    output_100, output_200, output_301, output_400, output_302 = [], [], [], [], []
    data = uigf_data["list"]
    for each in data:
        if each["gacha_type"] == "100":
            output_100.append([each["item_type"], each["name"], each["time"], each['id'], each['rank_type']])
        elif each["gacha_type"] == "200":
            output_200.append([each["item_type"], each["name"], each["time"], each['id'], each['rank_type']])
        elif each["gacha_type"] == "301":
            output_301.append([each["item_type"], each["name"], each["time"], each['id'], each['rank_type']])
        elif each["gacha_type"] == "400":
            output_400.append([each["item_type"], each["name"], each["time"], each['id'], each['rank_type']])
        elif each["gacha_type"] == "302":
            output_302.append([each["item_type"], each["name"], each["time"], each['id'], each['rank_type']])
    return {"100": output_100, "200": output_200, "301": output_301, "400": output_400, "302": output_302}


def OriginalToJson(basedir, paths):
    opt = []
    for path in paths:
        data = pickle.loads(open(basedir + path, 'rb').read())
        for each in data:
            opt.append({"count": "1", "gacha_type": path[:3], "id": each[3], "item_type": each[0], "name": each[1],
                        "rank_type": each[4], "time": each[2], "uigf_gacha_type": UIGF_GACHATYPE[path[:3]]})
    return opt
