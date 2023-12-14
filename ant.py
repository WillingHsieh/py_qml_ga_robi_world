# This Python file uses the following encoding: utf-8
from threading import Timer

# 每次清扫工作罗比可以执行200个动作。
# 动作可以是以下7种：往北移动、往南移动、往东移动、往西移动、随机移动、不动、收集罐子。
# 每个动作都会受到奖赏或惩罚。
#   如果罗比所在的格子中有罐子并且收集起来了，就会得到10分的奖赏。
#   如果进行收集罐子的动作而格子中又没有罐子，就会被罚1分。
#   如果撞到了墙，会被罚5分，并弹回原来的格子。
# 罗比可以看到5个格子（当前格子、东、南、西、北）每个格子可以标为空、罐和墙。
# 这样就有3*3*3*3*3 = 3^5 = 243种可能情形。

class Ways:
    up = 0
    right = 1
    down = 2
    left = 3

class Ant:
    # 計時器
    tm_interval = 0.8
    timer = None

    def __init__(self, par_cells):
        self.cells = par_cells

        self.rows = self.cells.rows
        self.cols = self.cells.cols

        self.r = 0
        self.c = 0

        self.way = Ways.up

    # ==== 開始/結束 ====

    # 若螞蟻在黑格(color)，左轉90度，將該格改為白格，向前移一步。
    # 若螞蟻在白格，右轉90度，將該格改為黑格，向前移一步；
    def step(self):
        # 變色/轉向
        if self.is_color():
            self.set_color( False)
            self.turn_left()
        else:
            self.set_color( True)
            self.turn_right()

        # print( "self.way:", self.way)
        # 移動
        if self.way == Ways.left:
            self.move_left()
        elif self.way == Ways.right:
            self.move_right()
        elif self.way == Ways.up:
            self.move_up()
        elif self.way == Ways.down:
            self.move_down()

    def run(self):
        # print( "run()...")
        self.step()

        self.timer = Timer(self.tm_interval, self.run)
        self.timer.start()

    def begin(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
        else:
            self.timer = Timer(self.tm_interval, self.run)
            self.timer.start()

    def get_ti_ms(self):
        return int( self.tm_interval * 1000)

    def speed_up(self):
        self.tm_interval /= 2
        if self.tm_interval < 0.003:
            self.tm_interval = 0.003
        self.cells.ant_ti_changed.emit( self.get_ti_ms())
        print( "加速：", self.tm_interval)

    def speed_down(self):
        self.tm_interval *= 2
        self.cells.ant_ti_changed.emit( self.get_ti_ms())
        print("減速：", self.tm_interval)

    def stop(self):
        print( "stop()...")
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    # ==== 方向/轉向 ====

    def is_color(self):
        idx = self.get_idx()
        return self.cells.is_data_true( idx)

    def set_color(self, val):
        idx = self.get_idx()
        self.cells.set_data( idx, val)
        # self.cells.__data[ idx] = val

    def get_way(self):
        return self.way

    def turn_right(self):
        self.way = (self.way + 1) % 4
        self.cells.ant_way_changed.emit( self.way)

    def turn_left(self):
        self.way = (self.way + 3) % 4
        self.cells.ant_way_changed.emit( self.way)

    # ==== 位置/移動 ====

    def get_idx(self):
        return self.cells.get_idx( self.r, self.c)

    def move_up(self):
        self.r = (self.r - 1 + self.rows) % self.rows
        self.cells.ant_pos_changed.emit(self.get_idx())

    def move_down(self):
        self.r = (self.r + 1) % self.rows
        self.cells.ant_pos_changed.emit(self.get_idx())

    def move_left(self):
        self.c = (self.c - 1 + self.cols) % self.cols
        self.cells.ant_pos_changed.emit(self.get_idx())

    def move_right(self):
        self.c = (self.c + 1) % self.cols
        self.cells.ant_pos_changed.emit(self.get_idx())
