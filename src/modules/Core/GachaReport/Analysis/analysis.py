from PySide6.QtCharts import QPieSeries, QPieSlice, QChart
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QFont

from qfluentwidgets import isDarkTheme
from ....Scripts.Utils import tools
from ....constant import COLOR_MAPPING

utils = tools.Tools()

class Analysis:
    def __init__(self, data):
        self.data = data
        self.total_amount = 0
        self.star_5 = []
        self.star_5_amount = 0
        self.star_4 = []
        self.star_4_amount = 0
        self.star_3_amount = 0
        self.chart = QChart()
        if self.data:
            self.total_amount = int(self.data[0]["order"])
            self.star_5 = [f"[{unit['order']}]{unit['name']}" for unit in self.data if unit['rank_type'] == "5"]
            self.star_5_amount = len(self.star_5)
            self.star_4 = [f"[{unit['order']}]{unit['name']}" for unit in self.data if unit['rank_type'] == "4"]
            self.star_4_amount = len(self.star_4)
            self.star_3_amount = len([unit for unit in self.data if unit['rank_type'] == "3"])

            self.chartSeries = QPieSeries()
            self.chart5Star = QPieSlice()
            self.chart4Star = QPieSlice()
            self.chart3Star = QPieSlice()

            self.characterList = utils.read_metadata("character")
            self.weaponList = utils.read_metadata("weapon")
            self.permanentList = utils.read_metadata("permanent")

    def get_total_amount_to_string(self):
        return str(self.total_amount)

    def get_star_5_to_string(self):
        return ' '.join(self.star_5)

    def get_star_5_amount_to_string(self):
        return str(self.star_5_amount)

    def get_star_4_to_string(self):
        return ' '.join(self.star_4)

    def get_star_4_amount_to_string(self):
        return str(self.star_4_amount)

    def get_star_3_amount_to_string(self):
        return str(self.star_3_amount)

    def get_star_5_percent_to_string(self):
        if self.total_amount:
            return f"{round(self.star_5_amount / self.total_amount, 2)}%"
        else:
            return "0%"

    def get_star_4_percent_to_string(self):
        if self.total_amount:
            return f"{round(self.star_4_amount / self.total_amount, 2)}%"
        else:
            return "0%"

    def get_guarantee(self, data_type):
        guarantee_text = ""
        nearest_5_star = {}
        additional_fix = 80 if data_type == "武器祈愿" else 90
        is_permanent_pool = True if data_type == "常驻祈愿" else False
        for unit in self.data:
            if unit['rank_type'] == "5":
                nearest_5_star = unit
                break
        if nearest_5_star and not is_permanent_pool:
            if nearest_5_star["name"] in self.permanentList:
                guarantee_text += "情况: 小保底歪了/直接进入大保底"
                guarantee_text += f"\n最近一次在第{nearest_5_star['order']}抽得到{nearest_5_star['name']}"
                guarantee_text += f"\n将在第{int(nearest_5_star['order']) + additional_fix}抽之前必出当期UP"
                guarantee_text += f"\n当前已经{self.total_amount}/{int(nearest_5_star['order']) + additional_fix}抽, 还差{int(nearest_5_star['order']) + additional_fix - self.total_amount}抽"
                guarantee_text += f"\n预计最多需要{int(nearest_5_star['order']) + additional_fix - self.total_amount}个纠缠之缘, 约等于{(int(nearest_5_star['order']) + additional_fix - self.total_amount) * 160}原石"
            elif nearest_5_star["name"] not in self.permanentList:
                guarantee_text += "情况: 保底重置/等待小保底"
                guarantee_text += f"\n最近一次在第{nearest_5_star['order']}抽得到{nearest_5_star['name']}"
                guarantee_text += f"\n(第{int(nearest_5_star['order']) + additional_fix}抽之前有50%的概率出当期UP，在第{int(nearest_5_star['order']) + 2 * additional_fix}抽之前必出当期UP)"
                guarantee_text += f"\n小保底: 当前已经{self.total_amount}/{int(nearest_5_star['order']) + additional_fix}抽, 还差{int(nearest_5_star['order']) + additional_fix - self.total_amount}抽"
                guarantee_text += f"\n预计最多需要{int(nearest_5_star['order']) + additional_fix - self.total_amount}个纠缠之缘, 约等于{(int(nearest_5_star['order']) + additional_fix - self.total_amount) * 160}原石"
                guarantee_text += f"\n大保底: 当前已经{self.total_amount}/{int(nearest_5_star['order']) + 2 * additional_fix}抽, 还差{int(nearest_5_star['order']) + 2 * additional_fix - self.total_amount}抽"
                guarantee_text += f"\n预计最多需要{int(nearest_5_star['order']) + 2 * additional_fix - self.total_amount}个纠缠之缘, 约等于{(int(nearest_5_star['order']) + 2 * additional_fix - self.total_amount) * 160}原石"
        elif is_permanent_pool:
            guarantee_text += f"最近一次在第{nearest_5_star['order']}抽得到{nearest_5_star['name']}"
            guarantee_text += f"\n将在第{int(nearest_5_star['order']) + 90}抽之前必出五星"
            guarantee_text += f"\n当前已经{self.total_amount}/{int(nearest_5_star['order']) + additional_fix}抽, 还差{int(nearest_5_star['order']) + additional_fix - self.total_amount}抽"
            guarantee_text += f"\n预计最多需要{int(nearest_5_star['order']) + additional_fix - self.total_amount}个相遇之缘, 约等于{(int(nearest_5_star['order']) + additional_fix - self.total_amount) * 160}原石"
        elif not nearest_5_star:
            guarantee_text = "暂无数据"
        return guarantee_text

    def get_pie_chart(self):

        if not self.data:
            return self.chart

        self.chartSeries.append('5星', 0)
        self.chartSeries.append('4星', 0)
        self.chartSeries.append('3星', 0)

        self.chart5Star = self.chartSeries.slices()[0]
        self.chart5Star.setBrush(QColor(COLOR_MAPPING["5"]))
        self.chart5Star.setLabelFont(QFont("Microsoft YaHei", 10))
        self.chart5Star.setValue(self.star_5_amount)

        self.chart4Star = self.chartSeries.slices()[1]
        self.chart4Star.setBrush(QColor(COLOR_MAPPING["4"]))
        self.chart4Star.setLabelFont(QFont("Microsoft YaHei", 10))
        self.chart4Star.setValue(self.star_4_amount)

        self.chart3Star = self.chartSeries.slices()[2]
        self.chart3Star.setBrush(QColor(COLOR_MAPPING["3"]))
        self.chart3Star.setLabelFont(QFont("Microsoft YaHei", 10))
        self.chart3Star.setValue(self.star_3_amount)

        self.chart.addSeries(self.chartSeries)
        self.chart.setPlotArea(QRectF(0, 0, 500, 150))
        self.chart.setBackgroundVisible(False)
        self.chart.createDefaultAxes()

        self.chart.legend().setVisible(True)
        self.chart.legend().setGeometry(QRectF(0, 0, 100, 100))
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.chart.legend().setLabelColor(QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0))

        return self.chart
