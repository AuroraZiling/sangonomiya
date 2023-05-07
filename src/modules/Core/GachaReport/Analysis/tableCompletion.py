def originalTableDataToComplete(data):
    for eachData in ["200", "301", "302"]:
        for index, unit in enumerate(data[eachData]):
            unit.insert(0, str(len(data[eachData])-index))
            unit.append("单抽")
        time_tmp = [i[3] for i in data[eachData]]
        pos = 0
        while pos < len(time_tmp) - 9:
            if time_tmp[pos] == time_tmp[pos + 1]:
                for i in range(pos, pos + 10):
                    data[eachData][i][-1] = f"十连-{10 - i + pos}"
                pos += 9
            pos += 1
    return data