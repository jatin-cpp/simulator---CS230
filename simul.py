# register 32 * 32 bits
from colorama import Fore
from paste import instructions,data

# metrics
cycle = 0
branch_stalls = 0
# cache metrics
ricachehit = 0 
rdcachehit = 0
ricachemiss = 0
rdcachemiss = 0

ricycle = 0
rdcycle = 0


wicachemiss = 0
wdcachemiss = 0

wicycle = 0
wdcycle = 0


#initial conditions
read_cycles = 20
write_cycles = 20
cache_size = 128 #Bytes
block_size = 16 #Bytes

# creating cache
cachei = {}
cached = {}
for i in range(int(cache_size/block_size)):
    cached[i]=[] 
    cachei[i]=[]

# auxilary functions related  to memory access
def getblock(address):
    block = (int(address/16))%8
    return block

def cacheblock(address):
    lst = []
    block = getblock(address)
    start = (int(address/16))*16
    lst = [r for r in range(start,start + 4*int(block_size/4),4)]
    # print("lst",lst,"block",block,"start",start,"lst",lst)
    return lst

# memory access functions
def read_memory(address,mode):
    global cached,cachei,memoryd,memoryi
    global ricachehit,rdcachehit,ricachemiss,rdcachemiss
    global ricycle,rdcycle
    #mode 0 = instruction , 1 = data
    if mode == 0:
        block_no = getblock(address)
        if address in cachei[block_no]:
            ricachehit = ricachehit + 1
            ricycle = ricycle + 1
            return memoryi[address]
        else:
            if memoryi[address] == 'HALT':
                return memoryi[address]
            cachei[block_no] =  cacheblock(address)
            ricycle = ricycle + read_cycles
            ricachemiss = ricachemiss + 1
            print("ricachemiss",ricachemiss,"ricachecycle",ricycle)
            return memoryi[address]
    elif mode == 1:
        block_no = getblock(address)
        if address in cached[block_no]:
            rdcachehit = rdcachehit + 1
            rdcycle = rdcycle + 1 
            return memoryd[address]
        else:
            if memoryd[address] == 'HALT':
                return memoryd[address]
            cached[block_no] =  cacheblock(address)
            rdcycle = rdcycle + read_cycles
            print("rdcachemiss",rdcachemiss,"rdcachecycle",rdcycle)
            rdcachemiss = rdcachemiss + 1
            return memoryd[address]
        

def write_memory(address,mode,data):
    global cached,cachei,memoryd,memoryi
    global wicachemiss,wdcachemiss
    global wicycle,wdcycle
    if mode == 0:
        block_no = getblock(address)
        cachei[block_no] = cacheblock(address)
        memoryi[address] = data
        wicycle = wicycle + write_cycles
        wicachemiss = wicachemiss + 1
        print("wicachemiss",wicachemiss,"wicycle",wicycle)
    elif mode == 1:
        block_no = getblock(address)
        cached[block_no] = cacheblock(address)
        memoryd[address] = data
        wdcycle = wdcycle + write_cycles
        wdcachemiss = wdcachemiss + 1
        print("wdcachemiss",wdcachemiss,"wdcycle",wdcycle)


register = [None]*32
register[0] = 0
# register 29-31 used for functions
# memory 256 KB [word aligned]
memoryi = {}
memoryd = {}
for i in range(0,256*1024,4):
    try:
        memoryi[i] = instructions[int(i/4)] 
    except:
        memoryi[i] = None
    try: 
        memoryd[i] = int(data[int(i/4)][0])
    except:
        memoryd[i] = None
    

# for i in range(0,4*6,4):
#     print(memoryi[i])
# print("blank")
# for i in range(0,4*6,4):
#     print(memoryd[i])
# incrementsize = 4

# IR,PC = 0,0# Actual Program counter and IR
PC=0
#used by IF

IF_PC,IF_IR = 0,0 # result of IF stage
# used by ID stage
IF_flag=0

ID_PC,ID_IR,ID_RF1,ID_RF2,ID_IMM=0,0,0,0,0 # result of ID stage , RF1 and RF2 are 
# used by EX stage
ID_flag=0

EX_BRANCH,EX_IR,EX_ALU,EX_ZERO,EX_RF2 =0,0,0,0,0 # branch to change the branch , ALU for computaion,
#ZERO status of comparison,RF2 for store purpose
#used by MEM stage
EX_Flag=0

MEM_ALU,MEM_DATA,MEM_IR = 0,0,0
# In WB stage write back to register from MEM stage
#used for writing to registers
MEM_Flag=0

branch_signal_mem_access = 0 # spl signal by MEM stage to IF when branching is done

def position(offset_reg):
    for i in range(len(offset_reg)):
        if(offset_reg[i] == '('):
            return i
    pass

def instructionPrint(instruction,code):
    if code == 1:
        if instruction == 0:
            print("x",end='\t')
            return
        if instruction[-1]!="skip":
            print("I"+str(instruction[-1]),end='\t')
        else:
            print("I"+str(instruction[-2]),end='\t')
            pass
    elif code == 0:
        if instruction == 0:
            print("x")
            return
        if instruction[-1]!="skip":
            print("I"+str(instruction[-1]))
        else:
            print("I"+str(instruction[-2]))
            pass

    elif code == 2:
        # skip one
        print(Fore.RED, end='')
        if instruction == 0:
            print("x",end='\t')
            return
        if instruction[-1]!="skip":
            print("I"+str(instruction[-1]),end='\t')
        else:
            print("I"+str(instruction[-2]),end='\t')
        print(Fore.WHITE, end='')

        pass
    pass

instructionNo=1

def instructionFetch():
    global instructionNo 
    global IF_flag
    global EX_BRANCH
    global branch_signal_mem_access,branch_stalls
    # print("IF",end="\t")
    global PC,memoryi, IF_PC,IF_IR,memoryd
    global ID_IR,EX_IR
    # IF_IR = memoryi[PC]
    IF_IR = read_memory(PC,0)
    IF_IR.append(instructionNo)
    instructionNo = instructionNo +1
    if branch_signal_mem_access :
        IF_IR.append("skip")
        ID_IR.append("skip")
        EX_IR.append("skip")
        branch_stalls = branch_stalls + 3
        PC = EX_BRANCH
        branch_signal_mem_access=0
    else:
        PC = PC + 4
    IF_PC = PC
    instructionPrint(IF_IR,1)
    IF_flag=1
    pass

def instructionDecode():
    global ID_flag,IF_flag
    global register 
    global IF_IR,IF_PC 
    global ID_IR,ID_PC, ID_RF1,ID_RF2,ID_IMM
    fcol = 1 #local
    if IF_flag:
        if IF_IR[-1] !='skip':
            if IF_IR[0]=='add' or IF_IR[0]=='sub' :
                ID_RF1 = register[int(IF_IR[2][1:])]#2
                ID_RF2 = register[int(IF_IR[3][1:])]#3
                pass

            elif IF_IR[0]=='addi' or IF_IR[0]=='subi' :
                ID_RF1 = register[int(IF_IR[2][1:])]#2
                ID_IMM = int(IF_IR[3])#3

            elif IF_IR[0] == 'lw':
                if IF_IR[2][-1] != ')':
                    ID_RF2 = register[int(IF_IR[2][1:])]#2
                    # print("print this",IF_IR,int(IF_IR[2][1:]))
                else:
                    pos = position(IF_IR[2])
                    ID_RF2 = register[int(IF_IR[2][pos+2:-1])]#2
                    ID_IMM = int(IF_IR[2][:pos])

            elif IF_IR[0] == 'bne' or IF_IR[0] == "be":
                ID_RF1 = register[int(IF_IR[1][1:])]#1
                ID_RF2 = register[int(IF_IR[2][1:])]#2
                ID_IMM = int(IF_IR[3])#3
                pass
        else : 
            instructionPrint(IF_IR,2)
            fcol = 0


        # print("ID",end="\t")
        #proceed with decode
        ID_IR = IF_IR
        ID_PC = IF_PC
        ID_flag=1
    if fcol:
        instructionPrint(IF_IR,1)

def instructionExecute():
    global EX_Flag,ID_flag
    global ID_PC,ID_IR,ID_RF1,ID_RF2,ID_IMM
    global EX_BRANCH,EX_IR,EX_ALU,EX_ZERO,EX_RF2
    fcol = 1 #local
    if ID_flag:
        if ID_IR[-1] !='skip':
            if ID_IR[0]=='add':
                EX_ALU = ID_RF1 + ID_RF2
                pass
            elif ID_IR[0]=='sub':
                EX_ALU = ID_RF1 - ID_RF2
                pass
            elif ID_IR[0]=='addi':
                EX_ALU = ID_RF1 + ID_IMM
                pass
            elif ID_IR[0]=='subi':
                EX_ALU = ID_RF1 - ID_IMM
                pass

            elif ID_IR[0]=='lw' or ID_IR[0]=='sw':
                # print(ID_IR[0],"exec block")
                if ID_IR[2][-1] != ')':
                    EX_RF2 = ID_RF2
                    # print(ID_IR[0],"exec block",IF_IR[2])
                else:
                    EX_RF2 = ID_RF2 + ID_IMM

            elif ID_IR[0] == 'bne':
                if ID_RF1 != ID_RF2 :
                    EX_ZERO = True
                else :
                    EX_ZERO = False 
                EX_BRANCH = ID_PC + 4*ID_IMM
                pass
            elif ID_IR[0] == "be":
                if ID_RF1 == ID_RF2 :
                    EX_ZERO = True
                else :
                    EX_ZERO = False 
                EX_BRANCH = ID_PC + 4*ID_IMM
                pass
        else : 
            instructionPrint(ID_IR,2)
            fcol = 0


        # print("EX",end="\t")
        #proceed with Execute
        """^This needs to be modified """
        EX_IR = ID_IR

        EX_Flag=1
    if fcol:
        instructionPrint(ID_IR,1)

def instructionMemory():
    global PC
    global MEM_Flag,EX_Flag
    global EX_BRANCH,EX_IR,EX_ALU,EX_ZERO,EX_RF2
    global MEM_ALU,MEM_DATA,MEM_IR
    global ID_IR, ID_RF1,ID_RF2
    global branch_signal_mem_access # spl signal for branching
    fcol = 1 #local
    if EX_Flag:
        # print("MEM",end="\t")
        #proceed with Memory access
        if EX_IR[-1] !='skip':

            # if EX_IR[0] == 'lw' or EX_IR[0] == 'sw':
            #     # if ID_IR[0] == 'add' or ID_IR[0] == 'addi' or ID_IR[0] == 'sub' or ID_IR[0] == 'subi'
            #     pass

            if EX_IR[0] == 'lw':
                # print(EX_IR)
                # print(register[1])
                # print(EX_RF2)
                # MEM_DATA = memoryd[EX_RF2]
                MEM_DATA = read_memory(EX_RF2,1)
                pass
            elif EX_IR[0] == 'sw':
                # memoryd[EX_RF2] = register[int(EX_IR[1][1:])]
                #loc , mode , data
                write_memory(EX_RF2,1,register[int(EX_IR[1][1:])])

            elif EX_IR[0] == 'be' or EX_IR[0] == 'bne':
                if EX_ZERO :
                    branch_signal_mem_access = 1
            elif EX_IR[0] == 'add' or EX_IR[0] == 'addi' or EX_IR[0] == 'sub' or EX_IR[0] == 'subi':
                if EX_IR[1] in ID_IR[1:]:
                    if ID_IR[0] == 'add' or ID_IR[0] == 'addi' or ID_IR[0] == 'sub' or ID_IR[0] == 'subi':
                        if EX_IR[1] == ID_IR[2]:
                            ID_RF1 = EX_ALU
                        elif EX_IR[1] == ID_IR[3]:
                            ID_RF2 = EX_ALU
                    elif ID_IR[0] == 'be' or ID_IR[0] == 'bne':
                        if EX_IR[1] == ID_IR[1]:
                            ID_RF1 = EX_ALU
                        elif EX_IR[1] == ID_IR[2]:
                            ID_RF2 = EX_ALU
                # if EX_IR[1] in 
        else : 
            instructionPrint(EX_IR,2)
            fcol = 0

        MEM_IR = EX_IR
        MEM_ALU = EX_ALU

        MEM_Flag=1
    if fcol : 
        instructionPrint(EX_IR,1)

    pass

def instructionWriteback():
    global MEM_Flag
    global register
    global MEM_ALU,MEM_DATA,MEM_IR
    global ID_RF1,ID_RF2,ID_IR
    fcol = 1 #local
    if MEM_Flag:
        if MEM_IR[-1] !='skip':

            if MEM_IR[0] == 'add' or MEM_IR[0] == 'addi' or MEM_IR[0] == 'sub' or MEM_IR[0] == 'subi':
                if MEM_IR[1] in ID_IR[1:]:
                    if ID_IR[0] == 'add' or ID_IR[0] == 'addi' or ID_IR[0] == 'sub' or ID_IR[0] == 'subi':
                        if MEM_IR[1] == ID_IR[2]:
                            ID_RF1 = MEM_ALU
                        elif MEM_IR[1] == ID_IR[3]:
                            ID_RF2 = MEM_ALU
                    elif ID_IR[0] == 'be' or ID_IR[0] == 'bne':
                        if MEM_IR[1] == ID_IR[1]:
                            ID_RF1 = MEM_ALU
                        elif MEM_IR[1] == ID_IR[2]:
                            ID_RF2 = MEM_ALU
                register[int(MEM_IR[1][1:])] = MEM_ALU
                pass
            elif MEM_IR[0] == 'lw':
                register[int(MEM_IR[1][1:])] = MEM_DATA
        else : 
            instructionPrint(MEM_IR,2)
            fcol = 0
    if fcol: 
        instructionPrint(MEM_IR,1)

        # print("WB",end="\t")
        #proceed with Writeback

for i in range(1,30):
    register[i] =0 

# register[1] = 
# register[29],register[30] = 9,9
if __name__ == "__main__":
    count = 20000
    print("WB\tMEM\tEX\tID\tIF\tcycle")
    for i in range(count):
        instructionWriteback()
        instructionMemory()
        instructionExecute()
        instructionDecode()
        instructionFetch()
        print(i+1)
        cycle = i+1
        if IF_IR[0] == "HALT" and ID_IR[0] == "HALT" and EX_IR[0] == "HALT" and MEM_IR[0] == "HALT" :
            cycle = cycle - 4
            break
    # final count
    cycle = cycle + ricycle + rdcycle + wicycle + wdcycle


    for i in range(1,31):
        print("R"+str(i),register[i])

    print("cycles :",cycle)
    print("branch stalls :",branch_stalls)
    print("icache miss",ricachemiss+wicachemiss)
    print("icache hit",ricachehit)
    print("dcache miss",rdcachemiss+wdcachemiss)
    print("dcache hit",rdcachehit+ricachehit)
    print("CPI : " ,cycle/(cycle - ricycle-rdcycle-wicycle-wdcycle-branch_stalls))

    # for p in range(320,344,4):
    #     print("M"+str(p),memory[p])

# for i in range(0,32,4):
#     print(memoryd[i])