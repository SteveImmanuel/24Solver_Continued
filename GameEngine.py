# Kelompok sin
# Kamis 31/1/19
# back-end
# menghitung solusi 24 solver dari input dengan algoritma greedy

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
                daftar.append([temp_eq,angka])
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
    '''
    fungsi mencari persamaan dengan point optimum untuk solusi 
    permasalahan game 24 dari masukan yang ada
    '''
    masukan.sort(reverse=True)
    equation = [str(masukan[0])]
    masukan.remove(masukan[0])

    while masukan != []:
        maks = seleksi(masukan,equation)
        equation = maks[0]
        # print('selected',equation)
        masukan.remove(maks[1])
    # print ('point',countPoint(equation,eval(equation)))
    # yang direturn persamaan,total hasil evaluasi, dan point
    return (''.join(equation),maks[2],maks[3])

def seleksi(kandidat,solusi_now):
    '''
    fungsi menyeleksi kandidat dan mengembalikan persamaan
    dengan point terbesar
    greedy by point
    '''
    operator = '+-*/'
    angka = kandidat[0]
    daftar = list()
    for op in operator: # coba untuk semua operator
        for place in range(1,len(solusi_now)+1,2):#operator,angka
            temp_eq = solusi_now.copy()
            temp_eq.insert(place,str(angka))
            temp_eq.insert(place,op)
            daftar.append((temp_eq,angka))
        for place in range(0,len(solusi_now)+1,2):#angka,operator
            temp_eq = solusi_now.copy()
            temp_eq.insert(place,op)
            temp_eq.insert(place,str(angka))
            daftar.append((temp_eq,angka))
    return greedy(daftar)

def countPoint(exp,result):
    # menghitung point dari exp yang masuk dan result-nya
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
    '''
    mengecek apakah persamaan sudah valid
    yaitu yang tidak ada operator yang double
    tidak ada operator di depan
    dan tidak ada operator setelah (
    '''
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
    '''
    fungsi yang mengembalikan persamaan dari daftar yang
    memiliki jumlah point terbesar 
    dengan menggunakan kurung pada iterasi saat semua angka 
    telah terpilih
    '''
    braket2 = [()]
    braket4 = [(),(0, 4),(2, 6),(4, 8),(0, 6),(2, 8),(0, 4, 6, 10), (0, 5,1, 8), (0, 7,3, 8), (2, 7,3, 10), (2, 9,5, 10)]
    first = True
    for pasang in daftar:
        angka = pasang[1]
        for bracket in (braket4 if len(pasang[0])==7 else braket2):
            exp=pasang[0].copy()
            for indexinsert,brac in zip(bracket,'()()'):
                exp.insert(indexinsert,brac)
            equation = ''.join(exp)
            try: 
                if (valid_eq(equation)):
                    hasil = eval(equation)
                else:
                    continue
            except:
                continue
            if first: # iterasi pertama
                max_point = countPoint(exp,hasil)
                select_eq = exp
                selected = angka
                total = hasil
                first = False
            else:
                temp_point = countPoint(exp,hasil)
                if (max_point<temp_point):
                    max_point = temp_point
                    select_eq = exp
                    selected = angka
                    total = hasil
    return [select_eq,selected,total,max_point]

def greedy_not_kurung(daftar):
    '''
    fungsi yang mengembalikan persamaan dari daftar yang
    memiliki jumlah point terbesar tanpa menggunakan kurung
    '''
    first = True
    for pasang in daftar:
        exp = pasang[0]
        angka = pasang[1]
        equation = ''.join(exp)
        try: 
            hasil = eval(equation)
        except:
            continue
        if first: # iterasi pertama
            max_point = countPoint(exp,hasil)
            select_eq = exp
            selected = angka
            first=False
        else:
            temp_point = countPoint(exp,hasil)
            if (max_point<temp_point):
                max_point = temp_point
                select_eq = exp
                selected = angka
    return [select_eq,selected]