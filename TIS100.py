import glob
import re
import time

class Node:
    def __init__(self):
        self.instr = []
        self.acc = 0
        self.bak = 0
        self.len = 0
        self.pc = -1
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
        self.au = True
        self.ad = True
        self.al = True
        self.ar = True
        return

    def fill_instr(self, filename):
        f = open(filename, 'r')
        temp = f.read().splitlines()
        f.close()
        for line in temp:
            self.instr.append(line)
        self.len = len(self.instr)
        
    def step(self):
        if self.au and self.ad and self.al and self.ar:
            self.pc+=1
            if(self.pc >= self.len):
                self.pc = 0
        return self.instr[self.pc]

tis = [[Node() for x in range(4)] for x in range(4)] 
tick = float(raw_input("Please input tick: "))
files = glob.glob('*.tis')
coded = []

for i in files:
    point = [int(s) for s in re.findall(r'\d+', i)]
    tis[point[0]][point[1]].fill_instr(i)
    coded.append(point)

count = 0
while True:
    cnode = [coded[count][0], coded[count][1]]
    instr = tis[cnode[0]][cnode[1]].step()
    instr = instr.split()

    a = instr[0]
    while('#' in a):
        instr = tis[cnode[0]][cnode[1]].step()
        instr = instr.split()
        a = instr[0]
        
    if a == 'MOV':
        src = instr[1]
        dst = instr[2]
        if dst == "ACC":
            dst = 0
        elif dst == "UP":
            dst = 1
        elif dst == "RIGHT":
            dst = 2
        elif dst == "DOWN":
            dst = 3
        elif dst == "LEFT":
            dst = 4
        else:
            dst = 5

        if src.isdigit():
            if dst == 0:
                tis[cnode[0]][cnode[1]].acc = int(src)
            elif dst == 1:
                tis[cnode[0]][cnode[1]].up = int(src)
                tis[cnode[0]][cnode[1]].au = False
            elif dst == 2:
                tis[cnode[0]][cnode[1]].right = int(src)
                tis[cnode[0]][cnode[1]].ar = False
            elif dst == 3:
                tis[cnode[0]][cnode[1]].down = int(src)
                tis[cnode[0]][cnode[1]].ad = False
            elif dst == 4:
                tis[cnode[0]][cnode[1]].up = int(src)
                tis[cnode[0]][cnode[1]].al = False
        else:
            value = False
            if src == "ACC":
                src = tis[cnode[0]][cnode[1]].acc
                value = True
            elif src == "UP":
                if cnode[1] != 0:
                    if tis[cnode[0]][cnode[1]-1].ad == False:
                        src = tis[cnode[0]][cnode[1]-1].down
                        tis[cnode[0]][cnode[1]-1].ad = True
                        value = True
            elif src == "RIGHT":
                if cnode[0] != 3:
                    if tis[cnode[0]+1][cnode[1]].al == False:
                        src = tis[cnode[0]+1][cnode[1]].left
                        tis[cnode[0]+1][cnode[1]].al = True
                        value = True
            elif src == "DOWN":
                if cnode[1] != 3:
                    if tis[cnode[0]][cnode[1]+1].au == False:
                        src = tis[cnode[0]][cnode[1]+1].up
                        tis[cnode[0]][cnode[1]+1].au = True
                        value = True
            elif src == "LEFT":
                if cnode[0] != 0:
                    if tis[cnode[0]-1][cnode[1]].ar == False:
                        src = tis[cnode[0]-1][cnode[1]].right
                        tis[cnode[0]-1][cnode[1]].ar = True
                        value = True
            if value:
                if dst == 0:
                    tis[cnode[0]][cnode[1]].acc = int(src)
                elif dst == 1:
                    tis[cnode[0]][cnode[1]].up = int(src)
                    tis[cnode[0]][cnode[1]].au = False
                elif dst == 2:
                    tis[cnode[0]][cnode[1]].right = int(src)
                    tis[cnode[0]][cnode[1]].ar = False
                elif dst == 3:
                    tis[cnode[0]][cnode[1]].down = int(src)
                    tis[cnode[0]][cnode[1]].ad = False
                elif dst == 4:
                    tis[cnode[0]][cnode[1]].left = int(src)
                    tis[cnode[0]][cnode[1]].al = False

    elif a == 'SWP':
            tmp = tis[cnode[0]][cnode[1]].acc
            tis[cnode[0]][cnode[1]].acc = tis[cnode[0]][cnode[1]].bak
            tis[cnode[0]][cnode[1]].bak = tis[cnode[0]][cnode[1]].acc
    elif a == 'SAV':
            tis[cnode[0]][cnode[1]].bak = tis[cnode[0]][cnode[1]].acc
    elif a == 'ADD':
            src = instr[1]
            if src.isdigit():
                tis[cnode[0]][cnode[1]].acc += int(src)
            else:
                value = False
                if src == "ACC":
                    src = tis[cnode[0]][cnode[1]].acc
                    value = True
                elif src == "UP":
                    if cnode[1] != 0:
                        if tis[cnode[0]][cnode[1]-1].ad == False:
                            src = tis[cnode[0]][cnode[1]-1].down
                            tis[cnode[0]][cnode[1]-1].ad = True
                            value = True
                elif src == "RIGHT":
                    if cnode[0] != 3:
                        if tis[cnode[0]+1][cnode[1]].al == False:
                            src = tis[cnode[0]+1][cnode[1]].left
                            tis[cnode[0]+1][cnode[1]].al = True
                            value = True
                elif src == "DOWN":
                    if cnode[1] != 3:
                        if tis[cnode[0]][cnode[1]+1].au == False:
                            src = tis[cnode[0]][cnode[1]+1].up
                            tis[cnode[0]][cnode[1]+1].au = True
                            value = True
                elif src == "LEFT":
                    if cnode[0] != 0:
                        if tis[cnode[0]-1][cnode[1]].ar == False:
                            src = tis[cnode[0]-1][cnode[1]].right
                            tis[cnode[0]-1][cnode[1]].ar = True
                            value = True
                if value:
                    tis[cnode[0]][cnode[1]].acc += int(src)
    elif a == 'SUB':
        src = instr[1]
        if src.isdigit():
            tis[cnode[0]][cnode[1]].acc -= int(src)
        else:
            value = False
            if src == "ACC":
                src = tis[cnode[0]][cnode[1]].acc
                value = True
            elif src == "UP":
                if cnode[1] != 0:
                    if tis[cnode[0]][cnode[1]-1].ad == False:
                        src = tis[cnode[0]][cnode[1]-1].down
                        tis[cnode[0]][cnode[1]-1].ad = True
                        value = True
            elif src == "RIGHT":
                if cnode[0] != 3:
                    if tis[cnode[0]+1][cnode[1]].al == False:
                        src = tis[cnode[0]+1][cnode[1]].left
                        tis[cnode[0]+1][cnode[1]].al = True
                        value = True
            elif src == "DOWN":
                if cnode[1] != 3:
                    if tis[cnode[0]][cnode[1]+1].au == False:
                        src = tis[cnode[0]][cnode[1]+1].up
                        tis[cnode[0]][cnode[1]+1].au = True
                        value = True
            elif src == "LEFT":
                if cnode[0] != 0:
                    if tis[cnode[0]-1][cnode[1]].ar == False:
                        src = tis[cnode[0]-1][cnode[1]].right
                        tis[cnode[0]-1][cnode[1]].ar = True
                        value = True
            if value:
                tis[cnode[0]][cnode[1]].acc -= int(src)
    elif a == 'NEG':
            tis[cnode[0]][cnode[1]].acc *= -1
    elif a == 'JMP' or 'JRO':
            src = instr[1]
            tis[cnode[0]][cnode[1]].pc += (int(src) + (int(src)/abs(int(src))))
    elif a == 'JEZ':
            if tis[cnode[0]][cnode[1]].acc == 0:
                    src = instr[1]
                    tis[cnode[0]][cnode[1]].pc += (int(src) + (int(src)/abs(int(src))))
    elif a == 'JNZ':
            if tis[cnode[0]][cnode[1]].acc != 0:
                    src = instr[1]
                    tis[cnode[0]][cnode[1]].pc += (int(src) + (int(src)/abs(int(src))))
    elif a == 'JGZ':
            if tis[cnode[0]][cnode[1]].acc > 0:
                    src = instr[1]
                    tis[cnode[0]][cnode[1]].pc += (int(src) + (int(src)/abs(int(src))))
    elif a == 'JLZ':
            if tis[cnode[0]][cnode[1]].acc < 0:
                    src = instr[1]
                    tis[cnode[0]][cnode[1]].pc += (int(src) + (int(src)/abs(int(src))))
    if not tis[0][0].au:
        tis[0][0].au = True
        print tis[0][0].up
        
    count = (count+1)%len(coded)
    time.sleep(tick)
