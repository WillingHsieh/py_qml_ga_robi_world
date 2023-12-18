import random

class Op:
    up = "0"
    right = "1"
    down = "2"
    left = "3"
    random = "4"
    pick = "5"
    nothing = "6"

op_names = {
    "0": "up",
    "1": "right",
    "2": "down",
    "3": "left",
    "4": "random",
    "5": "pick",
    "6": "nothing",
}

class Grid_type:
    empty = "0"
    cans = "1"
    wall = "2"

grid_types = (
    Grid_type.empty,
    Grid_type.cans,
    Grid_type.wall
)

def init_map():
    op_map = {}
    i = 0
    for c0 in grid_types:
        for c1 in grid_types:
            for c2 in grid_types:
                for c3 in grid_types:
                    for c4 in grid_types:
                        key = c0 + c1 + c2 + c3 + c4
                        # print(i, key)
                        op_map[key] = i
                        i += 1
    return op_map

class Gene:

    # 基因對照表：Robi 處境對應到基因所在位置
    # "012345" -> 0...242
    op_map = init_map()

    def __init__(self):

        # 代表基因的字串
        self.gene_str = "4" * 243

        random.seed()

    # 隨機產生基因
    def set_gene_random(self):
        self.gene_str = ""
        for i in range(243):
            self.gene_str += str( random.randint( 0, 6))
        print( "新的基因:", self.gene_str[:30]+"...")

    def get_op(self, str_type):
        i = self.op_map[ str_type]
        return self.gene_str[i]

    def dump(self):
        # print( len( self.op_map), self.op_map)
        print( len( self.gene_str), self.gene_str)

if __name__ == "__main__":
    # gene = Gene()
    # gene.init_map()
    # gene.dump_map()

    g2 = Gene()
    g2.set_gene_random()
    # g2.dump()
    g2.set_gene_random()
    # g2.dump()
    # print( g2.get_op( "00002"))
    # print( g2.get_op( "00012"))

    # s = "012345"
    # print( s[1])

