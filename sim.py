# memory(256KB)(word alligned) and register(32 register , 32 bits)
register = [None]*32
register[0] = 0
memory = {}
for i in range(0,256*1024,4):
    memory[i] = None
# for i in range(0,256*1024,4):
#     print(i,memory[i])
# special registers
PC =0
IR=0 # to hold the Current Instruction after IF and before increasing the PC.# Instruction Register
MR=0 #memory register
DR=0 #data register
operation,destn,src1,src2=0,0,0,0
def instructionFetch():
    global IR,PC,memory
    IR = memory[PC]
    PC = PC + 4
#stage = ["","IF","ID","EX","MA","WB"]
# instruction MIPS -> 3 address format op dest,src1,src2
# load instruction in the memory

def operand(operation):
    if(operation == "add" or operation == "sub" or operation == "addi" or operation == "subi"):
        return 1
    elif(operation == "lw" or operation == "sw"):
        return 2
    elif(operation == "bne" or operation == "be"):
        return 3

def sliceoffset(offstring):
    index = 0
    for i in range(len(offstring)):
        if offstring[i] == "(":
            index = i
    return index


def instructionDecode():
    global operation,destn,src1,src2
    operation = IR[0]
    flag =operand(operation)
    if flag==1:
        destn = IR[1]
        src1 = IR[2]
        src2 = IR[3]
    elif flag == 2:
        src1 = IR[1]
        src2 = IR[2]
    elif flag == 3 :
        src1 = IR[1]
        src2 = IR[2]
        destn = IR[3]
        pass

def instructionExecute():
    global operation,register,destn,src1,src2,MR,DR,PC
    if operation == "add":
        register[int(destn[1:])] = register[int(src1[1:])] + register[int(src2[1:])]
    elif operation == "sub":
        register[int(destn[1:])] = register[int(src1[1:])] - register[int(src2[1:])]
    elif operation == "addi":
        register[int(destn[1:])] = register[int(src1[1:])] + int(src2)
    elif operation == "subi":
        register[int(destn[1:])] = register[int(src1[1:])] - int(src2)
    elif operation == "lw":
        if src2[0] == "R":
            MR = int(register[int(src2[1:])])
            DR = int(memory[MR])
            register[int(src1[1:])] = DR
        else:
            offset = int(src2[0]) #this needs to be modified
            MR = int(register[int(src2[3:-1])]) + offset
            DR = int(memory[MR])
            register[int(src1[1:])] = DR
    elif operation == "sw":
        if src2[0] == "R":
            MR = int(register[int(src2[1:])])
            DR = int(register[int(src1[1:])]) 
            memory[MR]= DR
        else:
            offset = int(src2[0]) #this needs to be modified # to include ["lw","R4","26(R2)"]
            MR = int(register[int(src2[3:-1])]) + offset
            DR = int(register[int(src1[1:])]) 
            memory[MR]= DR
    elif operation == "be":
        if register[int(src1[1:])] == register[int(src2[1:])]:
            PC  = PC + 4*int(destn)
    elif operation == "bne":
        if register[int(src1[1:])] != register[int(src2[1:])]:
            PC  = PC + 4*int(destn)

def instructinMemoryAcess():
    global operation,register,destn,src1,src2,MR,DR,PC
    if operation == "lw":
        if src2[0] == "R":
            MR = int(register[int(src2[1:])])
            DR = int(memory[MR])
            register[int(src1[1:])] = DR
        else:
            offset = int(src2[0]) #this needs to be modified to include ["lw","R4","26(R2)"]
            MR = int(register[int(src2[3:-1])]) + offset
            DR = int(memory[MR])
            register[int(src1[1:])] = DR
    elif operation == "sw":
        if src2[0] == "R":
            MR = int(register[int(src2[1:])])
            DR = int(register[int(src1[1:])]) 
            memory[MR]= DR
        else:
            offset = int(src2[sliceoffset(src2)]) #includes ["lw","R4","26(R2)"]
            MR = int(register[int(src2[sliceoffset(src2)+2:-1])]) + offset
            DR = int(register[int(src1[1:])]) 
            memory[MR]= DR
    elif operation == "be":
        if register[int(src1[1:])] == register[int(src2[1:])]:
            PC  = PC + 4*int(destn)
    elif operation == "bne":
        if register[int(src1[1:])] != register[int(src2[1:])]:
            PC  = PC + 4*int(destn)

    pass

memory[0] = ["bne","R0","R1","3"]
memory[4] = ["lw","R6","R5"]
memory[16] = ["lw","R6","R4"]
memory[28] = 0
memory[32] = 1
register[5] = 32
register[4] = 28
register[1] = 0 
# register[6] = 31415

for i in range(2):
    instructionFetch()
    instructionDecode()
    instructionExecute()

for i in range(32):
    print(register[i])
# for i in range(0,32,4):
#     print(memory[i])