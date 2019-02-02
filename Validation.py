# Kelompok sin
# Jumat 1/2/19
# berisi fungsi yang memvalidasi data input

def isInt(param):
# Mengembalikan true jika param adalah integer
    try:
        int(param)
        return True
    except:
        return False

def isAllInt(param):
# Mengembalikan true jika semua anggota param adalah integer
    i = 0
    Int = True
    while (i<len(param) and Int):
        if(not(isInt(param[i]))):
            Int = False
        else:
            i += 1
    return Int

def isAllPos(param):
# mengembalikan true jika semua anggora param adalah positif
    i = 0
    Pos = True
    while (i<len(param) and Pos):
        if(int(param[i])<0):
            Pos = False
        else:
            i += 1
    return Pos

def CheckInput(masukan):
# fungsi meminta input 4 bilangan hingga benar
    if(not(isAllInt(masukan))):
        print('Ada input bukan bilangan bulat\n')
        return 0
    elif(len(masukan)!=4):
        print('Jumlah bilangan tidak sesuai\n')
        return 0
    elif(not(isAllPos(masukan))):
        print('Ada bilangan yang negatif\n')
        return 0
    else:
        return masukan