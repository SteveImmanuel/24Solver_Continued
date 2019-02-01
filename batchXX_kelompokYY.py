# Kelompok sin
# Kamis 31/1/19
# front-end 2
# input ouput file

import sys
from GameEngine import CheckInput,calculate,calculate_2
import time

if __name__ == "__main__":
    argumen = sys.argv[1:]
    if len(argumen)==2:
        try: # mencoba membuka file input
            in_f = open(argumen[0],'r')
        except:
            print("tidak dapat membuka file input")
            sys.exit(1)
        try: # mencoba membuat file output
            out_f = open(argumen[1],'w')
        except:
            print("tidak dapat membuat file output")
            sys.exit(1)
        # membaca input dari file
        masukan = in_f.read().split()
        masukan = list(map(int, masukan)) # casting ke int
        if (CheckInput(masukan)!=0): # memastikan input valid
            keluaran = calculate_2(masukan) # menghitung
            print('keluaran',keluaran)
            out_f.write(keluaran+'\n') # menulis ke file output
            print('ditemukan solusi')
        else: # input tidak valid
            print("coba lagi")
    else: # parameter input terlalu banyak
        print("parameter input salah")