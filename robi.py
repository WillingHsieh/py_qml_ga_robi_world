# This Python file uses the following encoding: utf-8
from threading import Timer
from gene import *

# 每次清扫工作罗比可以执行200个动作。
# 动作可以是、往东移动、往西以下7种：往北移动、往南移动移动、随机移动、不动、收集罐子。
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

class Robi:

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

        self.gene = Gene()
        # self.gene.set_gene_random()
        self.gene.dump()

        self.score = -1
        self.set_score( "歸零")

        self.step_counter = -1
        self.set_step_counter( 0)

        self.step_max = 0

        self.op_func = {
            "0": self.move_up,
            "1": self.move_right,
            "2": self.move_down,
            "3": self.move_left,
            "4": self.move_random,
            "5": self.pickup,
            "6": self.nothing,
        }

    # ==== 移動／動作 ====

    def move_up(self):
        self.set_way( Ways.up)
        if self.r <= 0:
            self.set_score( "撞牆")
            self.cells.robi_hit.emit( Ways.up)
            return
        self.r -= 1
        self.cells.robi_pos_changed.emit(self.get_idx())
        self.cells.get_nbs_type()

    def move_right(self):
        self.set_way( Ways.right)
        if self.c >= (self.cols-1):
            self.set_score( "撞牆")
            self.cells.robi_hit.emit( Ways.right)
            return
        self.c += 1
        self.cells.robi_pos_changed.emit(self.get_idx())
        self.cells.get_nbs_type()

    def move_down(self):
        self.set_way( Ways.down)
        if self.r >= (self.rows-1):
            self.set_score( "撞牆")
            self.cells.robi_hit.emit( Ways.down)
            return
        self.r += 1
        self.cells.robi_pos_changed.emit(self.get_idx())
        self.cells.get_nbs_type()

    def move_left(self):
        self.set_way( Ways.left)
        if self.c <= 0:
            self.set_score( "撞牆")
            self.cells.robi_hit.emit( Ways.left)
            return
        self.c -= 1
        self.cells.robi_pos_changed.emit(self.get_idx())
        self.cells.get_nbs_type()

    def move_random(self):
        random_way = str( random.randint( 0, 3))
        print( "\t隨機方向:", random_way)
        self.op_func[ random_way]()

    def pickup(self):
        if self.is_color():
            self.set_color( False)
            self.set_score( "撿拾成功")
        else:
            self.set_score( "撿拾失敗")
        self.cells.get_nbs_type()

    @staticmethod
    def nothing():
        pass

    # ==== 開始 ====

    def step(self):

        # 決定做什麼
        nbs_type = self.cells.get_nbs_type()
        op = self.gene.get_op( nbs_type)
        print( self.step_counter, "基因決定:",
               nbs_type, "->", op + "(" + op_names[ op] + ")")

        # 執行動作
        self.op_func[ op]()

        # 步數累計
        self.set_step_counter( self.step_counter + 1)

    def run(self):
        self.step()

        # 步數累計
        # self.set_step_counter( self.step_counter + 1)

        self.timer = Timer(self.tm_interval, self.run)
        self.timer.start()

    def begin(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
        else:
            self.timer = Timer(self.tm_interval, self.run)
            self.timer.start()

    def run_200(self):
        self.step()

        # 步數累計／判斷是否結束
        # self.set_step_counter( self.step_counter + 1)
        if self.step_counter >= self.step_max:
            self.cells.finished_200()
            return

        self.timer = Timer(self.tm_interval, self.run_200)
        self.timer.start()

    def begin_200(self):
        self.timer = Timer(self.tm_interval, self.run_200)
        self.timer.start()

    def stop(self):
        print( "stop()...")
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    # ==== 時間 ====

    def get_ti_ms(self):
        return int( self.tm_interval * 1000)

    def speed_up(self):
        self.tm_interval /= 2
        if self.tm_interval < 0.003:
            self.tm_interval = 0.003
        self.cells.robi_ti_changed.emit( self.get_ti_ms())
        print( "加速：", self.tm_interval)

    def speed_down(self):
        self.tm_interval *= 2
        self.cells.robi_ti_changed.emit( self.get_ti_ms())
        print("減速：", self.tm_interval)

    # ==== 顏色 ====

    def is_color(self):
        idx = self.get_idx()
        return self.cells.is_data_true( idx)

    def set_color(self, val):
        idx = self.get_idx()
        self.cells.set_data( idx, val)

    # ==== 方向/定位 ====

    def get_idx(self):
        return self.cells.get_idx( self.r, self.c)

    def get_way(self):
        return self.way

    def set_way(self, par_way):
        self.way = par_way
        self.cells.robi_way_changed.emit( self.way)

    # ==== 分數／基因 ====

    def set_score(self, par_i):
        if par_i == "歸零":
            self.score = 0
        elif par_i == "撞牆":
            self.score -= 5
        elif par_i == "撿拾成功":
            self.score += 10
        elif par_i == "撿拾失敗":
            self.score -= 1

        # print( par_i, "-> 分數:", self.score)
        self.cells.robi_score.emit( self.score)

    def set_step_counter(self, par_c):
        self.step_counter = par_c
        self.cells.robi_step_counter.emit( self.step_counter)

    def reset(self):
        self.r = 0
        self.c = 0
        self.cells.robi_pos_changed.emit(self.get_idx())

        self.set_way( Ways.up)

        self.reset_gene()
        self.set_score( "歸零")
        self.step_max = 10
        self.set_step_counter( 0)

    def reset_gene(self):
        self.gene.set_gene_random()
