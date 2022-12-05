from asyncore import read
import csv
import sys
from colorama import Fore

if len(sys.argv) < 3:
    print(Fore.MAGENTA+ "python simul.py <instruction_file_path> <memory_file_path>" + Fore.WHITE)
    exit(1)

pathi = sys.argv[1]
filei = open(pathi,newline='')
readeri = csv.reader(filei)
instructions = [r for r in readeri]


pathd = sys.argv[2]
filed = open(pathd,newline='')
readerd = csv.reader(filed)
data = [d for d in readerd]


# memory_base 

# memory[0] = ['addi','R7','R0','5']
# memory[4] = ['be','R7','R1','8']
# memory[8] = ['addi','R7','R0','800']
# memory[12] = ['add','R1','R2','R3']
# memory[16] = ['addi','R7','R0','1200']
# # memory[16] = ['lw','R13','20(R1)']
# memory[20] = ['add','R4','R1','R5']
# # memory[20] = ['sw','R30','40(R1)']
# # memory[16] = ['add','R13','R14','R15']
# # memory[20] = ['add','R16','R17','R18']
# # memory[20] = ['lw','R16','R1']
# memory[24] = ['addi','R2','R0','2400']
# memory[28] = ['add','R22','R23','R24']
# memory[32] = ['add','R25','R26','R27']
# memory[36] = ['add','R2','R2','R3']
# memory[40] = ['add','R4','R5','R6']
# memory[40] = ['be','R7','R1','-4']
# memory[44] = ['add','R8','R8','R9']
# memory[48] = ['add','R10','R11','R12']
# memory[52] = ['add','R10','R11','R12']
# memory[56] = ['add','R10','R11','R12']
# memory[60] = ['add','R4','R5','R6']
# memory[320]= 9090