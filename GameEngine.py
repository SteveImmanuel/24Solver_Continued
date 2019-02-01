# Kelompok sin
# Kamis 31/1/19
# back-end
# menghitung solusi 24 solver dari input dengan algoritma greedy

import itertools

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

def calculate(masukan):
    operator = '+-*/'
    masukan.sort(reverse=True)
    equation = [str(masukan[0])] # berubah
    masukan.remove(masukan[0])
    while masukan != []:
        # first=True
        # select_eq = '' # menyimpan persamaan dengan poin
        daftar = list()
        for op in operator: # coba untuk semua operator
            for angka in masukan: # coba untuk semua angka
                temp_eq = equation.copy()
                temp_eq += op + str(angka)
                daftar.append((temp_eq,angka))
                # try: 
                #     hasil = eval(temp_eq)
                # except:
                #     continue
                # if first: # iterasi pertama
                #     max_point = countPoint(temp_eq,hasil)
                #     select_eq = temp_eq
                #     selected = angka
                #     first=False
                # else:
                #     temp_point = countPoint(temp_eq,hasil)
                #     if (max_point<temp_point):
                #         max_point = temp_point
                #         select_eq = temp_eq
                #         selected = angka
        maks = greedy(daftar)
        equation = maks[0]
        masukan.remove(maks[1])
    equation = ''.join(equation)
    print ('point',countPoint(equation,eval(equation)))
    return equation

def calculate_2(masukan):
    operator = '+-*/'
    masukan.sort(reverse=True)
    # print(masukan)
    equation = [str(masukan[0])]
    masukan.remove(masukan[0])
    
    while masukan != []:
        daftar = list()
        angka = masukan[0]
        # for angka in masukan: # coba untuk semua angka
        for op in operator: # coba untuk semua operator
            for place in range(1,len(equation)+1,2):#operator,angka
                temp_eq = equation.copy()
                temp_eq.insert(place,str(angka))
                temp_eq.insert(place,op)
                # print('tempeq1',temp_eq)
                daftar.append((temp_eq,angka))
            for place in range(0,len(equation)+1,2):#angka,operator
                temp_eq = equation.copy()
                temp_eq.insert(place,op)
                temp_eq.insert(place,str(angka))
                # print('tempeq2',temp_eq)
                daftar.append((temp_eq,angka))
        maks = greedy(daftar)
        # print('maks',maks[0],maks[1])
        equation = maks[0]
        print('currentselected',equation)
        # print('remove',maks[1])
        masukan.remove(maks[1])
    equation = ''.join(equation)
    # print ('point',countPoint(equation,eval(equation)))
    return equation

def countPoint(exp,result):
    point=-1*abs(24-result)
    for char in exp:
        if char=='+':
            point+=5
        elif char=='-':
            point+=4
        elif char=='*':
            point+=3
        elif char=='/':
            point+=2
        elif char=='(':
            point-=1
    return point

def valid_eq(equation):
    operator = '+-*/'
    flag = False
    if equation[0] in operator :
        return False
    else:
        for char in equation:
            if char in operator:
                if flag:
                    return False
                else:
                    flag = True
            elif char == '(':
                flag = True
            else:
                flag = False
        return True

def greedy(daftar):
    braket2 = [()]
    # braket3 = [(0,4),(2,6)]
    braket4 = [(),(0, 4),(2, 6),(4, 8),(0, 6),(2, 8),(0, 4, 6, 10), (0, 5,1, 8), (0, 7,3, 8), (2, 7,3, 10), (2, 9,5, 10)]
    first = True
    # print(daftar)
    for pasang in daftar:
        # print('checking',pasang[0])
        exp = pasang[0]
        angka = pasang[1]
        # print(len(exp))
        # a=braket3 if len(exp)==5 else (braket4 if len(exp)==7 else braket2)
        # print(a)
        for bracket in (braket4 if len(exp)==7 else braket2):
            # print(bracket)
            exp_temp=exp.copy()
            for indexinsert,brac in zip(bracket,'()()'):
                exp_temp.insert(indexinsert,brac)
            equation = ''.join(exp_temp)
            try: 
                if (valid_eq(equation)):
                    hasil = eval(equation)
                else:
                    continue
            except:
                continue
            if first: # iterasi pertama
                max_point = countPoint(exp_temp,hasil)
                select_eq = exp_temp
                selected = angka
                first = False
                # print('first',equation)
            else:
                temp_point = countPoint(exp_temp,hasil)
                if (max_point<temp_point):
                    max_point = temp_point
                    select_eq = exp_temp
                    selected = angka
                # print(equation,' ',temp_point,' ',max_point)
            # print(equation,'maxpoint=', max_point)
    return [select_eq,selected]