#MAO2116
import os, platform

bit = platform.architecture()[0]
def mao_main():
    if bit == '64bit':
        from fuck_mao import menu
        menu()
    elif bit == '32bit':
        from fuck_mao_32 import menu
        menu()
    else:
        print(bit)
        exit()