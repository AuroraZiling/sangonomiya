def jsonToOriginal(uigf_data):
    output_100, output_200, output_301, output_400, output_302 = [], [], [], [], []
    data = uigf_data["list"]
    for each in data:
        if each["gacha_type"] == "100":
            output_100.append([each["item_type"], each["name"], each["time"]])
        elif each["gacha_type"] == "200":
            output_200.append([each["item_type"], each["name"], each["time"]])
        elif each["gacha_type"] == "301":
            output_301.append([each["item_type"], each["name"], each["time"]])
        elif each["gacha_type"] == "400":
            output_400.append([each["item_type"], each["name"], each["time"]])
        elif each["gacha_type"] == "302":
            output_302.append([each["item_type"], each["name"], each["time"]])
    return {"100": output_100, "200": output_200, "301": output_301, "400": output_400, "302": output_302}