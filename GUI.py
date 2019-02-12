from tkinter import *
from tkinter import ttk,messagebox
from random import choice
from GameEngine import calculate,countPoint


#inisialisasi variabel global
FONT=('Segoe UI Semilight',15)
root = Tk()
root.title('24 Solver dengan Algoritma Greedy')
root.iconbitmap('data/gameicon.ico') #hanya berfungsi di platform windows
root.resizable(False, False)
topFrame1=Frame(root)
topFrame2=Frame(root)
middleFrame=Frame(root)
bottomFrame=Frame(root)
canvas=Canvas(topFrame1, width=650,height=630)
bg_img=PhotoImage(file='data/BackGround.ppm')
bg=canvas.create_image(0,0,image=bg_img,anchor='nw')
allCard=selectedCard=selectedDeck=backCover=[]
mode=1 #0 = mode manual,1=mode acak

class Card:#class card untuk menyimpan gambar kartu dan melakukan animasi
    def __init__(self,imagename,xpos,ypos):
        self.imagefile=PhotoImage(file=imagename)
        self.image=canvas.create_image(xpos,ypos,image=self.imagefile,anchor='nw')
        self.name=imagename
        self.xpos=xpos
        self.ypos=ypos
    def moveCard(self,Position,Direction):
        if Direction=='in':
            multiplier=-1
        elif Direction=='out':
            multiplier=1
        if Position==0:
            deltax=-21.5
            deltay=-15.5
        elif Position==1:
            deltax=21.5
            deltay=-15.5
        elif Position==2:
            deltax=-21.5
            deltay=15.5
        elif Position==3:
            deltax=21.5
            deltay=15.5
        elif Position==4:
            deltax=-21.5
            deltay=0
        for i in range(0,10):
            canvas.move(self.image,deltax*multiplier,deltay*multiplier)
            canvas.update()
            root.after(1)
        coord=canvas.coords(self.image)
        self.xpos=coord[0]
        self.ypos=coord[1]

def initGame():#inisialisasi GUI
    global allCard,selectedCard,selectedDeck,backCover
    allCard=['data/'+str(x)+str(y)+'.png' for x in range(1,14) for y in ['C','H','D','S']]
    selectedCard=['none']*4
    selectedDeck=['none']*4
    backCover='none'
    assignCard()
    lbl_eval['text']=lbl_result['text']=lbl_point['text']=''
    lbl_indikator['text']='52'

def drawCard():#animasi untuk melakukan pengambilan kartu
    global selectedCard
    global selectedDeck
    if selectedDeck[0]=='none':
        messagebox.showinfo('Kartu Dek Habis','Anda tidak dapat ambil kartu lagi karena kartu di dek sudah habis. Lakukan pengocokan kembali terlebih dahulu!')
    else:
        btn_modemanual.state(["disabled"])
        btn_moderandom.state(["disabled"])
        btn_draw.state(["disabled"])
        btn_reshuffle.state(["disabled"])
        btn_solve.state(["disabled"])
        for idx,selected in enumerate(selectedDeck):
            selected.moveCard(idx,'out')        
            selectedCard[idx]=Card(selected.name,selected.xpos,selected.ypos)
            lbl_indikator['text']=str(int(lbl_indikator['text'])-1)
        lbl_eval['text']=lbl_result['text']=lbl_point['text']=''
        assignCard()
        btn_draw.state(["!disabled"])
        btn_reshuffle.state(["!disabled"])
        btn_solve.state(["!disabled"])
        btn_modemanual.state(["!disabled"])
        btn_moderandom.state(["!disabled"])

def createCard():#pembuatan instance kartu baru
    global allCard
    if len(allCard)>=1:
        tempSelected=choice(allCard)
        result=Card(tempSelected,225,165)
        allCard.remove(tempSelected)
    else:
        result='none'
    return result


def assignCard():#pemilihan kartu dari deck yang tersisa 
#card0 diambil dari backcover sedangkan lainnya assign card baru, 
# jadi setiap assignCard() assign 1 card untuk backCover dan 3 untuk card2,3,4
    global selectedDeck
    global allCard
    global backCover
    if backCover!='none': #simpan value backCover
        tempCard=Card(backCover.name,backCover.xpos,backCover.ypos)
    else:
        tempCard='none'
    if len(allCard)>3: #ketika sisa kartu di dek tinggal 3 berarti backcover tidak perlu diassign lagi
        backCover=createCard()
    else:
        backCover='none'
    for i in range(3,-1,-1):
        if i==0 and tempCard!='none':
            selectedDeck[i]=Card(tempCard.name,tempCard.xpos,tempCard.ypos)
        else:
            selectedDeck[i]=createCard()
    
def reshuffle():#animasi untuk pengocokan kartu dek  
    global selectedCard
    btn_draw.state(["disabled"])
    btn_reshuffle.state(["disabled"])
    btn_solve.state(["disabled"])
    btn_modemanual.state(["disabled"])
    btn_moderandom.state(["disabled"])
    if selectedCard[0]!='none':# cek apakah selected deck sudah terassign
        for i in range(0,4):
            selectedCard[i]=Card(selectedCard[i].name,selectedCard[i].xpos,selectedCard[i].ypos)
            selectedCard[i].moveCard(i,'in') 
        tempCover=Card(selectedCard[3].name,selectedCard[3].xpos,selectedCard[3].ypos)#simpan nilainya sebelum di init ulang
    else:
        tempCover=Card(selectedDeck[0].name,selectedDeck[0].xpos,selectedDeck[0].ypos)
    initGame()
    selectedCard[0]=Card(tempCover.name,tempCover.xpos,tempCover.ypos)#create ulang supaya terletak di layer paling atas
    selectedCard[0].moveCard(4,'out')
    selectedDeck[0]=Card(selectedDeck[0].name,selectedDeck[0].xpos,selectedDeck[0].ypos)#create ulang supaya terletak di layer paling atas
    selectedCard[0].moveCard(4,'in')
    selectedCard=['none']*4
    btn_draw.state(["!disabled"])
    btn_reshuffle.state(["!disabled"])
    btn_solve.state(["!disabled"])
    btn_modemanual.state(["!disabled"])
    btn_moderandom.state(["!disabled"])

def solve():#untuk memanggil backend dan mendapatkan solusi
    valid=False
    if mode==1:
        if selectedCard[0]=='none':
            messagebox.showinfo('Kartu Belum Diambil','Anda tidak dapat melakukan perhitungan karena belum ada kartu terpilih. Lakukan ambil kartu dahulu!')
        else:
            valid=True
            inputNumber=[]
            for selected in selectedCard:
                tempNumber=(selected.name).replace('data/','').replace('.png','')
                tempNumber=int(tempNumber[:len(tempNumber)-1])
                inputNumber.append(tempNumber)
    else:#mode=0
        try:
            inputNumber=[int(entry1.get()),int(entry2.get()),int(entry3.get()),int(entry4.get())]
            valid=True
            for number in inputNumber:
                if number>13:
                    valid=False
            if valid==False:
                messagebox.showinfo('Input Salah','Input harus berupa angka dari 1 sampai 13!')            
        except:
            messagebox.showinfo('Input Salah','Input harus berupa angka dari 1 sampai 13!')
    
    if valid==True:
        result=calculate(inputNumber)
        lbl_result['text']=result[0]
        lbl_eval['text']=str(round(result[1],3))
        lbl_point['text']=str(round(countPoint(result[0],result[1],1),3))

def modeManual():#GUI bentuk input 4 angka manual
    global mode
    mode=0
    #buang frame1
    topFrame1.grid_remove()
    btn_draw.grid_remove()
    btn_reshuffle.grid_remove()
    btn_modemanual.grid_remove()
    lbl_indikator.grid_remove()
    lbl_indikator_txt.grid_remove()
    #munculkan frame2
    topFrame2.grid(row=0,pady=10)
    btn_moderandom.grid(row=0,column=0,sticky='w',padx=12,ipadx=2,ipady=2)
    lbl_point_txt.grid(row=0,column=1,sticky='w')
    lbl_point.grid(row=0,column=2,sticky='w')
    entry1_txt.grid(row=0,column=0,padx=9,pady=3)
    entry1.grid(row=0,column=1,padx=9,pady=3)
    entry2_txt.grid(row=0,column=2,padx=9,pady=3)
    entry2.grid(row=0,column=3,padx=9,pady=3)
    entry3_txt.grid(row=1,column=0,padx=9,pady=3)
    entry3.grid(row=1,column=1,padx=9,pady=3)
    entry4_txt.grid(row=1,column=2,padx=9,pady=3)
    entry4.grid(row=1,column=3,padx=9,pady=3)
    #hapus text
    lbl_eval['text']=lbl_result['text']=lbl_point['text']=''


def modeRandom():#GUI bentuk 4 angka terambil secara acak
    global mode
    mode=1
    #munculkan frame1
    topFrame1.grid(row=0)
    btn_modemanual.grid(row=0,column=0,sticky='w',padx=12,pady=4,ipadx=2,ipady=2)
    btn_solve.grid(row=0,column=1,sticky='w',padx=12,pady=4,ipadx=2,ipady=2)
    btn_draw.grid(row=0,column=2,sticky='w',padx=12,pady=4,ipadx=2,ipady=2)
    btn_reshuffle.grid(row=0,column=3,sticky='w',padx=12,pady=4,ipadx=2,ipady=2)
    lbl_indikator_txt.grid(row=0,column=0,sticky='w')
    lbl_indikator.grid(row=0,column=1,sticky='w')
    lbl_result_txt.grid(row=1,column=0,sticky='w')
    lbl_result.grid(row=1,column=1,sticky='w')
    lbl_point_txt.grid(row=0,column=2,sticky='w')
    lbl_point.grid(row=0,column=3,sticky='w')
    lbl_eval_txt.grid(row=1,column=2,sticky='w')
    lbl_eval.grid(row=1,column=3,sticky='w')
    #buang frame2
    topFrame2.grid_remove()
    btn_moderandom.grid_remove()
    entry1_txt.grid_remove()
    entry1.grid_remove()
    entry2_txt.grid_remove()
    entry2.grid_remove()
    entry3_txt.grid_remove()
    entry3.grid_remove()
    entry4_txt.grid_remove()
    entry4.grid_remove()
    #hapus text
    lbl_eval['text']=lbl_result['text']=lbl_point['text']=''

#bentuk semua object di window
ttkStyle = ttk.Style()
ttkStyle.configure('my.TButton', font=FONT)
lbl_indikator_txt=Label(bottomFrame,text='Jumlah sisa kartu :',font=FONT,width=14,height=1,relief="groove")
lbl_result_txt=Label(bottomFrame,text='Persamaan :',font=FONT,width=14,height=1,relief="groove")
lbl_point_txt=Label(bottomFrame,text='Poin :',font=FONT,width=14,height=1,relief="groove")
lbl_eval_txt=Label(bottomFrame,text='Hasil Evaluasi :',font=FONT,width=14,height=1,relief="groove")
lbl_indikator=Label(bottomFrame,text='',font=FONT,width=14,height=1,relief="groove")
lbl_result=Label(bottomFrame,text='',font=FONT,width=14,height=1,relief="groove")
lbl_point=Label(bottomFrame,text='',font=FONT,width=14,height=1,relief="groove")
lbl_eval=Label(bottomFrame,text='',font=FONT,width=14,height=1,relief="groove")
btn_draw=ttk.Button(middleFrame,text='Ambil Kartu', style='my.TButton',command=drawCard)
btn_solve=ttk.Button(middleFrame,text='Hitung', style='my.TButton',command=solve)
btn_reshuffle=ttk.Button(middleFrame,text='Kocok Ulang',style='my.TButton',command=reshuffle)
btn_modemanual=ttk.Button(middleFrame,text='Mode Manual',style='my.TButton',command=modeManual)
btn_moderandom=ttk.Button(middleFrame,text='Mode Acak',style='my.TButton',command=modeRandom)
entry1=Entry(topFrame2,font=FONT,width=14,bd=3)
entry2=Entry(topFrame2,font=FONT,width=14,bd=3)
entry3=Entry(topFrame2,font=FONT,width=14,bd=3)
entry4=Entry(topFrame2,font=FONT,width=14,bd=3)
entry1_txt=Label(topFrame2,text='Angka 1 :',font=FONT,width=7,height=1)
entry2_txt=Label(topFrame2,text='Angka 2 :',font=FONT,width=7,height=1)
entry3_txt=Label(topFrame2,text='Angka 3 :',font=FONT,width=7,height=1)
entry4_txt=Label(topFrame2,text='Angka 4 :',font=FONT,width=7,height=1)

#taruh object sesuai grid
topFrame1.grid(row=0)
topFrame2.grid(row=0,pady=10)
middleFrame.grid(row=1)
bottomFrame.grid(row=2)
canvas.grid()

#initialisasi game dan looping
initGame()
modeRandom()
root.mainloop()