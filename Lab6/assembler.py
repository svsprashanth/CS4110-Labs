import os
import sys

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }

dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }

jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }

table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    }

for i in range(0,16):
    label = "R" + str(i)
    table[label] = i

variable_ptr = 16  #for next variables
fileName = sys.argv[1].rstrip()
input_file = open(fileName).readlines()
stripped = []
# add labels to the symbol table
line_num = 0
for i in input_file:
    # print(i, end="")
    # if("\t" in i or " " in i):
    #     print(i)
    line = i.strip()
    if(line!="" and line[0]!='/'):
        if(line[0]=="("):
            label = line[1:-1]
            table[label] = line_num
        else:
            line_num+=1
            stripped.append(line+"\n")

def translate_a(line):
    global variable_ptr
    if line[1].isalpha():
        label = line[1:-1]
        aValue = table.get(label, -1)
        if aValue == -1: #lable not in table
            table[label] = variable_ptr
            variable_ptr+=1
        aValue = table[label]
    else:
        aValue = int(line[1:])
    temp = bin(aValue)[2:].zfill(16)
    return temp

def translate_c(line):
    line = line[:-1]
    if not "=" in line:
        line = "null=" + line
    if not ";" in line:
        line = line + ";null"
    temp = line.split('=')
    destCode = dest.get(temp[0], "destFAIL")
    temp = temp[1].split(";")
    compCode = comp.get(temp[0], "compFAIL")
    jumpCode = jump.get(temp[1], "jumpFAIL")

    return compCode, destCode, jumpCode

translated = []
for i in stripped:
    temp = None
    if(i[0]=='@'):
        temp = translate_a(i)
        translated.append(temp)
    else:
        temp = translate_c(i)
        temp = "111"+temp[0]+temp[1]+temp[2]
        translated.append(temp)

out = open(fileName.replace('.asm','.hack'),"w+")
for i in translated:
    out.write(i+"\n")

out.close()
