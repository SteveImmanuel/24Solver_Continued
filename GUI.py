from tkinter import *
from tkinter import ttk,messagebox
from random import choice
from GameEngine import calculate,calculate_2


#inisialisasi variabel global
FONT=('Segoe UI Semilight',15)
root = Tk()
root.title('24 Solver dengan Algoritma Greedy')
root.iconbitmap('data/gameicon.ico') #kalo di linux ini dicomment aja karna ga ngefek
root.resizable(False, False)
topFrame=Frame(root)
middleFrame=Frame(root)
bottomFrame=Frame(root)
canvas=Canvas(topFrame, width=640,height=630,bg='green')
allCard=selectedCard=selectedDeck=backCover=[]

class Card:
    def __init__(self,imagename,xpos,ypos):
        self.imagefile=PhotoImage(file=imagename)
        self.image=canvas.create_image(xpos,ypos,image=self.imagefile,anchor='nw')
        self.name=imagename
        self.xpos=xpos
        self.ypos=ypos
    def moveCard(self,Position,Direction):
        if Direction=='in':
            multiplier=-5
        elif Direction=='out':
            multiplier=5
        if Position==0:
            deltax=-4.2
            deltay=-3.1
        elif Position==1:
            deltax=4.2
            deltay=-3.1
        elif Position==2:
            deltax=-4.2
            deltay=3.1
        elif Position==3:
            deltax=4.2
            deltay=3.1
        elif Position==4:
            deltax=-4.2
            deltay=0
        for i in range(0,10):
            canvas.move(self.image,deltax*multiplier,deltay*multiplier)
            canvas.update()
            root.after(1)
        coord=canvas.coords(self.image)
        self.xpos=coord[0]
        self.ypos=coord[1]

def initGame(lbl_result,lbl_eval,lbl_point,lbl_indikator):
    global allCard,selectedCard,selectedDeck,backCover
    allCard=['data/'+str(x)+str(y)+'.png' for x in range(1,14) for y in ['C','H','D','S']]
    selectedCard=['none']*4
    selectedDeck=['none']*4
    backCover='none'
    assignCard()
    lbl_eval['text']=lbl_result['text']=lbl_point['text']=''
    lbl_indikator['text']='52'

def drawCard(lbl_result,lbl_eval,lbl_point,lbl_indikator,btn_draw,btn_reshuffle,btn_solve):
    global selectedCard
    global selectedDeck
    if selectedDeck[0]=='none':
        messagebox.showinfo('Kartu Dek Habis','Anda tidak dapat ambil kartu lagi karena kartu di dek sudah habis. Lakukan pengocokan kembali terlebih dahulu!')
    else:
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

def createCard():
    global allCard
    # print(len(allCard),allCard)
    if len(allCard)>=1:
        tempSelected=choice(allCard)
        result=Card(tempSelected,220,165)
        allCard.remove(tempSelected)
    else:
        result='none'
    return result


def assignCard(): 
#card0 diambil dari backcover sedangkan lainnya assign card baru, jadi setiap assignCard() assign 1 card buat backCover dan 3 buat card234
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
    
def reshuffle(lbl_result,lbl_eval,lbl_point,lbl_indikator,btn_draw,btn_reshuffle,btn_solve):  
    global selectedCard
    btn_draw.state(["disabled"])
    btn_reshuffle.state(["disabled"])
    btn_solve.state(["disabled"])
    if selectedCard[0]!='none':# cek apakah selected deck sudah terassign
        for i in range(0,4):
            selectedCard[i]=Card(selectedCard[i].name,selectedCard[i].xpos,selectedCard[i].ypos)
            selectedCard[i].moveCard(i,'in') 
        tempCover=Card(selectedCard[3].name,selectedCard[3].xpos,selectedCard[3].ypos)#simpan nilainya sebelum di init ulang
    else:
        tempCover=Card(selectedDeck[0].name,selectedDeck[0].xpos,selectedDeck[0].ypos)
    initGame(lbl_result,lbl_eval,lbl_point,lbl_indikator)
    selectedCard[0]=Card(tempCover.name,tempCover.xpos,tempCover.ypos)#create ulang supaya terletak di layer paling atas
    selectedCard[0].moveCard(4,'out')
    selectedDeck[0]=Card(selectedDeck[0].name,selectedDeck[0].xpos,selectedDeck[0].ypos)#create ulang supaya terletak di layer paling atas
    selectedCard[0].moveCard(4,'in')
    selectedCard=['none']*4
    btn_draw.state(["!disabled"])
    btn_reshuffle.state(["!disabled"])
    btn_solve.state(["!disabled"])

def solve(lbl_result,lbl_eval,lbl_point):
    if selectedCard[0]=='none':
        messagebox.showinfo('Kartu Belum Diambil','Anda tidak dapat melakukan perhitungan karena belum ada kartu terpilih. Lakukan ambil kartu dahulu!')
    else:
        inputNumber=[]
        for selected in selectedCard:
            tempNumber=(selected.name).replace('data/','').replace('.png','')
            tempNumber=int(tempNumber[:len(tempNumber)-1])
            inputNumber.append(tempNumber)
        result=calculate_2(inputNumber)
        lbl_result['text']=result[0]
        lbl_eval['text']=str(round(result[1],3))
        lbl_point['text']=str(round(result[2],3))

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
btn_draw=ttk.Button(middleFrame,text='Ambil Kartu', style='my.TButton',command=lambda:drawCard(lbl_result,lbl_eval,lbl_point,lbl_indikator,btn_draw,btn_reshuffle,btn_solve))
btn_solve=ttk.Button(middleFrame,text='Hitung', style='my.TButton',command=lambda:solve(lbl_result,lbl_eval,lbl_point))
btn_reshuffle=ttk.Button(middleFrame,text='Kocok Ulang',style='my.TButton',command=lambda:reshuffle(lbl_result,lbl_eval,lbl_point,lbl_indikator,btn_draw,btn_reshuffle,btn_solve))

#taruh semua object sesuai grid
topFrame.grid(row=0)
middleFrame.grid(row=1)
bottomFrame.grid(row=2)
canvas.grid()
btn_reshuffle.grid(row=0,column=0,sticky='w',padx=20,ipadx=2,ipady=2)
btn_draw.grid(row=0,column=1,sticky='w',padx=20,ipadx=2,ipady=2)
btn_solve.grid(row=0,column=2,sticky='w',padx=20,ipadx=2,ipady=2)
lbl_indikator_txt.grid(row=0,column=0,sticky='w')
lbl_indikator.grid(row=0,column=1,sticky='w')
lbl_result_txt.grid(row=1,column=0,sticky='w')
lbl_result.grid(row=1,column=1,sticky='w')
lbl_point_txt.grid(row=0,column=2,sticky='w')
lbl_point.grid(row=0,column=3,sticky='w')
lbl_eval_txt.grid(row=1,column=2,sticky='w')
lbl_eval.grid(row=1,column=3,sticky='w')

#initialisasi game dan looping
initGame(lbl_result,lbl_eval,lbl_point,lbl_indikator)
root.mainloop()