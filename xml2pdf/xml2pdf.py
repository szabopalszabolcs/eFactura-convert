import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
from datetime import datetime as dt


url='https://webservicesp.anaf.ro/prod/FCTEL/rest/transformare/FACT1'
Headers={'Content-Type':'text/plain','Accept':'*/*'}
bground = 'lightgrey'
fontheader = ('Calibri',16)
font1 = ('Calibri',12)
font2 = ('Calibri',10)
open_file = 'Nu sunt fisiere selectate'
write_file = 'Nu exista cale pentru salvare'

mainwindow=tk.Tk()
mainwindow.configure(padx=20,background=bground)
mainwindow.title('Conversie XML PDF')

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
    try:
        denumire=xmltree.find('{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingSupplierParty/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party/{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity/{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}RegistrationName').text
    except:
        denumire=''

    pdf = str(denumire+' '+cui+' '+nrfact+'.pdf')

    for ch in notAllowed:
        pdf=pdf.replace(ch,'')

    pdf=write_file+'/'+pdf

    return pdf

def conversie():

    global open_file
    global write_file
    global Headers
    global url
    global lblrezultate
    global lblconversie
    error='Fisiere neprelucrate:'+'\n'

    if open_file == 'Nu sunt fisiere selectate':
        return
    if write_file == 'Nu exista cale pentru salvare':
        return

    lblrezultate.config(text='')
    lblrezultate.update()
    lblconversie.config(text='Conversie in curs',fg='RED')
    lblconversie.update()
    index = 0

    for xml in open_file:

        try:           
            
            xmltree=ET.parse(xml)
            root=xmltree.getroot()
            strBody=ET.tostring(root,encoding='utf-8')
            pdf=generateFileName(xmltree,write_file)

            try:
                result=requests.post(url,strBody,headers=Headers)
                if str(result.content).find('"nok"') == -1:
                    pdffile=open(pdf,'wb')
                    pdffile.write(result.content)
                    pdffile.close()
                    index+=1
                    lblconversie.config(text='Au fost convertite '+str(index)+' fisiere',fg='RED')
                    lblconversie.update()
                else:
                    lblrezultate.config(text='Nu s-a creat pdf pentru fisierul '+xml.split('/')[len(xml.split('/'))-1]+'\n'+lblrezultate.cget('text'))
                    error=error+xml.split('/')[len(xml.split('/'))-1]+'\n'
                    print(result.content)
            except:
                lblrezultate.config(text='Nu s-a creat pdf pentru fisierul '+xml.split('/')[len(xml.split('/'))-1]+'\n'+lblrezultate.cget('text'))
                error=error+xml.split('/')[len(xml.split('/'))-1]+'\n'
        except:
            lblrezultate.config(text='Nu s-a creat pdf pentru fisierul '+xml.split('/')[len(xml.split('/'))-1]+'\n'+lblrezultate.cget('text'))
            error=error+xml.split('/')[len(xml.split('/'))-1]+'\n'

    if index==len(open_file):
        lblrezultate.config(text='Au fost convertite '+str(index)+' fisiere',fg='BLACK')
    else:
        lblrezultate.config(text='Au fost convertite '+str(index)+' fisiere'+'\n'+lblrezultate.cget('text'),fg='RED')
        errorfile=open(write_file+'/Error '+str(dt.now().strftime("%Y-%m-%d %H-%M-%S"))+'.txt','w')
        errorfile.write(error)
    lblconversie.config(text='Conversie terminata',fg='BLACK')

def openfiles():
    global open_file
    global lblimport
    global lblrezultate
    open_file=filedialog.askopenfilenames(defaultextension='xml')
    lblimport.config(text=str(len(open_file))+' fisiere selectate',fg='BLACK')
    lblrezultate.config(text='')

def writefiles():
    global write_file
    global lblexport
    write_file=filedialog.askdirectory()
    lblexport.config(text=str(write_file),fg='BLACK')
    
lblheader=tk.Label(mainwindow,font=fontheader,wraplength=380,background=bground,fg='GREY',text='Conversie XML in PDF',pady=20)
lblheader.pack(expand=True)

btnimport=tk.Button(mainwindow,text='Selectare fisiere XML',font=font1,command=lambda:openfiles(),width=38)
btnimport.pack()

lblimport=tk.Label(mainwindow,font=font2,wraplength=380,background=bground,fg='RED',text=open_file)
lblimport.pack(expand=True)

btnexport=tk.Button(mainwindow,text='Selectare locatie PDF',font=font1,command=lambda:writefiles(),width=38)
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
