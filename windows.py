import tkinter as tk
from tkinter import messagebox
import backend_bank as backend


class Finestra(tk.Toplevel):
    """La classe Finestra possiede gli attributi e i metodi necessari per svolgere gran
    parte delle operazioni bancarie dell'app: Depositare,Ritirare,Prestiti e Trasferimenti
    di denaro sono questi le operazioni che si possono effettuare  """
    def __init__(self,master):
        #tk.Toplevel.__init__(self,master)
        self.master = master
        #self.master = tk.Toplevel()
        #self.master.geometry("425x250+140+140")
        #self.master.wm_title("")
        self.frame = tk.Frame(self.master,height=250,width=425)
        
#------------------------Labels
        self.label = tk.Label(self.frame,text="",bg="white",bd=10,font=("Verdana",13),fg="#363a47")
        self.cliente = tk.Label(self.frame,text="Cliente",font=("Verdana",15),fg="#363a47")
        self.somma = tk.Label(self.frame,text="Somma",font=("Verdana",15),fg="#363a47")
        self.somma_ritirare_lab = tk.Label(self.frame,text="Somma",font=("Verdana",15),fg="#363a47")
        self.data_prest = tk.Label(self.frame,text="Data",font=("Verdana",15),fg="#363a47")
        self.mittente = tk.Label(self.frame,text="Mittente",font=("Verdana",15),fg="#363a47")
        self.destinatario = tk.Label(self.frame,text="Destinatario",font=("Verdana",14),fg="#363a47")
        self.label_prestito = tk.Label(self.frame,text="Prestito residuo di Euro",font=("Verdana",11),fg="#363a47")
        self.prestito_residuo = tk.Label(self.frame,text="",font=("Verdana",11))
#-----------------------Variabili       
        self.cliente_text = tk.StringVar()
        self.somma_int = tk.IntVar()
        self.data_text = tk.StringVar()
        self.destinatario_text = tk.StringVar()
        self.somma_rit_int = tk.IntVar()
        self.somma_dep = tk.IntVar()
#-----------------------Bottoni
        self.prestito_but = tk.Button(self.frame,text="Prestito",font=("Verdana",12),bd=3,command=self.prestito)
        self.trasferisci_but = tk.Button(self.frame,text="Trasferisci",font=("Verdana",12),bd=3,command=self.trasferisci)
        self.ritira_but = tk.Button(self.frame,text="Ritira",command=self.ritira,font=("Verdana",12),bd=3)
        self.deposita_but = tk.Button(self.frame,text="Deposita",font=("Verdana",12),bd=3,command=self.deposita)
        self.aggiorna_but = tk.Button(self.frame,text="Aggiorna",font=("Verdana",12),bd=3,command=self.aggiorna)
        self.cerca_but = tk.Button(self.frame,text="Cerca",font=("Verdana",12),bd=3,command=self.cronologia_prestito)
# -------------------Entry
        self.cliente_entry = tk.Entry(self.frame,textvariable=self.cliente_text,bd=4,font=("Verdana",12))
        self.somma_entry = tk.Entry(self.frame,textvariable=self.somma_int,bd=4,font=("Verdana",12))
        self.data_entry = tk.Entry(self.frame,textvariable=self.data_text,bd=4,font=("Verdana",12))
        self.mittente_entry = tk.Entry(self.frame,textvariable=self.cliente_text,bd=4,font=("Verdana",12))
        self.destinatario_entry = tk.Entry(self.frame,textvariable=self.destinatario_text,bd=4,font=("Verdana",12))
        self.somma_rit_entry = tk.Entry(self.frame,textvariable=self.somma_rit_int,font=("Verdana",12),width=14)
        self.somma_deposito_entry = tk.Entry(self.frame,textvariable=self.somma_dep,font=("Verdana",12),width=14)
#------------------Listbox e ScrollBar
        self.box_list = tk.Listbox(self.frame)
        self.scroll_bar = tk.Scrollbar(self.box_list)
        self.box_list.configure(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.configure(command=self.box_list.yview)
        self.frame.pack()
#Posizionamento delle etichette,entries e bottoni per Trasferire i soldi da un conto all'altro   
    def lab_entry_trasferimento(self):
        self.master.title("Benvenuto nel servizio per il trasferimento monetario tra clienti")
        self.label.place(relx=0.098,rely=0.02)
        self.mittente.place(relx=0.1,rely=0.29)
        self.destinatario.place(relx=0.1,rely=0.495)
        self.somma.place(relx=0.1,rely=0.69)
        self.mittente_entry.place(relx=0.395,rely=0.305)
        self.destinatario_entry.place(relx=0.395,rely=0.505)
        self.somma_entry.place(relx=0.395,rely=0.705)
        self.trasferisci_but.place(relx=0.52,rely=0.83,relheight=0.12,relwidth=0.31)

#Posizionamento delle etichette,entries e bottoni per ritirare e depositare
    def lab_entry_ritira_dep(self):
        self.master.title("Benvenuto nel servizio Ritira e Deposita")
        self.label.place(relx=0.098,rely=0.02)
        self.cliente.place(relx=0.129,rely=0.31)
        self.cliente_entry.place(relx=0.38,rely=0.32,relwidth=0.35)
        self.somma_ritirare_lab.place(relx=0.129,rely=0.45)
        self.somma_rit_entry.place(relx=0.38,rely=0.47,relwidth=0.35)
        self.ritira_but.place(relx=0.77,rely=0.49,relheight=0.1)
        self.somma.place(relx=0.129,rely=0.62) 
        self.somma_deposito_entry.place(relx=0.38,rely=0.63,relwidth=0.35)
        self.deposita_but.place(relx=0.77,rely=0.625,relheight=0.1)   

#Posizionamento delle etichette,entries e bottoni per il prestito
    def lab_entry_prestito(self):
        """ Funzione per piazzare le etichette e le entry comuni per molte operazioni
        all'interno del programma come ad esempio eseguguire un prestito o aggiornare 
        un prestito esistente """
        self.master.title("Benvenuto nel servizio Prestiti")
        self.label.config(text="Prestito Senza Interessi")
        self.label.place(relx=0.098,rely=0.02)
        self.cliente.place(relx=0.1,rely=0.29)
        self.somma.place(relx=0.1,rely=0.495)
        self.cliente_entry.place(relx=0.395,rely=0.305)
        self.somma_entry.place(relx=0.395,rely=0.505)
        self.data_prest.place(relx=0.1,rely=0.69)
        self.data_entry.place(relx=0.395,rely=0.685)

    def cronologia_info(self):
        self.master.title("Sezione Cronologica")
        self.label.config(font=("Verdana",15))
        self.label.place(relx=0.098,rely=0.02)
        self.cliente.place(relx=0.1,rely=0.26)
        self.cliente_entry.place(relx=0.34,rely=0.27,relwidth=0.38)
        self.box_list.place(relwidth=0.965,relheight=0.5,relx=0.01,rely=0.45)
        self.scroll_bar.pack(side="right",fill="y")
        self.cerca_but.place(relx=0.76,rely=0.27,relheight=0.1)
        
#---------------------------Funzioni
    def ritira(self):
        """ <<Funzione per ritirare denaro>>"""
        backend.database.ritira(self.cliente_entry.get(),int(self.somma_rit_entry.get()))
        messagebox.showinfo("Ritira","Ritiro Effettuato con Successo")
       
    def deposita(self):
        """Funzione per depositare denaro """
        backend.database.deposita(int(self.somma_deposito_entry.get()),self.cliente_entry.get())
        messagebox.showinfo("Deposito","Deposito Effettuato con Successo")

    def trasferisci(self):
        """><Funzione per il trasferimento del denaro da Cliente a Cliente>> """
        backend.database.trasferisci_denaro(self.mittente_entry.get(),
                    self.destinatario_entry.get(),int(self.somma_entry.get()))
        messagebox.showinfo("Transazione","Transazione eseguita con successo!!")
    
    def prestito(self):
        """<<Funzione che effettua il prestito inserendo i dati nella tabella prestiti
         prendendo come parametri il cliente ,la somma e la data>> """
        backend.database.crea_prestito(self.cliente_entry.get(),
                    int(self.somma_entry.get()),self.data_entry.get())
        messagebox.showinfo("Prestito", """Operazione effettuata con successo.""")

    def aggiorna(self):
        """<<Funzione che aggiorna il prestito del cliente,nel caso in cui la 
        somma restituita estingua il debito la funzione aggiorna  lo stato di attivazione e
         la data del saldo effettuato>>"""
        backend.database.aggiorna_prestito(self.cliente_entry.get(),
        int(self.somma_entry.get()),self.data_entry.get())
        messagebox.showinfo("Aggiornamento Prestito","""Operazione effettuata con successo.
        Controllare lo stato del prestito presso la Cronologia""")
        
        self.prestito_residuo.config(text=backend.database.prestito_in_corso(self.cliente_entry.get()))
        #

    def cronologia_prestito(self):
        """Funzione necessaria per tenere traccia dei prestiti che un dato cliente ha ricevuto
        ed estinto.Per maggiori informazioni leggere direttamente la mini-documentazione per la funzione
        cronologia."""
        backend.database.cronologia()
        self.box_list.delete(0,tk.END)
        for row in backend.database.mostra_prestiti_cliente(self.cliente_entry.get()):
            self.box_list.insert(tk.END,row)