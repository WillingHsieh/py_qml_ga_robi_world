import random

type_s = {
    "0": "空",
    "1": "易",
    "2": "牆",
}

def nbs_type_str( s):
    str_rt = ""
    str_rt += "　" + type_s[s[0]]
    str_rt += "\n" + ( type_s[s[3]] + type_s[s[4]] + type_s[s[1]])
    str_rt += "\n" + "　" + type_s[s[2]]
    return str_rt

class Grid_type:
    empty = "0"
    cans = "1"
    wall = "2"

class Op:
    up = "0"
    right = "1"
    down = "2"
    left = "3"
    random = "4"
    pick = "5"
    sleep = "6"

grid_type = ( Grid_type.empty, Grid_type.cans, Grid_type.wall)

def init_map():
    op_map = {}
    i = 0
    for c0 in grid_type:
        for c1 in grid_type:
            for c2 in grid_type:
                for c3 in grid_type:
                    for c4 in grid_type:
                        key = c0 + c1 + c2 + c3 + c4
                        # print(i, key)
                        op_map[key] = i
                        i += 1
    return op_map

class Gene:
    op_map = init_map()

    def __init__(self):
        self.gene_str = ""

    def set_gene_random(self):
        for i in range(243):
            self.gene_str += str( random.randint( 0, 6))

    def get_op(self, str_type):
        i = self.op_map[ str_type]
        return self.gene_str[i]

    def dump_map(self):
        print( len( self.op_map), self.op_map)
        print( len( self.gene_str), self.gene_str)

if __name__ == "__main__":
    gene = Gene()
    # gene.init_map()
    gene.dump_map()

    g2 = Gene()
    g2.set_gene_random()
    g2.dump_map()
    print( g2.get_op( "00002"))
    print( g2.get_op( "00012"))

    # s = "012345"
    # print( s[1])

