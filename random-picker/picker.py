#coding:utf-8
#Imports
import random
import tkinter as tk

#Values
filename = "data.ini"
running = False
noRepeat = True
index = 0

#Functions
def load_json():
    """Load the name list from the json file"""
    import json
    with open(filename,'r') as f:
        data = json.load(f) #The name list data
    return data

def load_number_list(ndata,namelist):
    """Ndata is the value which load_names() returns.
       Use this dict to out some numbers"""
    out_list = ndata[u'out']
    num_list = list(range(1,62 + 1)) #The base list. 62 is the number of students.
    for j in out_list:
        i = namelist.index(j) + 1
        try:
            num_list.remove(i)
        except:
            pass
    rep_list = ndata[u'repeat']
    for j in rep_list.keys():
        i = namelist.index(j) + 1
        num_list.extend([int(i)]*rep_list[j]) #Repeat the number i for rep_list[i] times
    return num_list

def load_name_list(ndata):
    """Ndata is the value which load_names() returns.
       Use this dict to out the name list"""
    return ndata[u'name']

def random_num_list(numlist):
    """Returns the random version of numlist"""
    return random.shuffle(numlist)

def look_up_name(number,namelist):
    """Returns the name of the number from the namelist"""
    return namelist[number - 1]

def btn():
    """The handle function of the button."""
    global running
    global chVarDis,root,lbl_number,lbl_name,btn_main,ckb
    global nameStr,numberStr,btnStr
    global num_list
    
    running = not running
    if running:
        nameStr.set("")
        numberStr.set("")
        random_num_list(num_list)
        btnStr.set(u"停止")
    else:
        nameStr.set(look_up_name(int(numberStr.get()),name_list))
        btnStr.set(u"点击开始抽号")
        noRepeat = bool(chVarDis.get())
        if noRepeat:
            while int(numberStr.get()) in num_list:
                num_list.remove(int(numberStr.get()))
            if len(num_list) <= 2:
                num_list = load_number_list(json_data)
def update():
    """Update the textbox."""
    global numberStr,index,num_list,running,root,json_data
    if running:
        if index >= len(num_list):
            index = 0
        numberStr.set(str(num_list[index]))
        index += 1
    root.after(25,update)

def tk_init():
    """The init and main function of tk."""
    global chVarDis,root,lbl_number,lbl_name,btn_main,ckb
    global nameStr,numberStr,btnStr
    from tkinter import font
    root = tk.Tk() #Create the window
    root.title(u'随机点号器')
    root.minsize(300,350)
    root.maxsize(300,350)
    root.after(25,update)
    chVarDis = tk.IntVar()
    nameStr = tk.StringVar()
    numberStr = tk.StringVar()
    btnStr = tk.StringVar()
    btnStr.set(u"点击开始抽号")
    lblFt = font.Font(size=60)
    btnFt = font.Font(size=30)
    ckbFt = font.Font(size=24)
    lbl_number = tk.Label(root,font=lblFt,textvariable=numberStr)
    lbl_number.pack(fill=tk.X)
    lbl_name = tk.Label(root,font=lblFt,textvariable=nameStr)
    lbl_name.pack(fill=tk.X)
    btn_main = tk.Button(root,command=btn,font=btnFt,textvariable=btnStr)
    btn_main.pack(fill=tk.X)
    ckb = tk.Checkbutton(root,text=u'不重复抽号',font=btnFt,variable = chVarDis)
    ckb.select()
    ckb.pack(fill=tk.X)
    root.mainloop()

#Mains
def main():
    global json_data,name_list
    global num_list
    json_data = load_json()
    name_list = load_name_list(json_data)
    num_list = load_number_list(json_data,name_list)
    random_num_list(num_list)
    tk_init()

#Runs main()
if __name__ == "__main__":
    main()
