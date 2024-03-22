import zipfile
import os
import tkinter as tk
from tkinter import filedialog
import datetime
import requests

bground = 'lightgrey'
fontheader = ('Calibri',16)
font1 = ('Calibri',12)
font2 = ('Calibri',10)
open_file = 'Nu sunt fisiere selectate'
write_file = 'Nu exista cale pentru salvare'

mainwindow=tk.Tk()
mainwindow.configure(padx=20,background=bground)
mainwindow.title('Conversie ZIP XML')

def openfiles():
    global open_file
    global lblimport
    global lblrezultate
    open_file=filedialog.askopenfilenames(defaultextension='zip')
    lblimport.config(text=str(len(open_file))+' fisiere selectate',fg='BLACK')
    lblrezultate.config(text='')

def writefiles():
    global write_file
    global lblexport
    write_file=filedialog.askdirectory()
    lblexport.config(text=str(write_file),fg='BLACK')

def conversie():

    global write_file
    global open_file
    global lblrezultate
    global lblconversie
    index=0

    lblrezultate.config(text='')
    lblrezultate.update()
    lblconversie.config(text='Conversie in curs')
    lblconversie.update()

    for filename in open_file:
        if filename.find('.zip')>0:
            try:
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    index+=1
                    for zippedFile in zip_ref.filelist:
                        xmlFile=zip_ref.extract(zippedFile,write_file)
            except:
                lblrezultate.config(text=lblrezultate.cget('text')+'\n'+'Nu a fost despachetat fisierul'+zippedFile.split('/')[len(zippedFile.split('/'))-1])
    lblrezultate.config(text='Au fost despachetate '+str(index)+' fisiere'+'\n'+lblrezultate.cget('text'))
    if index==len(open_file):
        lblrezultate.config(fg='BLACK')
    else:
        lblrezultate.config(fg='RED')
    lblrezultate.update()
    lblconversie.config(text='Conversie terminata')

lblheader=tk.Label(mainwindow,font=fontheader,wraplength=380,background=bground,fg='GREY',text='Conversie ZIP in XML',pady=20)
lblheader.pack(expand=True)

btnimport=tk.Button(mainwindow,text='Selectare fisiere ZIP',font=font1,command=lambda:openfiles(),width=38)
btnimport.pack()

lblimport=tk.Label(mainwindow,font=font2,wraplength=380,background=bground,fg='RED',text=open_file)
lblimport.pack(expand=True)

btnexport=tk.Button(mainwindow,text='Selectare locatie fisiere XML',font=font1,command=lambda:writefiles(),width=38)
btnexport.pack()

lblexport=tk.Label(mainwindow,font=font2,wraplength=380,background=bground,fg='RED',text=write_file)
lblexport.pack(expand=True)

btnconversie=tk.Button(mainwindow,text='Conversie',font=font1,command=lambda:conversie(),width=38)
btnconversie.pack()

lblconversie=tk.Label(mainwindow,font=font2,wraplength=380,background=bground,text='Nu au fost efectuate conversii')
lblconversie.pack()

btnquit=tk.Button(mainwindow,text='Iesire',font=font1,command=lambda:mainwindow.destroy(),width=38)
btnquit.pack()

lblrezultate=tk.Label(mainwindow,font=font2,wraplength=380,background=bground,fg='RED')
lblrezultate.pack(expand=True)

mainwindow.mainloop()