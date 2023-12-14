# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal, Property
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
import random

from robi import *
from db import *

class Cells(QObject):
    def __init__(self):
        super().__init__()

        # ==== 設定參數 ====

        self.__rows = 10
        self.__cols = 10
        self.__len = 60

        # 格子總數
        self.__count = self.__rows * self.__cols

        # 初始化 data/data_next
        self.__data = [ False for i in range( self.__count)]

        # 初始化 鄰居查表
        self.__data_nbs = []
        for i in range(self.__count):
            self.__data_nbs.append( self.get_around_nbs(i))

        # 資料庫以及地圖名稱列表
        self.__db = DB()
        self.__maps_name = self.__db.get_name_list()
        self._maps_name_changed.emit( self.__maps_name)

        # 羅比
        self.robi = Robi(self)
        print( "init...end")

    # ==== 座標換算/查表 ====

    def get_row_col(self, idx):
        row = idx // self.__cols
        col = idx % self.__cols
        return row, col

    def get_idx(self, row, col):
        return row * self.__cols + col

    # 上 右 下 左 為 0, 1, 2 ,3
    def get_around_nbs(self, idx):
        nbs = []
        row, col = self.get_row_col(idx)

        left  = col - 1
        right = col + 1
        up    = row - 1
        down  = row + 1

        nbs_row_cols = (
            ( up,  col),    # 上
            ( row,  right), # 右
            ( down, col),   # 下
            ( row,  left),  # 左
        )
        for ( r, c) in nbs_row_cols:
            if not ( 0 <= r < self.__rows):
                nbs.append( -1)
            elif not ( 0 <= c < self.__cols):
                nbs.append( -1)
            else:
                nbs.append( self.get_idx( r, c))
        return nbs

    def get_nbs_type(self):
        p = self.get_robi_pos()
        print( p, ":", self.__data_nbs[ p])

    # 高度
    def get_rows(self):
        return self.__rows
    _rows_changed = Signal(int)
    rows = Property(int, get_rows, notify=_rows_changed)

    # 寬度
    def get_cols(self):
        return self.__cols
    _cols_changed = Signal(int)
    cols = Property(int, get_cols, notify=_cols_changed)

    # 格子大小
    def get_len(self):
        return self.__len
    _len_changed = Signal( int)
    len = Property( int, get_len, notify=_len_changed)

    # ==== 地圖 ====

    def get_maps_name(self):
        return self.__maps_name
    _maps_name_changed = Signal(list)
    maps_name = Property(list, get_maps_name, notify=_maps_name_changed)

    # 將地圖存回 data
    def restore_map(self, list_map):
        self.data_clear()
        for ( r, c) in list_map:
            self.set_data( self.get_idx( r, c), True)

    @Slot( str)
    def load_map(self, str_name):
        print( "str_name:", str_name)
        list_map = self.__db.get_map( str_name)
        # print( "list_map:", list_map)
        self.restore_map( list_map)

    @Slot( str)
    def save_map(self, str_name):
        # print( str_name)

        # 存入資料庫
        map_data = []
        for i in range( self.__count):
            if self.__data[ i]:
                map_data.append( self.get_row_col( i))
        str_map = str( map_data)
        # print( str_map)
        self.__db.insert_data(str_name, str_map)

        self.__maps_name = self.__db.get_name_list()
        self._maps_name_changed.emit(self.__maps_name)

    @Slot( str)
    def del_map(self, str_name):
        # print( str_name)
        self.__db.del_data( str_name)

        self.__maps_name = self.__db.get_name_list()
        self._maps_name_changed.emit(self.__maps_name)

    # ==== 對應到 UI 的陣列 ====

    def get_data(self):
        return self.__data
    _data_changed = Signal( list)
    data = Property(list, get_data, notify=_data_changed)

    def is_data_true(self, idx):
        return self.__data[ idx]

    # 設定單一格子，會響應到 UI
    @Slot( int, bool)
    def set_data(self, idx, val):
        if self.__data[ idx] != val:
            self.__data[idx] = val
            self._cell_changed.emit( idx, val)
    _cell_changed = Signal( int, bool)

    # ==== 按鈕對應功能 ====

    @Slot( int)
    def load_random(self, percent):
        list_len = int(self.__count * percent / 100)
        print( "list_len:", list_len)

        list_pos = set()
        while len(list_pos) < list_len:
            list_pos.add( random.randint(0, self.__count-1))
        print( len(list_pos), list_pos)

        for ii in list_pos:
            self.set_data( ii, True)

    @Slot()
    def data_clear(self):
        for idx in range( self.__count):
            self.set_data( idx, False)

    # 羅比的計時器
    def get_robi_ti(self):
        return self.robi.get_ti_ms()
    robi_ti_changed = Signal( int)
    robi_ti = Property(int, get_robi_ti, notify=robi_ti_changed)

    # 羅比的位置
    def get_robi_pos(self):
        return self.robi.get_idx()
    robi_pos_changed = Signal( int)
    robi_pos = Property(int, get_robi_pos, notify=robi_pos_changed)

    # 羅比的方向
    def get_robi_way(self):
        return self.robi.get_way()
    robi_way_changed = Signal( int)
    robi_way = Property(int, get_robi_way, notify=robi_way_changed)

    robi_hit = Signal( int)

    # 跌代
    @Slot()
    def step(self):
        print( "step()...")
        self.robi.step()

    @Slot()
    def stop(self):
        self.robi.stop()

    @Slot()
    def begin(self):
        # print( "begin()...")
        self.robi.begin()

    # ==== 速度 ====

    @Slot()
    def speed_up(self):
        self.robi.speed_up()

    @Slot()
    def speed_down(self):
        self.robi.speed_down()

    @Slot()
    def move_up(self):
        self.robi.move_up()
        self.get_nbs_type()

    @Slot()
    def move_down(self):
        self.robi.move_down()
        self.get_nbs_type()

    @Slot()
    def move_left(self):
        self.robi.move_left()
        self.get_nbs_type()

    @Slot()
    def move_right(self):
        self.robi.move_right()
        self.get_nbs_type()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    qmlRegisterType( Cells, 'Cells', 1, 0, 'Cells')

    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
