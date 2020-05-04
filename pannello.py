import tkinter as tk
from tkinter.ttk import Combobox
import windows
import backend_bank as backend
from tkinter import messagebox
import datetime


class Pannello:
    """ La classe Pannello è la classe genitore dell'app contiene
    il template principale i bottoni sul menu a sinistra,la barra di ricerca e
    lo spazio centrale da utilizzare per registrare un nuovo cliente,modificare 
    un vecchio cliente e visionare le informazioni dei clienti registrati,contiene
    le funzioni necessarie per svolgere i compiti sopracitati. """
    def __init__(self,root):
        self.root = root
        self.root.resizable(False, False) 
        self.root.wm_title("Benvenuto nel pannello Amministrativo")
        self.frame = tk.Frame(self.root,width=700,height=625)
 #------------Immagini qui
        self.sfondo = tk.PhotoImage(file="img\sfondodue.png")
        self.staff = tk.PhotoImage(file="img\staff.png")
        self.registra = tk.PhotoImage(file="img\\registra.png")
        self.ritira = tk.PhotoImage(file="img\\ritira.png")
        self.cronologia = tk.PhotoImage(file="img\cronologia.png")
        self.trasferisci = tk.PhotoImage(file="img\\trasferisci.png")
        self.prestito = tk.PhotoImage(file="img\prestito.png")
        self.aggiorna = tk.PhotoImage(file="img\\aggiorna.png")
        self.account_elimina = tk.PhotoImage(file="img\elimina.png")
        self.sfondo_lab = tk.Label(self.frame,image=self.sfondo)
        self.sfondo_lab.place(relx=0,rely=0,relheight=1,relwidth=1)
        self.box_sinistra = tk.Frame(self.frame,bg="#292c35")
        self.box_sinistra.place(relx=0,rely=0.11,relwidth=0.336,relheight=0.9)
        self.frame_bottone_registra = tk.Frame(self.frame,bg="#c4c5c8")
        self.frame_bottone_registra.place(relx=0.65,rely=0.252,relwidth=0.286,relheight=0.046) 
        self.indice = 0  
       
#------------Bottoni   
        self.amministrazione_btn = tk.Button(self.box_sinistra,bg="#363a47",
                image=self.staff,bd=3,height=0.02,width=0.220)
        self.amministrazione_btn.grid(row=0,column=0)
        self.register_customer_btn = tk.Button(self.box_sinistra,bg="#363a47",
                image=self.registra,bd=3,command=self.registra_cliente_view
                ,height=0.02,width=0.220)
        self.register_customer_btn.grid(row=1,column=0)
        self.ritira_btn = tk.Button(self.box_sinistra,bg="#363a47",image=self.ritira,
                bd=3,command=self.ritira_deposita_view,height=0.02,width=0.220)
        self.ritira_btn.grid(row=2,column=0)
        self.cronologia_btn = tk.Button(self.box_sinistra,bg="#363a47",image=self.cronologia,
                bd=3,command=self.cronologia_view,height=0.02,width=0.220)
        self.cronologia_btn.grid(row=3,column=0)
        self.trasferisci_btn = tk.Button(self.box_sinistra,bg="#363a47",image=self.trasferisci,
                bd=3,command=self.trasferimento_soldi_view,height=0.02,width=0.220)
        self.trasferisci_btn.grid(row=4,column=0)
        self.prestito_btn = tk.Button(self.box_sinistra,bg="#363a47",image=self.prestito,
                command=self.prestito_finestra_view,height=0.02,width=0.220)
        self.prestito_btn.grid(row=5,column=0)
        self.aggiorna_btn = tk.Button(self.box_sinistra,bg="#363a47",image=self.aggiorna,
                command=self.aggiorna_prestito_view,height=0.02,width=0.220)
        self.aggiorna_btn.grid(row=6,column=0)
        self.account_del_btn = tk.Button(self.box_sinistra,bg="#363a47",image=self.account_elimina,
                command=self.elimina_account_view,height=0.02,width=0.220)
        self.account_del_btn.grid(row=7,column=0)
#-------------------Box Dati 
        self.box_dati = tk.Frame(self.root,bg="white")
        self.box_dati.place(relx=0.354,rely=0.299,relwidth=0.625,relheight=0.66)          
#-------------------------Ricerca
        search_type = ["Nome e Cognome","Numero Account"]
        self.combo = Combobox(self.root,values=search_type,width=14,height=25,font=("Verdana",12))
        self.combo.set("Seleziona")
        self.combo.place(relx=0.430,rely=0.159)
        self.combo.bind("<<ComboboxSelected>>",self.tipo_selezionato)
        self.ricerca_text = tk.StringVar()
        self.ricerca_entry = tk.Entry(self.root,textvariable=self.ricerca_text,font=("Verdana",12))
        self.ricerca_entry.place(relx=0.678,rely=0.160,height=22,width=130)
        self.cerca_but = tk.Button(self.root,text="Cerca",font=("Verdana",12),command=self.ricerca)
        self.cerca_but.place(relx=0.88,rely=0.1598,height=25)
        self.frame.pack()
#----------------Labels e Entry per l'inserimento dei dati del cliente 
#--------------variabili
    def labels_entry(self):
        self.name_text = tk.StringVar()
        self.sesso_text = tk.StringVar()
        self.data_nascita_text = tk.StringVar()
        self.cellulare_int = tk.StringVar()
        self.tipo_account_text = tk.StringVar()
        self.occupazione_text = tk.StringVar()
        self.azienda_text = tk.StringVar()
        self.numero_account_int = tk.IntVar()
        self.indirizzo_text = tk.StringVar()
        self.data_creazione_text = tk.StringVar()
        self.saldo_text = tk.IntVar()
#----------------------------------Entry e labels
        self.name = tk.Label(self.box_dati,text="Nome",font=("Verdana",11),bg="white")
        self.name_entry = tk.Entry(self.box_dati,textvariable=self.name_text,bd=3,font=("Verdana",11),width=14)
        self.sesso = tk.Label(self.box_dati,text="Sesso",font=("Verdana",11),bg="white")
        self.sesso_entry = tk.Entry(self.box_dati,textvariable=self.sesso_text,bd=3,font=("Verdana",11),width=14)
        self.data_nascita = tk.Label(self.box_dati,text="Data di nascita",font=("Verdana",11),bg="white")
        self.data_nascita_entry = tk.Entry(self.box_dati,textvariable=self.data_nascita_text,bd=3,font=("Verdana",11),width=14)
        self.cellulare = tk.Label(self.box_dati,text="Cellulare",font=("Verdana",11),bg="white")
        self.cellulare_entry = tk.Entry(self.box_dati,textvariable=self.cellulare_int,bd=3,font=("Verdana",11),width=14)
        self.tipo_account = tk.Label(self.box_dati,text="Tipo account",font=("Verdana",11),bg="white")
        self.tipo_account_entry = tk.Entry(self.box_dati,textvariable=self.tipo_account_text,bd=3,font=("Verdana",11),width=14)
        self.occupazione = tk.Label(self.box_dati,text="Occupazione",font=("Verdana",11),bg="white")
        self.occupazione_entry = tk.Entry(self.box_dati,textvariable=self.occupazione_text,bd=3,font=("Verdana",11),width=14)
        self.azienda = tk.Label(self.box_dati,text="Azienda",font=("Verdana",11),bg="white")
        self.azienda_entry = tk.Entry(self.box_dati,textvariable=self.azienda_text,bd=3,font=("Verdana",11),width=14)
        self.numero_account = tk.Label(self.box_dati,text="Numero account",font=("Verdana",11),bg="white")
        self.numero_account_entry = tk.Entry(self.box_dati,textvariable=self.numero_account_int,bd=3,font=("Verdana",11),width=14)
        self.indirizzo = tk.Label(self.box_dati,text="Indirizzo",font=("Verdana",11),bg="white")
        self.indirizzo_entry = tk.Entry(self.box_dati,textvariable=self.indirizzo_text,bd=3,font=("Verdana",11),width=14)
        self.data_creazione = tk.Label(self.box_dati,text="Data creazione",font=("Verdana",11),bg="white")
        self.data_creazione_entry = tk.Entry(self.box_dati,textvariable=self.data_creazione_text,bd=3,font=("Verdana",11),width=14)
        self.saldo_corrente = tk.Label(self.box_dati,text="Saldo Corrente",font=("Verdana",11),bg="White")
        self.saldo_corrente_entry = tk.Entry(self.box_dati,textvariable=self.saldo_text,bd=3,font=("Verdana",11),width=14)
#------------------------------------------
    def dati_utente_lab(self):
        """Mostra i dati dell'utente cercato """
        self.name_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=28)
        self.sesso_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=3)
        self.data_nascita_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=28)
        self.cellulare_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=28)
        self.tipo_account_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=28)
        self.occupazione_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=28)
        self.azienda_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=28)
        self.numero_account_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=28)
        self.indirizzo_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=28)
        self.data_creazione_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=28)
        self.saldo_corrente_lab = tk.Label(self.box_dati,text="",font=("Verdana",11),bd=3,width=28)       
#il metodo current mi restituisce l'indice dell'oggetto selezionato nel combobox
 #l'indice l'ho inizializzato direttamente dalla classe a valore 0   

#---------------------------Pulire il Frame
    def pulisci_frame(self):
        """Funzione per pulire il Frame box dati ogni volta
         che viene premuto un bottone diverso dal menu di sinistra utilizzando il bottone
         torna indietro presente sopra il box_dati principale"""
        bottone = tk.Button(self.root,bg="#3ba526",font=("Verdana",13),text="Torna Indietro",
            fg="white",command=self.pulisci_frame)
        bottone.place(relx=0.375,rely=0.253,height=26,width=152)
        for widget in self.box_dati.winfo_children():
            widget.destroy()
    #Per Eliminare il bottone registra utilizzando il metodo pulisci_frame
        for widget in self.frame_bottone_registra.winfo_children():
            widget.destroy()

#--------------------Posizionamento dati cliente  
    def mostra_dati(self,row):  
        """Mostra le labels contenenti le informazioni personali di 
        un cliente nome,età saldo disponibile ecc."""
        self.name_lab["text"] = row[0]
        self.sesso_lab["text"] = row[1]
        self.data_nascita_lab["text"] = row[2]
        self.cellulare_lab["text"] = row[3]
        self.tipo_account_lab["text"] = row[4]
        self.occupazione_lab["text"] = row[5]
        self.azienda_lab["text"] = row[6]
        self.numero_account_lab["text"] = row[7]
        self.indirizzo_lab["text"] = row[8]
        self.data_creazione_lab["text"] = row[9]
        self.saldo_corrente_lab["text"] = row[10]

    def posiziona_etichettesx(self):
        self.labels_entry()
        """Posiziona le labels contenenti i campi predefiniti: nome,sesso,età,
        azienda ecc. ecc..da utilizzare quando vengono  richiamate le funzioni
        per ottenere o aggiornare le informazioni su un cliente o registrarne uno nuovo.  """
        self.name.grid(row=0,column=0,padx=10,pady=5)
        self.sesso.grid(row=1,column=0,padx=10,pady=5)
        self.data_nascita.grid(row=2,column=0,padx=10,pady=5)
        self.cellulare.grid(row=3,column=0,padx=10,pady=5)
        self.tipo_account.grid(row=4,column=0,padx=10,pady=5)
        self.occupazione.grid(row=5,column=0,padx=10,pady=5)
        self.azienda.grid(row=6,column=0,padx=10,pady=5)
        self.numero_account.grid(row=7,column=0,padx=10,pady=5)
        self.indirizzo.grid(row=8,column=0,padx=10,pady=5)
        self.data_creazione.grid(row=9,column=0,padx=10,pady=5)
        self.saldo_corrente.grid(row=10,column=0,padx=10,pady=5)

    def posizionadatidx(self):
        """Posiziona le labels contenenti i campi nome,sesso,età,azienda ecc.
         ecc..relative all cliente selezionato"""
        self.dati_utente_lab()
        self.name_lab.grid(row=0,column=1,padx=10,pady=5,columnspan=2)
        self.sesso_lab.grid(row=1,column=1,padx=10,pady=5)
        self.data_nascita_lab.grid(row=2,column=1,padx=10,pady=5,columnspan=2)
        self.cellulare_lab.grid(row=3,column=1,padx=10,pady=5,columnspan=2)
        self.tipo_account_lab.grid(row=4,column=1,padx=10,pady=5)
        self.occupazione_lab.grid(row=5,column=1,padx=10,pady=5)
        self.azienda_lab.grid(row=6,column=1,padx=10,pady=5,columnspan=2)
        self.numero_account_lab.grid(row=7,column=1,padx=10,pady=5,columnspan=2)
        self.indirizzo_lab.grid(row=8,column=1,padx=10,pady=5,columnspan=2)
        self.data_creazione_lab.grid(row=9,column=1,padx=10,pady=5)
        self.saldo_corrente_lab.grid(row=10,column=1,padx=10,pady=5)
#----------------Seleziona e Ricerca           
    def tipo_selezionato(self,event):
        """ Funzione per la barra di ricerca restituisce un indice corrispondente 
        all'opzione di ricerca selezionata. Esempio: all'opzione Nome e Cognome corrisponde 
        indice 0 """
        self.indice = self.combo.current()

    def seleziona(self):
        """Seleziona il cliente e ritorna il nome cliente salvando nella variabile self.cliente """
        try:
            if self.indice == 0:
                self.cliente = backend.database.cerca_nome(self.ricerca_entry.get())
                self.mostra_dati(self.cliente)
            else:
                self.cliente = backend.database.cerca_numero_account(self.ricerca_entry.get())
                self.mostra_dati(self.cliente)
        except:
            pass
        return self.cliente
        
    def ricerca(self):
        """Funzione di ricerca richiama le funzioni Posiziona_labelsSx e 
        Posiziona_labelsSx  per mostrare le labels e i dati relativi all'utente
         cercato utilizzando la funzione mostra_dati"""
        self.pulisci_frame()
        self.posiziona_etichettesx() 
        self.posizionadatidx()
        self.seleziona()
        self.bottone_aggiorna = tk.Button(self.frame_bottone_registra,bg="#0d7ee8",font=("Verdana",13),
                text="Aggiorna Dati",fg="white",command=self.mod_cliente_view)
        self.bottone_aggiorna.place(relx=0.247,rely=0,height=26,width=152)
         
#-----------------Metodi Registrazione,Aggiornamento dati Cliente
    def campi_da_riempire(self):
        """ Rappresentano i campi da riempire per registrare un nuovo cliente o per
        aggiornare un cliente già esistente"""
        self.name_entry.grid(row=0,column=1,padx=25,pady=5,columnspan=2)
        self.sesso_entry.grid(row=1,column=1,padx=25,pady=5,columnspan=2)
        self.data_nascita_entry.grid(row=2,column=1,padx=25,pady=5,columnspan=2)
        self.cellulare_entry.grid(row=3,column=1,padx=25,pady=5,columnspan=2)
        self.tipo_account_entry.grid(row=4,column=1,padx=25,pady=5)
        self.occupazione_entry.grid(row=5,column=1,padx=25,pady=5)
        self.azienda_entry.grid(row=6,column=1,padx=25,pady=5,columnspan=2)
        self.numero_account_entry.grid(row=7,column=1,padx=25,pady=5,columnspan=2)
        self.indirizzo_entry.grid(row=8,column=1,padx=25,pady=5,columnspan=2)
        self.data_creazione_entry.grid(row=9,column=1,padx=25,pady=5)
        self.saldo_corrente_entry.grid(row=10,column=1,padx=25,pady=5)

    def registra_cliente_view(self):
        """metodo view al bottone registra nel menu a sinistra 
        che richiama le funzioni necessarie per registrare un cliente"""
        self.pulisci_frame()
        self.bottone_registra = tk.Button(self.frame_bottone_registra,bg="#0d7ee8",
                font=("Verdana",13),text="Registra Cliente",fg="white",command=self.aggiungi_cliente)
        self.bottone_registra.place(relx=0.247,rely=0,height=26,width=152)
        """Inserisco le etichette e i campi da compilare per registrare un nuovo cliente"""
        self.posiziona_etichettesx() 
        self.campi_da_riempire() 
              
    def aggiungi_cliente(self):
        """Aggiunge il cliente nel database """
        backend.database.aggiungi_cliente(self.name_entry.get(),
        self.sesso_entry.get(),self.data_nascita_entry.get(),self.cellulare_entry.get()
        ,self.tipo_account_entry.get(),self.occupazione_entry.get(),self.azienda_entry.get(),
        self.numero_account_entry.get(),self.indirizzo_entry.get(),self.data_creazione_entry.get(),
        self.saldo_corrente_entry.get())
        messagebox.showinfo("Operazione eseguita con successo","Nuovo cliente registrato.")
    #Richiamo la funzione aggiungi cliente dal backend.py che inserisce nel database
    # i dati del cliente inserite dall'operatore bancario    
    
    def mod_cliente_view(self):
        """Metodo riferito al bottone Amministrazione  richiama le funzioni di posizionamento 
        per le etichette e i campi in cui inserire i dati aggiornati,il metodo modifica_cliente
        serve a modificare  i dati personali del cliente già presente nel database"""
        self.pulisci_frame()
        self.posiziona_etichettesx()
        self.campi_da_riempire() 
        item = self.seleziona()
        self.name_entry.insert(0,item[0])
        self.sesso_entry.insert(0,item[1])
        self.data_nascita_entry.insert(0,item[2])
        self.cellulare_entry.insert(0,item[3])
        self.tipo_account_entry.insert(0,item[4])
        self.occupazione_entry.insert(0,item[5])
        self.azienda_entry.insert(0,item[6])
        self.numero_account_entry.insert(0,item[7])
        self.indirizzo_entry.insert(0,item[8])
        self.data_creazione_entry.insert(0,item[9])
        self.saldo_corrente_entry.insert(0,"LOCKED ")
        self.modifica_but = tk.Button(self.frame_bottone_registra,bg="#0d7ee8",
                font=("Verdana",13),text="Aggiorna",fg="white",command=self.modifica_cliente)
        self.modifica_but.place(relx=0.22,rely=0,height=26,width=152) 
        
    def modifica_cliente(self):
        """metodo per modificare i dati di un cliente già registrato nel database"""
        self.seleziona()
        backend.database.aggiorna_cliente(self.name_entry.get(),
        self.sesso_entry.get(),self.data_nascita_entry.get(),self.cellulare_entry.get()
        ,self.tipo_account_entry.get(),self.occupazione_entry.get(),self.azienda_entry.get(),
        self.numero_account_entry.get(),self.indirizzo_entry.get(),self.data_creazione_entry.get())
        messagebox.showinfo("Operazione eseguita con successo","Dati cliente Aggiornati")

    def elimina_account_view(self):
        self.pulisci_frame()
        self.label_elimina = tk.Label(self.box_dati,
            text="""Inserisci il nome completo del cliente
        da eliminare dal database""",bg="white",font=("Verdana",15),
            fg="black").place(relx=0.01,rely=0.02)
        self.elimina_text = tk.StringVar()
        self.cliente_lab = tk.Label(self.box_dati,text="Nome Completo",bg="white",
            fg="#2C3335",font=("Verdana",14))
        self.cliente_lab.place(relx=0.07,rely=0.29)
        self.elimina_entry = tk.Entry(self.box_dati,bd=5,textvariable=self.elimina_text,
            font=("Verdana",13),width=14)
        self.elimina_entry.place(relx=0.47,rely=0.29)
        self.eliminazione_but = tk.Button(self.box_dati,text="Conferma Eliminazione",bg="#EA7DFF",
            font=("Verdana",12),bd=3,command=self.elimina_cliente)
        self.eliminazione_but.place(relx=0.35,rely=0.44)
    
    def elimina_cliente(self):
        backend.database.elimina_cliente(self.elimina_entry.get())
        messagebox.showinfo("Operazione eseguita","Cliente eliminato dal database!")
        self.elimina_entry.delete(0,tk.END)

#---------------------------Servizio Ritira e Deposita       
    def ritira_deposita_view(self):
        """Finestra che utilizza la classe Finestra,per il deposito e il ritiro
         dei soldi utilizzando le funzioni ritira e deposita """
        """Finestra Top Level  definita per ritirare o depositare i soldi in un account """
        self.finestra = tk.Toplevel()
        app = windows.Finestra(self.finestra)
        app.lab_entry_ritira_dep()
        app.label.config(text="Servizio Ritira e Deposita")
        
#-----------------------Servizio Trasferimento dei Soldi da Cliente a Cliente
    def trasferimento_soldi_view(self):
        """ Posiziono le etichette,i campi e i bottoni necessari dalla classe finestra..
        Finestra per l'inserimento dei dati necessari a completare la transazione monetaria da un cliente
        all'altro utilizzando la funzione Trasferisci """
        self.finestra = tk.Toplevel()
        app= windows.Finestra(self.finestra)
        app.lab_entry_trasferimento()
        app.label.config(text="Trasferimento Soldi")
          
#--------------------------Servizio Prestiti   
    def prestito_finestra_view(self):
        """Apre una finestra Top Level in cui effettuare il prestito """
        self.finestra = tk.Toplevel() 
        app = windows.Finestra(self.finestra)
        app.lab_entry_prestito()
        app.prestito_but.place(relx=0.62,rely=0.83,relheight=0.12,relwidth=0.31)
        app.label.config(text="Prestito senza Interessi")
        
    def aggiorna_prestito_view(self):
        """Apre una finestra Top Level per aggiornare il prestito """
        self.finestra = tk.Toplevel()
        app = windows.Finestra(self.finestra)
        app.lab_entry_prestito()
        self.prestito_label = tk.Label(self.finestra,text="Somma da restituire")
        app.aggiorna_but.place(relx=0.69,rely=0.83,relheight=0.12,relwidth=0.28)
        app.label_prestito.place(relx=0,rely=0.86)
        app.prestito_residuo.place(relx=0.44,rely=0.86)
        app.label.config(text="Aggiorna lo stato del Prestito")

    def cronologia_view(self):
        self.finestra = tk.Toplevel()
        app = windows.Finestra(self.finestra)
        app.cronologia_info()
        app.label.config(text="Cronologia Prestiti")
        
        
        
        


         

