import tkinter as tk
from tkinter import filedialog

bground = 'lightgrey'
fontheader = ('Calibri',16)
font1 = ('Calibri',12)
font2 = ('Calibri',10)
open_file = 'Nu sunt fisiere selectate'

mainwindow=tk.Tk()
mainwindow.configure(padx=20,background=bground)
mainwindow.title('Print PDF')

def print():

    from pypdf import PdfWriter
    merger = PdfWriter()
    
    global open_file
    global lblrezultate
    global lblconversie

    index=0

    for pdf in open_file:
        try:
            if pdf.find('.pdf')>=0:
                merger.append(pdf)
                index+=1
        except:
            pass    
    merger.write("result.pdf")

    import os
    import subprocess
    import platform
    import locale

    if index>0:
        if platform.system() == 'Windows':
            args = '"C:\\Program Files\\gs\\gs10.02.1\\bin\\gswin64c" ' \
                '-sDEVICE=mswinpr2 ' \
                '-dBATCH ' \
                '-dNOPAUSE ' \
                '-dFitPage ' \
                '-sOutputFile="%printer%myPrinterName" '
            ghostscript = args + "result.pdf"
            subprocess.call(ghostscript, shell=True)
        elif platform.system() =='Linux':
            args = '/bin/gs ' \
                '-sDEVICE=deskjet ' \
                '-dBATCH ' \
                '-dNOPAUSE ' \
                '-dFitPage ' \
                '-sOutputFile="%printer%myPrinterName" '
            ghostscript = args + os.getcwd+"/result.pdf"
            subprocess.call(ghostscript, shell=True)
        if index==len(open_file):
            lblconversie.config(text='Au fost printate '+str(index)+' fisiere',fg='BLACK')
        else:
            lblconversie.config(text='Au fost printate '+str(index)+' fisiere',fg='RED')
    else:
        lblconversie.config(text='Nu au fost printate fisiere',fg='RED')
        

    try:
        os.remove("result.pdf")
    except:
        pass


def openfiles():
    global open_file
    global lblimport
    global lblrezultate
    open_file=filedialog.askopenfilenames(defaultextension='pdf')
    lblimport.config(text=str(len(open_file))+' fisiere selectate',fg='BLACK')
    lblrezultate.config(text='')
    
lblheader=tk.Label(mainwindow,font=fontheader,wraplength=380,background=bground,fg='GREY',text='Printare PDF',pady=20)
lblheader.pack(expand=True)

btnimport=tk.Button(mainwindow,text='Selectare fisiere PDF',font=font1,command=lambda:openfiles(),width=38)
btnimport.pack()

lblimport=tk.Label(mainwindow,font=font2,wraplength=380,background=bground,fg='RED',text=open_file)
lblimport.pack(expand=True)

btnprint=tk.Button(mainwindow,text='Print',font=font1,command=lambda:print(),width=38)
btnprint.pack()

lblconversie=tk.Label(mainwindow,font=font2,wraplength=380,background=bground,text='Nu s-a printat nici un fisier')
lblconversie.pack()

btnquit=tk.Button(mainwindow,text='Iesire',font=font1,command=lambda:mainwindow.destroy(),width=38)
btnquit.pack()

lblrezultate=tk.Label(mainwindow,font=font2,wraplength=380,background=bground,fg='RED')
lblrezultate.pack(expand=True)

mainwindow.mainloop()