import zipfile
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import requests
import xml.etree.ElementTree as ET
from datetime import datetime as dt
import json

bground = 'lightgrey'
fontheader = ('Calibri',16)
fontsubheader = ('Calibri',14)
font1 = ('Calibri',12)
font2 = ('Calibri',10)
url='https://webservicesp.anaf.ro/prod/FCTEL/rest/transformare/FACT1'
Headers={'Content-Type':'text/plain','Accept':'*/*'}
open_file_zip = 'Nu sunt fisiere selectate'
write_file_xml = 'Nu exista cale pentru salvare'
open_file_xml = 'Nu sunt fisiere selectate'
write_file_pdf = 'Nu exista cale pentru salvare'
open_file_pdf = 'Nu sunt fisiere selectate'
path_zip = ''
path_xml = ''
path_pdf = ''

if os.path.isfile('director.json'):
    try:
        file = open('director.json','r')
        jsonfile = json.load(file)
        if "write_xml" in jsonfile:
            write_file_xml = jsonfile["write_xml"]
        if "write_pdf" in jsonfile:
            write_file_pdf = jsonfile["write_pdf"]
        if "path_zip" in jsonfile:
            path_zip = jsonfile["path_zip"]
        if "path_xml" in jsonfile:
            path_xml = jsonfile["path_xml"]
        if "path_pdf" in jsonfile:
            path_pdf = jsonfile["path_pdf"]
    except:
        pass


mainwindow=tk.Tk()
mainwindow.configure(padx=20,pady=20,background=bground)
mainwindow.title('eFactura Gospodarie Comunala SA')

def coloring():
    
    if open_file_zip != 'Nu sunt fisiere selectate' and os.path.isdir(write_file_xml) == True and len(open_file_zip)>0 and write_file_xml!='':
        btn_conversie_zip2xml.configure(bg='GREY')
        btn_zip_xml_pdf.configure(bg='GREY')
    else:
        btn_conversie_zip2xml.configure(bg='SystemButtonFace')
        btn_zip_xml_pdf.configure(bg='SystemButtonFace')

    if open_file_xml != 'Nu sunt fisiere selectate' and os.path.isdir(write_file_pdf) == True and len(open_file_xml)>0 and write_file_pdf!='':
        btn_conversie_xml2pdf.configure(bg='GREY')
    else:
        btn_conversie_xml2pdf.configure(bg='SystemButtonFace')

    if open_file_pdf != 'Nu sunt fisiere selectate' and len(open_file_pdf)>0:
        btn_print.configure(bg='GREY')
    else:
        btn_print.configure(bg='SystemButtonFace')

    btn_zip_xml_pdf.update()
    btn_conversie_xml2pdf.update()
    btn_conversie_zip2xml.update()
    btn_print.update()

def openzip():
    global open_file_zip
    global lbl_import_zip
    global lbl_rezultate
    global path_zip
    if os.path.isdir(path_zip):
        open_file_zip=filedialog.askopenfilenames(initialdir=path_zip,filetypes=[('zip files','*.zip')])
    else:
        open_file_zip=filedialog.askopenfilenames(filetypes=[('zip files','*.zip')])
    try:
        path_zip=os.path.dirname(open_file_zip[0])    
    except:
        pass
    changedir()
    lbl_import_zip.config(text=str(len(open_file_zip))+' fisiere selectate',fg='BLACK')
    lbl_rezultate.configure(text='Rezultate operatii',fg='BLACK')
    lbl_rezultate.update()
    coloring()

def openxml():
    global open_file_xml
    global lbl_import_xml
    global lbl_rezultate
    global path_xml
    if os.path.isdir(path_xml):
        open_file_xml=filedialog.askopenfilenames(initialdir=path_xml,filetypes=[('xml files','*.xml')])
    else:
        open_file_xml=filedialog.askopenfilenames(filetypes=[('xml files','*.xml')])
    try:
        path_xml=os.path.dirname(open_file_xml[0])
    except:
        pass
    changedir()
    lbl_import_xml.config(text=str(len(open_file_xml))+' fisiere selectate',fg='BLACK')
    lbl_rezultate.configure(text='Rezultate operatii',fg='BLACK')
    lbl_rezultate.update()
    coloring()

def openpdf():
    global open_file_pdf
    global lbl_import_pdf
    global lbl_rezultate
    global path_pdf
    if os.path.isdir(path_pdf):
        open_file_pdf=filedialog.askopenfilenames(initialdir=path_pdf,filetypes=[('pdf files','*.pdf')])
    else:
        open_file_pdf=filedialog.askopenfilenames(filetypes=[('pdf files','*.pdf')])
    try:
        path_pdf=os.path.dirname(open_file_pdf[0])
    except:
        pass
    changedir()
    lbl_import_pdf.config(text=str(len(open_file_pdf))+' fisiere selectate',fg='BLACK')
    lbl_rezultate.configure(text='Rezultate operatii',fg='BLACK')
    lbl_rezultate.update()
    coloring()

def changedir():
    global write_file_xml
    global write_file_pdf
    global path_pdf
    global path_xml
    global path_zip
    try:
        file = open('director.json','w')
        dictionary = { "write_xml": write_file_xml, "write_pdf": write_file_pdf, "path_zip":path_zip, "path_xml":path_xml, "path_pdf":path_pdf }
        jsonfile = json.dumps(dictionary)
        file.write(jsonfile)
        file.close()
    except:
        pass

def writexml():
    global write_file_xml
    global lbl_export_xml
    global open_file_xml
    write_file_xml=filedialog.askdirectory()
    lbl_export_xml.config(text=str(write_file_xml),fg='BLACK')
    changedir()
    lbl_rezultate.configure(text='Rezultate operatii',fg='BLACK')
    lbl_rezultate.update()
    coloring()

def writepdf():
    global write_file_pdf
    global lbl_export_pdf
    write_file_pdf=filedialog.askdirectory()
    lbl_export_pdf.config(text=str(write_file_pdf),fg='BLACK')
    changedir()
    lbl_rezultate.configure(text='Rezultate operatii',fg='BLACK')
    lbl_rezultate.update()
    coloring()

def generateFileName(xmltree,write_file):
    
    notAllowed=['<','>',':','"','/','\\','|','?','*']
    
    try:
        nrfact=xmltree.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID').text
    except:
        nrfact=''
    try:
        cui=xmltree.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingSupplierParty/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyTaxScheme/{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID').text
    except:
        cui=''
    if cui=='RO8574327':
        try:
            denumire=xmltree.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingCustomerParty/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity/{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}RegistrationName').text
        except:
            denumire=''
        try:
            cui=xmltree.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingCustomerParty/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyTaxScheme/{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID').text
        except:
            cui=''
    else:
        try:
            denumire=xmltree.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingSupplierParty/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity/{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}RegistrationName').text
        except:
            denumire=''
        try:
            cui=xmltree.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingSupplierParty/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyTaxScheme/{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID').text
        except:
            cui=''
    
    cui = str.strip(cui)
    denumire = str.strip(denumire)
    nrfact = str.strip(nrfact)

    pdf = str(denumire+' '+cui+' '+nrfact+'.pdf')

    for ch in notAllowed:
        pdf=pdf.replace(ch,'')

    pdf=write_file+'/'+pdf

    return pdf

def conversie_zip2xml():

    global write_file_xml
    global open_file_zip
    global lbl_rezultate
    global lbl_conversie_zip2xml
    converted_files = []
    index=0

    if open_file_zip == 'Nu sunt fisiere selectate' or os.path.isdir(write_file_xml) == False or len(open_file_zip)==0:
        error_text=''
        if open_file_zip == 'Nu sunt fisiere selectate' or len(open_file_zip) == 0:
            error_text += 'Nu sunt fisiere ZIP selectate'+'\n'
        if os.path.isdir(write_file_xml) == False:
            error_text += "   Director XML inexistent"
        messagebox.showerror('Eroare',error_text)
        return

    lbl_conversie_zip2xml.config(text='Conversie in curs')
    lbl_conversie_zip2xml.update()
    first=True
    for filename in open_file_zip:
        if filename.find('.zip')>0:
            try:
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    index+=1
                    for zippedFile in zip_ref.filelist:
                        xml_file=zip_ref.extract(zippedFile,write_file_xml)
                        if xml_file.find('semnatura') == -1:
                            converted_files.append(xml_file)
            except:
                if first:
                    lbl_rezultate.config(text='Nu a fost despachetat fisierul'+os.path.basename(zippedFile))
                    first=False   
                else:
                    lbl_rezultate.config(text=lbl_rezultate.cget('text')+'\n'+'Nu a fost despachetat fisierul'+os.path.basename(zippedFile))
    if first:
        lbl_rezultate.config(text='Au fost despachetate '+str(index)+' din '+str(len(open_file_zip))+' fisiere',fg='BLACK')
    else:
        lbl_rezultate.config(text='Au fost despachetate '+str(index)+' din '+str(len(open_file_zip))+' fisiere'+'\n'+lbl_rezultate.cget('text'),fg='RED')
    lbl_rezultate.update()
    lbl_conversie_zip2xml.config(text='Conversie terminata')
    open_file_zip = 'Nu sunt fisiere selectate'
    lbl_import_zip.configure(text=open_file_zip,fg='RED')
    lbl_import_zip.update()
    coloring()
    return converted_files

def conversie_xml2pdf():

    global open_file_xml
    global write_file_pdf
    global Headers
    global url
    global lbl_rezultate
    global lbl_conversie_xml2pdf
    converted_files = []
    error='Fisiere neprelucrate:'+'\n'

    lbl_import_xml.config(text=str(len(open_file_xml))+' fisiere selectate',fg='BLACK')

    if open_file_xml == 'Nu sunt fisiere selectate' or os.path.isdir(write_file_pdf) == False or len(open_file_xml)==0:
        error_text=''
        if open_file_xml == 'Nu sunt fisiere selectate' or len(open_file_xml) == 0:
            error_text += 'Nu sunt fisiere XML selectate'+'\n'
        if os.path.isdir(write_file_pdf) == False:
            error_text += "   Director PDF inexistent"
        messagebox.showerror('Eroare',error_text)
        return

    lbl_conversie_xml2pdf.config(text='Conversie in curs',fg='RED')
    lbl_conversie_xml2pdf.update()

    index = 0

    from tkinter.ttk import Progressbar

    message_window = tk.Toplevel()
    message_window.title('Conversie XML->PDF')
    message_window.configure(background=bground,padx=40,pady=40,width=200)
    lbl_title = tk.Label(message_window,text='Conversie in curs',font=font1,bg=bground,pady=10)
    lbl_title.pack()
    lbl_stadiu = tk.Label(message_window,text='',bg=bground,fg='RED',font=font1,pady=10)
    lbl_stadiu.pack(expand=True)
    lbl_fisier = tk.Label(message_window,text='',bg=bground,fg='RED',font=font2,pady=10)
    lbl_fisier.pack(expand=True)
    message_window.focus()

    first=True

    for xml in open_file_xml:

        try:           
            xmltree=ET.parse(xml)
            root=xmltree.getroot()
            strBody=ET.tostring(root,encoding='utf-8')
            pdf=generateFileName(xmltree,write_file_pdf)
            #pdf=write_file_pdf+'/'+xml.split('/')[len(xml.split('/'))-1].replace('.xml','')+'.pdf'
            #if os.path.isfile(pdf):
            #            index+=1
            #else:
            try:
                result=requests.post(url,strBody,headers=Headers)
                lbl_fisier.configure(text='')
                lbl_fisier.update()
                trial = 1
                while str(result.content).find('%PDF-1.5')==-1 and trial<50:
                    result=requests.post(url,strBody,headers=Headers)
                    lbl_fisier.configure(text='Se prelucreaza '+os.path.basename(xml))
                    lbl_fisier.update()
                    trial +=1
                if str(result.content).find('%PDF-1.5')!=-1:
                    pdffile=open(pdf,'wb')
                    pdffile.write(result.content)
                    pdffile.close()
                    index+=1
                    converted_files.append(pdf)
                    lbl_conversie_xml2pdf.config(text='Au fost convertite '+str(index)+' fisiere',fg='RED')
                    lbl_conversie_xml2pdf.update()
                    lbl_stadiu.config(text='Au fost convertite '+str(index)+' fisiere din '+str(len(open_file_xml)),fg='RED')
                    lbl_stadiu.update()
                else:       
                    if first:
                        lbl_rezultate.config(text='Nu s-au creat toate pdf')
                        first = False
                    else:
                        pass
                    lbl_rezultate.update()
                    error=error+os.path.basename(xml)+'\n'
            except Exception as e:
                if first:
                    lbl_rezultate.config(text='Nu s-au creat toate pdf')
                    print(e)
                    first = False
                else:
                    pass
                lbl_rezultate.update()
                error=error+os.path.basename(xml)+'\n'
        except Exception as e:
            if first:
                lbl_rezultate.config(text='Nu s-au creat toate pdf')
                print(e)
                first = False
            else:
                pass
            lbl_rezultate.update()
            error=error+os.path.basename(xml)+'\n'
    if index==len(open_file_xml):
        lbl_rezultate.config(text='Au fost create '+str(index)+' din '+str(len(open_file_xml))+' fisiere pdf',fg='BLACK')
    else:
        lbl_rezultate.config(text='Au fost create '+str(index)+' din '+str(len(open_file_xml))+' fisiere pdf'+'\n'+lbl_rezultate.cget('text'),fg='RED')
        errorfile=open(write_file_pdf+'/Error '+str(dt.now().strftime("%Y-%m-%d %H-%M-%S"))+'.txt','w')
        errorfile.write(error)
    lbl_conversie_xml2pdf.config(text='Conversie terminata',fg='BLACK')
    message_window.destroy()
    open_file_xml = 'Nu sunt fisiere selectate'
    lbl_import_xml.configure(text=open_file_xml,fg='RED')
    lbl_import_xml.update()
    coloring()
    return converted_files

def print():

    from pypdf import PdfWriter
    merger = PdfWriter()
    
    global open_file_pdf
    global lbl_rezultate
    global lbl_print
    MaxDictStack = -1

    lbl_import_pdf.config(text=str(len(open_file_pdf))+' fisiere selectate',fg='BLACK')

    index=0

    if open_file_pdf == 'Nu sunt fisiere selectate' or len(open_file_pdf) == 0:
        error_text=''
        error_text += 'Nu sunt fisiere PDF selectate'+'\n'
        messagebox.showerror('Eroare',error_text)
        return

    for pdf in open_file_pdf:
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
        if index==len(open_file_pdf):
            lbl_print.config(text='Au fost printate '+str(index)+' din '+str(len(open_file_pdf))+' fisiere',fg='BLACK')
        else:
            lbl_print.config(text='Au fost printate '+str(index)+' din '+str(len(open_file_pdf))+' fisiere',fg='RED')
    else:
        lbl_print.config(text='Nu au fost printate fisiere',fg='RED')

    try:
        os.remove("result.pdf")
    except:
        pass

    if index == len(open_file_pdf):
        lbl_rezultate.configure(text=lbl_print.cget('text'),fg='BLACK')
    else:
        lbl_rezultate.configure(text=lbl_print.cget('text'),fg='RED')
    lbl_rezultate.update()
    open_file_pdf='Nu sunt fisiere selectate'
    lbl_import_pdf.configure(text=open_file_pdf,fg='RED')
    lbl_import_pdf.update()
    coloring()
    return index

def zip_xml_pdf():
    
    global write_file_xml
    global open_file_zip
    global lbl_rezultate
    global open_file_xml
    global write_file_pdf
    global open_file_pdf
    global lbl_print

    opened_files = len(open_file_zip)
    open_file_xml = conversie_zip2xml()
    open_file_pdf = conversie_xml2pdf()
    printed_pdf = print()
    if printed_pdf == opened_files:
        lbl_rezultate.configure(text='Au fost printate '+str(printed_pdf)+' din '+str(opened_files)+' fisiere',fg='BLACK')
    else:
        lbl_rezultate.configure(text='Au fost printate '+str(printed_pdf)+' din '+str(opened_files)+' fisiere',fg='RED')
    lbl_rezultate.update()

def lbl_export_pdf_command(event):
    global write_file_pdf
    path = os.path.normpath(write_file_pdf)
    try:
        os.startfile(path)
    except:
        pass

def lbl_export_xml_command(event):
    global write_file_xml
    path = os.path.normpath(write_file_xml)
    try:
        os.startfile(path)
    except:
        pass

fr_top = tk.Frame(mainwindow,bg=bground)
fr_top.pack(side='top')
fr_bottom = tk.Frame(mainwindow,bg=bground,padx=20,pady=20)
fr_bottom.pack(side='bottom')
fr_left_first = tk.Frame(mainwindow,bg=bground)
fr_left_first.pack(side='left')
fr_left = tk.Frame(fr_left_first,bg=bground,padx=20,pady=20)
fr_left.pack(side='left')
fr_center = tk.Frame(fr_left_first,bg=bground,padx=20,pady=20)
fr_center.pack(side='right')
fr_right = tk.Frame(mainwindow,bg=bground,padx=20,pady=20)
fr_right.pack(side='right')

lblheader=tk.Label(fr_top,font=fontheader,wraplength=380,background=bground,fg='GREY',text='eFactura Gospodarie Comunala')
lblheader.pack(expand=True)

lbl_zip2xml=tk.Label(fr_left,font=fontsubheader,wraplength=380,background=bground,fg='GREY',text='Conversie ZIP->XML',pady=20)
lbl_zip2xml.pack(expand=True)

btn_import_zip=tk.Button(fr_left,text='Selectare fisiere ZIP',font=font1,command=lambda:openzip(),width=38)
btn_import_zip.pack()

lbl_import_zip=tk.Label(fr_left,font=font2,wraplength=380,background=bground,fg='RED',text=open_file_zip)
lbl_import_zip.pack(expand=True)

btn_export_xml=tk.Button(fr_left,text='Selectare locatie fisiere XML',font=font1,command=lambda:writexml(),width=38)
btn_export_xml.pack()

if write_file_xml == 'Nu exista cale pentru salvare':
    color = 'RED'
else:
    color = 'BLACK'
lbl_export_xml=tk.Label(fr_left,font=font2,wraplength=380,background=bground,fg=color,text=write_file_xml)
lbl_export_xml.pack(expand=True)
lbl_export_xml.bind('<Button>',lbl_export_xml_command)

lbl_xml2pdf=tk.Label(fr_center,font=fontsubheader,wraplength=380,background=bground,fg='GREY',text='Conversie XML->PDF',pady=20)
lbl_xml2pdf.pack(expand=True)

btn_import_xml=tk.Button(fr_center,text='Selectare fisiere XML',font=font1,command=lambda:openxml(),width=38)
btn_import_xml.pack()

lbl_import_xml=tk.Label(fr_center,font=font2,wraplength=380,background=bground,fg='RED',text=open_file_xml)
lbl_import_xml.pack(expand=True)

btn_export_pdf=tk.Button(fr_center,text='Selectare locatie PDF',font=font1,command=lambda:writepdf(),width=38)
btn_export_pdf.pack()

if write_file_pdf == 'Nu exista cale pentru salvare':
    color = 'RED'
else:
    color = 'BLACK'
lbl_export_pdf=tk.Label(fr_center,font=font2,wraplength=380,background=bground,fg=color,text=write_file_pdf)
lbl_export_pdf.pack(expand=True)
lbl_export_pdf.bind('<Button>',lbl_export_pdf_command)

lbl_pdf=tk.Label(fr_right,font=fontsubheader,wraplength=380,background=bground,fg='GREY',text='Print PDF',pady=20)
lbl_pdf.pack(expand=True)

btn_import_pdf=tk.Button(fr_right,text='Selectare fisiere PDF',font=font1,command=lambda:openpdf(),width=38)
btn_import_pdf.pack()

lbl_import_pdf=tk.Label(fr_right,font=font2,wraplength=380,background=bground,fg='RED',text=open_file_pdf)
lbl_import_pdf.pack(expand=True)

btn_conversie_zip2xml=tk.Button(fr_left,text='Conversie ZIP->XML',font=font1,command=lambda:conversie_zip2xml(),width=38)
btn_conversie_zip2xml.pack()

lbl_conversie_zip2xml=tk.Label(fr_left,font=font2,wraplength=380,background=bground,text='Nu au fost efectuate conversii')
lbl_conversie_zip2xml.pack()

btn_conversie_xml2pdf=tk.Button(fr_center,text='Conversie XML->PDF',font=font1,command=lambda:conversie_xml2pdf(),width=38)
btn_conversie_xml2pdf.pack()

lbl_conversie_xml2pdf=tk.Label(fr_center,font=font2,wraplength=380,background=bground,text='Nu au fost efectuate conversii')
lbl_conversie_xml2pdf.pack()

btn_print=tk.Button(fr_right,text='Print PDF',font=font1,command=lambda:print(),width=38)
btn_print.pack()

lbl_print=tk.Label(fr_right,font=font2,wraplength=380,background=bground,text='Nu s-a printat nici un fisier')
lbl_print.pack()

lbl_extra=tk.Label(fr_right,font=font2,wraplength=380,background=bground,text='',pady=18)
lbl_extra.pack()

lbl_tot=tk.Label(fr_bottom,font=fontsubheader,wraplength=380,background=bground,fg='GREY',text='Toate operatiunile',pady=20)
lbl_tot.pack(expand=True)

btn_zip_xml_pdf=tk.Button(fr_bottom,text='Toate operatiunile',font=fontsubheader,command=lambda:zip_xml_pdf(),width=38)
btn_zip_xml_pdf.pack()

lbl_rezultate=tk.Label(fr_bottom,font=fontsubheader,wraplength=380,background=bground,fg='BLACK',text='Rezultate operatii',pady=10)
lbl_rezultate.pack(expand=True)

btnquit=tk.Button(fr_bottom,text='Iesire',font=font1,command=lambda:mainwindow.destroy(),width=18)
btnquit.pack()



mainwindow.mainloop()