#coding: utf-8
#0.1.0
import Tkinter as tk
import csv
import random
import time
import base64
import os
import codecs
from icon import img

class Word:
    def __init__(self,iid=0,wword="",mean="",sent="",arti="",book=0):
        self.id=iid
        self.word=wword
        self.mean=mean
        self.sent=sent
        self.arti=arti
        self.book=book
        

setting={}
data=[Word()]*50000
arti_id=[]
for i in range(50):
    arti_id.append([59999,0])
id_used=[]
mbook={'七上':1,'七下':2,'八上':3,'八下':4,'九上':5,'九下':6}
lbook=['','七上','七下','八上','八下','九上','九下']
marti={'桃花源记':(1,3),'与朱元思书':(2,4),'送东阳马生序':(3,4),'岳阳楼记':(4,4),'生于忧患，死于安乐':(5,6),'鱼我所欲也':(6,6),'曹刿论战':(7,6),'邹忌讽齐王纳谏':(8,6),'爱莲说':(9,3),'马说':(10,4),'小石潭记':(11,4),'醉翁亭记':(12,4),'愚公移山':(13,6),'论语':(14,1),'口技':(15,2),'陋室铭':(16,3),'三峡':(17,3),'记承天寺夜游':(18,3),'出师表':(19,5)}
larti=["","桃花源记","与朱元思书","送东阳马生序","岳阳楼记","生于忧患，死于安乐","鱼我所欲也","曹刿论战","邹忌讽齐王纳谏","爱莲说","马说","小石潭记","醉翁亭记","愚公移山","论语","口技","陋室铭","三峡","记承天寺夜游","出师表"]
artis=19
aans=""
pprob=Word()
vartis=[]
vbooks=[]
stabooks=[0,1,1,1,1,1,1]
idmax=0

def renew_book():
    global stabooks,vbooks,larti,marti,vartis
    for i in range(6):
        if stabooks[i+1]!=vbooks[i].get():
            
            stabooks[i+1]=vbooks[i].get()
            for j in larti[1:]:
                if marti[j][1]==i+1:
                    vartis[marti[j][0]-1].set(stabooks[i+1])
    renew()

def renew():
    global vartis,id_used,artis,arti_id,idmax
    id_used=[]
    idmax=0
    for i in range(artis):
        if vartis[i].get() and arti_id[i+1][1]-arti_id[i+1][0]>0:
            id_used.append(tuple(arti_id[i+1]))
            
            idmax+=(arti_id[i+1][1]-arti_id[i+1][0])
            #print(larti[i+1])
            #print("%d,%d"%(arti_id[i+1][0],arti_id[i+1][1]))
    if (idmax==0):
        vartis[0].set(1)
        i=0
        id_used.append(tuple(arti_id[i+1]))
        idmax+=(arti_id[i+1][1]-arti_id[i+1][0])
    #print(len(id_used))

def idmap(iid):
    global id_used,data,pprob
    tid=0
    sid=0
    #print(len(id_used))
    for each in id_used:
        tid+=(each[1]-each[0])
        if tid>=iid:
            
            pprob=data[(iid-sid-1+each[0])]
            #print("idmap:%d"%(pprob.id))
            return
        sid=tid
    pprob=data[0]
def get_prob():
    global idmax
    iid=random.randint(1,idmax)
    #print("get_prob:%d"%iid)
    return idmap(iid)

def read_setting():
    global setting
    with open('setting.ini','r') as f:
        lines=f.readlines()
        if lines[0][:3]==codecs.BOM_UTF8:
            lines[0]=lines[0][3:]
        for line in lines:
            if '=' in line:
                lt=line.split('=')
                setting[lt[0].strip(' ').strip('\r').strip('\n')]=lt[1].strip(' ').strip('\r').strip('\n')
                #print("Read %s=%s"%(lt[0].strip(' ').strip('\r').strip('\n'),lt[1].strip(' ').strip('\r').strip('\n')))

def read_data():
    global setting,data,idmax,arti_id,mbook,marti
    with open(setting['csv'],'rb') as myFile:
        lines=list(csv.reader(myFile))
    #print(lines[0])
    if lines[0][0][:3]==codecs.BOM_UTF8:
        #print("BOM")
        lines[0][0]=lines[0][0][3:]
    for line in lines:
        iid=int(line[0])
        line[0]=iid
        line[4]=marti[line[4]][0]
        line[5]=mbook[line[5]]
        data[iid]=Word(*line)
        artiid=data[iid].arti
        arti_id[artiid][0]=min(arti_id[artiid][0],iid)
        arti_id[artiid][1]=max(arti_id[artiid][1],iid+1)
        idmax+=1
    #print("%d ids."%idmax)
    for i in range(artis+1):
        if (arti_id[i][1]-arti_id[i][0]>0):
            id_used.append(tuple(arti_id[i]))

def hit_bans():
    global tword,tsent,tans,aans
    tans.set(aans)
def hit_bnext():
    global tword,tsent,tans,aans,pprob,tfrom
    global tbnext,tbans,setting
    tbans.set(setting['ansbut'])
    tbnext.set(setting['nextbut'])
    tans.set('')
    get_prob()
    #print("bnext:%d"%pprob.id)
    aans=pprob.mean
    tword.set(pprob.word)
    tsent.set(pprob.sent)
    tfrom.set('《'+larti[pprob.arti]+'》')

def draw_main():
    global tword,tsent,tans,tfrom,setting,vooks,vartis,aans,labout1,labout2,labout3,labout4,labout5,labout6,labout7,window
    global tbnext,tbans
    
    labout1.pack_forget()
    labout2.pack_forget()
    labout3.pack_forget()
    labout4.pack_forget()
    labout5.pack_forget()
    labout6.pack_forget()
    labout7.pack_forget()
    
    ckb=[]
    cka=[]
    lword=tk.Label(window,textvariable=tword,font=(setting['font'],int(setting['bsize'])))
    lword.pack()
    tword.set(setting['wr'])
    #print("p1")
    lsent=tk.Label(window,textvariable=tsent,font=(setting['font'],int(setting['bsize'])))
    lsent.pack()
    #print("p2")
    tsent.set(setting['sr'])
    lfrom=tk.Label(window,textvariable=tfrom,font=(setting['font'],int(setting['bsize'])))
    lfrom.pack()
    #print("p3")
    tfrom.set(setting['fr'])
    aans=setting['ans']
    tbans.set(setting['tbans0'])
    tbnext.set(setting['tbnext0'])
    bans=tk.Button(window,textvariable=tbans,command=hit_bans,font=(setting['font'],int(setting['ssize'])))
    bans.pack()
    lans=tk.Label(window,textvariable=tans,font=(setting['font'],int(setting['bsize'])))
    lans.pack()
    bnext=tk.Button(window,textvariable=tbnext,command=hit_bnext,font=(setting['font'],int(setting['ssize'])))
    bnext.pack()
    ltip=tk.Label(window,text=setting['ttip'],font=(setting['font'],int(setting['sssize'])))
    ltip.place(x=20,y=500,anchor='nw')
    for i in range(6):
        vbooks.append(tk.IntVar())
        vbooks[i].set(1)
        ckb.append(tk.Checkbutton(window, text=lbook[i+1], variable=vbooks[i], onvalue=1, offvalue=0,
                    command=renew_book))
        ckb[i].place(x=20+i/3*50,y=550+i%3*20,anchor='nw')
        #print("place %d:(%d,%d)"%(i,50+i/3*50,550+i%3*20))
    for i in range(artis):
        vartis.append(tk.IntVar())
        vartis[i].set(1)
        cka.append(tk.Checkbutton(window, text=larti[i+1], variable=vartis[i], onvalue=1, offvalue=0,
                    command=renew))
        cka[i].place(x=120+i/3*135,y=550+i%3*20,anchor='nw')
    
def main():
    global tword,tsent,tans,tfrom,setting,vooks,vartis,aans,labout1,labout2,labout3,labout4,labout5,labout6,labout7,window
    global tbans,tbnext
    read_setting()
    #print(setting)
    window=tk.Tk()
    #icon
    tmp=open("tmp.ico","wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    window.iconbitmap("tmp.ico")
    os.remove("tmp.ico")
    
    window.title(setting['title'])
    window.geometry(setting['size'])
    tword=tk.StringVar()
    tsent=tk.StringVar()
    tans=tk.StringVar()
    tfrom=tk.StringVar()
    tbans=tk.StringVar()
    tbnext=tk.StringVar()
    #about
    labout1=tk.Label(window,text=setting["about1"],font=(setting['font'],int(setting['bsize'])))
    labout1.pack()
    labout2=tk.Label(window,text=setting["about2"],font=(setting['font'],int(setting['bsize'])))
    labout2.pack()
    labout3=tk.Label(window,text=setting["about3"],font=(setting['font'],int(setting['bsize'])))
    labout3.pack()
    labout4=tk.Label(window,text=setting["about4"],font=(setting['font'],int(setting['bsize'])))
    labout4.pack()
    labout5=tk.Label(window,text=setting["about5"],font=(setting['font'],int(setting['bsize'])))
    labout5.pack()
    labout6=tk.Label(window,text=setting["about6"],font=(setting['font'],int(setting['bsize'])))
    labout6.pack()
    labout7=tk.Label(window,text=setting["about7"],font=(setting['font'],int(setting['bsize'])))
    labout7.pack()
    
    #/about
    
    read_data()
    #for i in data:
        #print("%d"%i.id)
    window.after(int(setting['startms']),draw_main)
    window.mainloop()

if __name__=="__main__":
    main()
