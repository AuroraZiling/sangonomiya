character_5_w_list = ["七七", "提纳里", "刻晴", "迪卢克", "莫娜", "琴"]
character_5_list = ["纳西妲", "赛诺", "妮露", "钟离", "宵宫", "可莉", "枫原万叶", "荒泷一斗", "夜兰", "魈", "神里绫华", "神里绫人",
                    "温迪", "八重神子", "甘雨", "申鹤", "优菈", "阿贝多", "胡桃", "达达利亚", "珊瑚宫心海", "雷电将军",
                    "七七", "刻晴", "迪卢克", "莫娜", "提纳里", "琴"]
character_4_list = ["坎蒂丝", "柯莱", "鹿野院平藏", "久岐忍", "云堇", "五郎", "托马", "九条裟罗", "罗莎莉亚", "早柚", "雷泽",
                    "凝光", "菲谢尔", "班尼特", "烟绯", "重云", "芭芭拉", "迪奥娜", "砂糖", "诺艾尔", "凯亚", "辛焱",
                    "香菱", "北斗", "行秋", "安柏", "丽莎"]
weapon_5_w_list = ["天空之翼", "天空之卷", "天空之脊", "天空之傲", "风鹰剑", "四风原典", "和璞鸢", "狼的末路", "天空之刃"]
weapon_5_list = ['雾切之回光', '斫峰之刃', '苍古自由之誓', '天空之刃', '磐岩结绿', '波乱月白经津', '风鹰剑',
                 '松籁响起之时', '天空之傲', '无工之剑', '狼的末路', '赤角石溃杵', '冬极白星', '天空之翼', '猎人之径',
                 '阿莫斯之弓', '终末嗟叹之诗', '飞雷之弦振', '若水', '神乐之真意', '不灭月华', '四风原典', '天空之卷',
                 '尘世之锁', '贯虹之槊', '息灾', '薙草之稻光', '护摩之杖', '和璞鸢', '天空之脊', '猎人之径']
weapon_4_list = ['笛剑', '祭礼剑', '匣里龙吟', '西风剑', '暗巷闪光', '钟剑', '千岩古剑', '恶王丸', '雨裁', '祭礼大剑',
                 '西风大剑', '祭礼弓', '绝弦', '幽夜华尔兹', '西风猎弓', '弓藏', '曚云之月', '暗巷猎手', '西风秘典',
                 '祭礼残章', '昭心', '暗巷的酒与诗', '流浪乐章', '西风长枪', '断浪长鳍', '匣里灭辰', '千岩长枪']
weapon_3_list = ['冷刃', '飞天御剑', '黎明神剑', '以理服人', '沐浴龙血的剑', '铁影阔剑', '神射手之誓', '鸦羽弓', '弹弓',
                 '魔导诸论', '讨龙英杰谭', '翡玉法球', '甲级宝珏', '白缨枪', '黑缨枪', '钺矛']


class Analysis:
    def __init__(self, target_uid, given_data=None):
        self.given_data = given_data if given_data else {}
        self.target_uid = target_uid
        self.ori_data_list, self.data_list, self.length_list = {}, {}, {}
        self.ori_data_list[target_uid] = {"100": [], "200": [], "301": [], "400": [], "302": []}
        self.length_list[target_uid] = {"100": 0, "200": 0, "301": 0, "400": 0, "302": 0}
        self.data_list[target_uid] = {}
        for each_mode in ["100", "200", "301", "400", "302"]:
            try:
                self.ori_data_list[target_uid][each_mode] = self.given_data[target_uid][f"data_{each_mode}"]["data"]
                self.length_list[target_uid][each_mode] = len(self.given_data[target_uid][f"data_{each_mode}"]["data"])
            except KeyError:
                continue
        for each in self.ori_data_list[target_uid].keys():
            tmp_list_5, tmp_list_4 = [], []
            self.data_list[target_uid][each] = {}
            for each_data_pos in range(len(self.ori_data_list[target_uid][each])):
                each_data = self.ori_data_list[target_uid][each][each_data_pos]
                if each_data[1] in character_5_list or each_data[1] in weapon_5_list:
                    tmp_list_5.append(each_data[1] + f"[{self.length_list[target_uid][each] - each_data_pos}]")
                elif each_data[1] in character_4_list or each_data[1] in weapon_4_list:
                    tmp_list_4.append(each_data[1] + f"[{self.length_list[target_uid][each] - each_data_pos}]")
            self.data_list[target_uid][each] = {"5": tmp_list_5, "4": tmp_list_4}

    def get_5(self, pray_mode):
        return self.data_list[self.target_uid][pray_mode]["5"], len(self.data_list[self.target_uid][pray_mode]["5"])

    def get_4(self, pray_mode):
        return self.data_list[self.target_uid][pray_mode]["4"], len(self.data_list[self.target_uid][pray_mode]["4"])

    def get_3(self, pray_mode):
        return len(self.ori_data_list[self.target_uid][pray_mode]) - self.get_5(pray_mode)[-1] - self.get_4(pray_mode)[-1]

    def guarantee(self, pray_mode):
        guarantee_model = ""
        current_data_length = self.length_list[self.target_uid][pray_mode]
        if pray_mode == "301":
            if not current_data_length:
                return "暂未出现5星角色"
            guarantee_data = self.get_5(pray_mode)
            try:
                nearest_data = [i.replace(']', '') for i in guarantee_data[0][0].split("[")]
            except IndexError:
                return "暂未出现5星角色"
            if nearest_data[0] in character_5_w_list:
                guarantee_model += "情况: 小保底歪了/直接进入大保底"
                guarantee_model += "(由于最近一次5星角色是提纳里，以下判断可能有误)" if nearest_data[0] == "提纳里" else ""
                guarantee_model += f"\n最近一次在第{nearest_data[1]}抽得到{nearest_data[0]}"
                guarantee_model += f", 意味着将在第{int(nearest_data[1]) + 90}抽之前必出当期UP"
                guarantee_model += f"\n当前已经{current_data_length}/{int(nearest_data[1]) + 90}抽, 还差{int(nearest_data[1]) + 90 - current_data_length}抽"
                guarantee_model += f"\n预计最多需要{int(nearest_data[1]) + 90 - current_data_length}个纠缠之缘, 约等于{(int(nearest_data[1]) + 90 - current_data_length) * 160}原石"
            else:
                guarantee_model += "情况: 保底重置"
                guarantee_model += "(由于最近一次5星角色是提纳里，以下判断可能有误)" if nearest_data[0] == "提纳里" else ""
                guarantee_model += f"\n最近一次在第{nearest_data[1]}抽得到{nearest_data[0]}"
                guarantee_model += f"\n(第{int(nearest_data[1]) + 90}抽之前有50%的概率出当期UP，在第{int(nearest_data[1]) + 180}抽之前必出当期UP)"
                guarantee_model += f"\n小保底: 当前已经{current_data_length}/{int(nearest_data[1]) + 90}抽, 还差{int(nearest_data[1]) + 90 - current_data_length}抽"
                guarantee_model += f"\n预计最多需要{int(nearest_data[1]) + 90 - current_data_length}个纠缠之缘, 约等于{(int(nearest_data[1]) + 90 - current_data_length) * 160}原石"
                guarantee_model += f"\n大保底: 当前已经{current_data_length}/{int(nearest_data[1]) + 180}抽, 还差{int(nearest_data[1]) + 180 - current_data_length}抽"
                guarantee_model += f"\n预计最多需要{int(nearest_data[1]) + 180 - current_data_length}个纠缠之缘, 约等于{(int(nearest_data[1]) + 180 - current_data_length) * 160}原石"
            return guarantee_model
        elif pray_mode == "302":
            if not current_data_length:
                return "暂未出现5星武器"
            guarantee_data = self.get_5(pray_mode)
            try:
                nearest_data = [i.replace(']', '') for i in guarantee_data[0][0].split("[")]
            except IndexError:
                return "暂未出现5星武器"
            if nearest_data[0] in weapon_5_w_list:
                guarantee_model += "情况: 小保底歪了/直接进入大保底"
                guarantee_model += f"\n最近一次在第{nearest_data[1]}抽得到{nearest_data[0]}"
                guarantee_model += f", 意味着将在第{int(nearest_data[1]) + 80}抽之前必出当期UP"
                guarantee_model += f"\n当前已经{current_data_length}/{int(nearest_data[1]) + 80}抽, 还差{int(nearest_data[1]) + 80 - current_data_length}抽"
                guarantee_model += f"\n预计最多需要{int(nearest_data[1]) + 80 - current_data_length}个纠缠之缘, 约等于{(int(nearest_data[1]) + 80 - current_data_length) * 160}原石"
            else:
                guarantee_model += "情况: 保底重置"
                guarantee_model += f"\n最近一次在第{nearest_data[1]}抽得到{nearest_data[0]}"
                guarantee_model += f", 意味着将在第{int(nearest_data[1]) + 80}抽之前有50%的概率出当期UP，在第{int(nearest_data[1]) + 160}抽之前必出当期UP"
                guarantee_model += f"\n小保底: 当前已经{current_data_length}/{int(nearest_data[1]) + 80}抽, 还差{int(nearest_data[1]) + 80 - current_data_length}抽"
                guarantee_model += f"\n预计最多需要{int(nearest_data[1]) + 80 - current_data_length}个纠缠之缘, 约等于{(int(nearest_data[1]) + 80 - current_data_length) * 160}原石"
                guarantee_model += f"\n大保底: 当前已经{current_data_length}/{int(nearest_data[1]) + 160}抽, 还差{int(nearest_data[1]) + 160 - current_data_length}抽"
                guarantee_model += f"\n预计最多需要{int(nearest_data[1]) + 160 - current_data_length}个纠缠之缘, 约等于{(int(nearest_data[1]) + 160 - current_data_length) * 160}原石"
            return guarantee_model
        elif pray_mode == "200":
            if not current_data_length:
                return "暂未出现5星"
            guarantee_data = self.get_5(pray_mode)
            nearest_data = [i.replace(']', '') for i in guarantee_data[0][0].split("[")]
            if nearest_data[0] in weapon_5_list or nearest_data[0] in character_5_list:
                guarantee_model += f"最近一次在第{nearest_data[1]}抽得到{nearest_data[0]}"
                guarantee_model += f", 意味着将在第{int(nearest_data[1]) + 90}抽之前必出五星"
                guarantee_model += f"\n当前已经{current_data_length}/{int(nearest_data[1]) + 90}抽, 还差{int(nearest_data[1]) + 90 - current_data_length}抽"
                guarantee_model += f"\n预计最多需要{int(nearest_data[1]) + 90 - current_data_length}个纠缠之缘, 约等于{(int(nearest_data[1]) + 90 - current_data_length) * 160}原石"
            return guarantee_model
        return "暂未支持新手祈愿分析"
