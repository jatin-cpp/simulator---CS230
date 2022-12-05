# from simul import memoryi,memoryd
#mode 0 = instruction , 1 = data

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

read_cycles = 20
write_cycles = 20

memoryi = {}
memoryd = {}

for i in range(0,4*1024,4):
    memoryi[i] = "I" +str(int(i/4))
    memoryd[i] = "D" +str(int(i/4))

# print(memoryi)
# print(memoryd)
cache_size = 128 #Bytes
block_size = 16 #Bytes
cachei = {}
cached = {}
for i in range(int(cache_size/block_size)):
    cached[i]=[] 
    cachei[i]=[]

# print(cached)
# print(cachei)
IF_IR,ID_IR,EX_IR,MEM_IR=0,0,0,0
fmemd=1
j=0

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
def instructionPrint(arg1,arg2):
    pass

def read_memory(address,mode):
    global cached,cachei,memoryd,memoryi
    global ricachehit,rdcachehit,ricachemiss,rdcachemiss
    global ricycle,rdcycle
    #mode 0 = instruction , 1 = data
    if mode == 0:
        block_no = getblock(address)
        if address in cachei[block_no]:
            ricachehit = ricachehit + 1
            return memoryi[address]
        else:
            if memoryi[address] == 'HALT':
                return memoryi[address]
            cachei[block_no] =  cacheblock(address)
            ricycle = ricycle + read_cycles
            ricachemiss = ricachemiss + 1
            return memoryi[address]
    elif mode == 1:
        block_no = getblock(address)
        if address in cached[block_no]:
            rdcachehit = rdcachehit + 1
            return memoryd[address]
        else:
            cached[block_no] =  cacheblock(address)
            rdcycle = rdcycle + read_cycles
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
    elif mode == 1:
        block_no = getblock(address)
        cached[block_no] = cacheblock(address)
        memoryd[address] = data
        wdcycle = wdcycle + write_cycles
        wdcachemiss = wdcachemiss + 1



read_memory(40,0)
read_memory(36,0)
read_memory(12,0)
read_memory(28,0)
read_memory(44,1)
read_memory(40,1)
write_memory(24,1,500)
write_memory(32,1,400)
write_memory(72,1,200)


print(cachei)
print(cached)

# print("ricachehit",ricachehit)
# print("rdcachehit",rdcachehit)
# print("ricachemiss",ricachemiss)
# print("rdcachemiss",ricachemiss)
# print("ricycle",ricycle)
# print("rdcycle",rdcycle)

print("wicycle",wicycle)
print("wdcycle",wdcycle)

print("wicachemiss",wicachemiss)
print("wdcachemiss",wdcachemiss)


for i in range(0,80,8):
    print("memoryd"+str(i),memoryd[i])
