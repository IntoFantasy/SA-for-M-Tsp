
# 进行全局参数的设置
def _init():
    global SA_Information
    SA_Information = {}


def initiation(name, value):
    SA_Information[name] = value


def getvalue(name):
    return SA_Information[name]


_init()
initiation("city_number", 21)          # 城市个数
initiation("city_first", 5)            # 出发城市编号
initiation("times", 200)               # 每轮的迭代次数
initiation("num_epochs", 1000)          # 总轮数
initiation("initial_temperate", 300)     # 设置初始温度
initiation("temperate_loss", 0.98)     # 温度的衰减率
