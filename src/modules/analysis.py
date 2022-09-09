character_5_w_list = ["七七", "刻晴", "迪卢克", "莫娜", "琴"]
character_5_list = ["提纳里", "钟离", "宵宫", "可莉", "枫原万叶", "荒泷一斗", "夜兰", "魈", "神里绫华", "神里绫人",
                    "温迪", "八重神子", "甘雨", "申鹤", "优菈", "阿贝多", "胡桃", "达达利亚", "珊瑚宫心海", "雷电将军",
                    "七七", "刻晴", "迪卢克", "莫娜", "琴"]
character_4_list = ["柯莱", "鹿野院平藏", "久岐忍", "云堇", "五郎", "托马", "九条裟罗", "罗莎莉亚", "早柚", "雷泽",
                    "凝光", "菲谢尔", "班尼特", "烟绯", "重云", "芭芭拉", "迪奥娜", "砂糖", "诺艾尔", "凯亚", "辛焱",
                    "香菱", "北斗", "行秋", "安柏", "丽莎"]
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
    def __init__(self, given_data=None, pray_mode=None):
        if given_data is None:
            given_data = []
        self.given_data = given_data
        self.pray_mode = pray_mode
        self.list_5, self.list_4 = [], []
        self.given_data_length = len(given_data)
        for each in range(len(self.given_data)):
            if self.given_data[each][1] in character_5_list or self.given_data[each][1] in weapon_5_list:
                self.list_5.append(self.given_data[each][1] + f"[{len(given_data)-each}]")
            elif self.given_data[each][1] in character_4_list or self.given_data[each][1] in weapon_4_list:
                self.list_4.append(self.given_data[each][1] + f"[{len(given_data)-each}]")

    def get_5(self):
        return self.list_5, len(self.list_5)

    def get_4(self):
        return self.list_4, len(self.list_4)

    def get_3(self):
        return len(self.given_data) - len(self.list_5) - len(self.list_4)

    def guarantee(self):
        if self.pray_mode == "301" and len(self.list_5):
            guarantee_model = ""
            guarantee_data = self.get_5()
            nearest_data = [i.replace(']', '') for i in guarantee_data[0][0].split("[")]
            if nearest_data[0] in character_5_w_list:
                guarantee_model += "情况: 小保底歪了/直接进入大保底"
                guarantee_model += f"\n最近一次在第{nearest_data[1]}抽得到{nearest_data[0]}"
                guarantee_model += f", 意味着将在{int(nearest_data[1])+90}抽之前必出当期UP"
                guarantee_model += f"\n当前已经{self.given_data_length}/{int(nearest_data[1])+90}抽, 还差{int(nearest_data[1])+90-self.given_data_length}抽"
                guarantee_model += f"\n预计最多需要{int(nearest_data[1])+90-self.given_data_length}个纠缠之缘, 约等于{(int(nearest_data[1])+90-self.given_data_length)*160}原石"
            return guarantee_model
        return "暂未支持除了角色活动祈愿之外的分析"
