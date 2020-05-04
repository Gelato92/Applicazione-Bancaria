import psycopg2
from psycopg2 import sql
import psycopg2.extras
import datetime
import time

db = "dbname='Banca' user='postgres' password='password' host='localhost' port='5432'"

class Database():
    def __init__(self,db):
        self.connessione = psycopg2.connect(db)
        self.cursore = self.connessione.cursor()
        self.cursore.execute("""CREATE TABLE IF NOT EXISTS clienti(Nome_completo TEXT NOT NULL,
        sesso CHAR(1) NOT NULL,data_di_nascita TIMESTAMP NOT NULL,cellulare VARCHAR(10) NOT NULL,
        tipo_account TEXT NOT NULL, occupazione TEXT NOT NULL,azienda TEXT NOT NULL,
        numero_account INT PRIMARY KEY ,indirizzo TEXT NOT NULL,
        data_creazione_account TIMESTAMP NOT NULL,saldo_corrente INTEGER NOT NULL)""")
        self.connessione.commit()
#-------------Staff
    def aggiungi_staff(self,username,password,email):
        query = sql.SQL("INSERT INTO {tabella} VALUES(%s,%s,%s)").format(
            sql.Identifier("clienti"))
        colonne = (username,password,email)
        self.cursore.execute(query,colonne)
        self.connessione.commit()

#devo utilizzare la classe sql del modulo psycopg2 per poter creare query dinamiche 
#e passare o la tabella oppure le colonne in modo da evitare di esporre i nomi delle colonne
    def visualizza_staff(self):
        self.cursore.execute(sql.SQL("SELECT * FROM {tabella}").format(
            tabella=sql.Identifier("staff"))) 
        rows = self.cursore.fetchall()
        return rows
        
# def mod_col(self,tipo,tipo1):
##self.cursore.execute(sql.SQL("ALTER TABLE {tabella} ALTER COLUMN {colonna} TYPE %s USING {colonna1}::%s").format(
# tabella=sql.Identifier("clienti"),colonna=sql.Identifier("data_creazione_account"),
# colonna1=sql.Identifier("data_creazione_account")),(tipo,tipo1))
# self.connessione.commit()

#--------------Clienti : Aggiungi ,Aggiorna,Elimina
    def visualizza_clienti(self):
        self.cursore.execute(sql.SQL("SELECT * FROM {tabella}").format(
            tabella=sql.Identifier("clienti")))
        rows = self.cursore.fetchall()
        return rows
    
    def elimina_cliente(self,nome_completo):  
        self.cursore.execute(sql.SQL("DELETE FROM {tab} WHERE {nome_completo}= %s").format(
            tab=sql.Identifier("clienti"),nome_completo=sql.Identifier("nome_completo")),
            (nome_completo,))
        self.connessione.commit()
   
    def aggiungi_cliente(self,Nome_completo,sesso,data_di_nascita,cellulare,tipo_account,occupazione,azienda,numero_account,indirizzo,data_creazione_account,saldo_corrente):
        query = sql.SQL("INSERT INTO {tabella} VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(tabella=sql.Identifier("clienti"))
        colonne = (Nome_completo,sesso,data_di_nascita,cellulare,tipo_account,occupazione,azienda,numero_account,indirizzo,data_creazione_account,saldo_corrente)
        self.cursore.execute(query,colonne)
        self.connessione.commit()
    
    def aggiorna_cliente(self,Nome_completo,sesso,data_di_nascita,cellulare,tipo_account,occupazione,azienda,numero_account,indirizzo,data_creazione_account):
        query = sql.SQL("""UPDATE {tabella} SET {colonna1}=%s,{colonna2}=%s,{colonna3}=%s,{colonna4}=%s,
              {colonna5}=%s,{colonna6}=%s,{colonna7}=%s,{colonna8}=%s,{colonna9}=%s,
              {colonna10}=%s WHERE {colonna1}=%s""").format(tabella=sql.Identifier("clienti"),
              colonna1=sql.Identifier("nome_completo"),colonna2=sql.Identifier("sesso"),
              colonna3=sql.Identifier("data_di_nascita"),colonna4=sql.Identifier("cellulare"),
              colonna5=sql.Identifier("tipo_account"),colonna6=sql.Identifier("occupazione"),
              colonna7=sql.Identifier("azienda"),colonna8=sql.Identifier("numero_account"),
              colonna9=sql.Identifier("indirizzo"),colonna10=sql.Identifier("data_creazione_account"),
              )
        colonne = (Nome_completo,sesso,data_di_nascita,cellulare,tipo_account,occupazione,azienda,numero_account,indirizzo,data_creazione_account,Nome_completo)
        self.cursore.execute(query,colonne)
        
#---------------funzione ricerca per nome e numero account 
    def cerca_nome(self,nome_completo): 
            self.cursore.execute(sql.SQL("SELECT * FROM {tabella} WHERE {colonna}=%s").format(
                tabella=sql.Identifier("clienti"),colonna=sql.Identifier("nome_completo")),(nome_completo,))
            rows = self.cursore.fetchone()
            return rows
            
    def cerca_numero_account(self,numero_account):
            self.cursore.execute(sql.SQL("SELECT * FROM {tabella} WHERE {colonna}=%s").format(
            tabella=sql.Identifier("clienti"),colonna=sql.Identifier("numero_account")),(numero_account,))
            rows = self.cursore.fetchone()
            return rows

#---------------------Saldo e opzioni di deposito e ritiro       
    def saldo_corrente(self,nome_completo):
        """Funzione che ritorna il saldo dell'utente selezionato  """
        self.cursore.execute(sql.SQL("SELECT {colonna} FROM {tabella} WHERE {colonna2}=%s").format(
        colonna=sql.Identifier("saldo_corrente"),tabella=sql.Identifier("clienti"),
        colonna2=sql.Identifier("nome_completo")),(nome_completo,))
        row =  self.cursore.fetchone()[0]
        return row

    def ritira(self,nome_completo,importo):
        """ Funzione per ritirare i soldi dal conto"""
        saldo = self.saldo_corrente(nome_completo)
        if saldo > importo:
            query = sql.SQL("UPDATE {tabella} SET {colonna} =%s WHERE {colonna2}=%s").format(
            tabella=sql.Identifier("clienti")
            ,colonna=sql.Identifier("saldo_corrente"),colonna2=sql.Identifier("nome_completo"))
            dati = (saldo - importo,nome_completo)
            self.cursore.execute(query,dati)
            self.connessione.commit()
            print("Ritiro effettuato")
        else:
            pass
        
    def deposita(self,importo,nome_completo):
        """ Funzione per depositare i soldi nel conto"""
        saldo = self.saldo_corrente(nome_completo)
        self.cursore.execute(sql.SQL("UPDATE {tabella} SET {colonna1}=%s WHERE {colonna2}=%s").format(
            tabella=sql.Identifier("clienti"),
        colonna1=sql.Identifier("saldo_corrente"),colonna2=sql.Identifier("nome_completo")),
            (saldo + importo,nome_completo))
        self.connessione.commit()
        print("Soldi Depositati con successo!")

    def aggiungi_in_massa(self):
        """ Per inserire in modo molto piu performante piu rows contemporaneamente
        utilizzeremo la funzione execute_batch del modulo extras di psycopg2
        >> Esempio:
        sql = 'INSERT INTO my_table (account_id, name) VALUES (%s,%s)'
        args = [(id, ' Pizza'),(id2,'Gelato')]
        psycopg2.extras.execute_batch(cursore, sql, args)
        cur.query()
        Equivale alla query ..... in SQL....
        "INSERT INTO my_table (account_id, name) VALUES (1, 'Yuval Pizza'),(2, 'Sunset Hair Saloon')
        """
        cur = self.connessione.cursor()
        clienti = [('Super Mario', 'M', '22-03-1943', "3333445892", 'giochino', 'Pizzaiolo', 'Nessuna', 13, 'Tokyo 11', '07-04-2020', 1000),
        ('Johnzy', 'M', '13-09-2000', "3365465789", 'Flessibile', 'Studente', 'Nessuna', 12, 'Cagliari 21', '29-03-2020', 1500),
         ('Pinocchio', 'F', '25-06-1961', "3332342789", 'Flessibile', 'Pensionata', 'Nessuna', 14, 'Ischia 21', '29-03-2020', 4000),
         ('Zazà', 'M', '23-09-1958', "3312342789", 'Flessibile', 'Msemmen e Madeleine', 'Nessuna', 5, 'Milano 21', '29-03-2020', 4000),
          ('Pecorino', 'M', '20-11-1992', "3483025200", 'Flessibile', 'Disoccupato', 'Nessuna', 6, 'Roma 21', '28-03-2020',1100)]
        query = """INSERT INTO clienti(nome_completo,sesso,data_di_nascita,cellulare,tipo_account,
             occupazione,azienda,numero_account,indirizzo,data_creazione_account,saldo_corrente) 
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        psycopg2.extras.execute_batch(cur,query,clienti)

 #--------------------------Prestito    
    def crea_prestito(self,nome_completo,cifra,data_prestito): 
        inizio = time.perf_counter()
        self.cursore.execute(sql.SQL("""BEGIN;INSERT INTO {tabella}({colonna1},{colonna2})
         SELECT {colonna3},{colonna4} FROM {tabella2} WHERE {colonna5}=%s;
         UPDATE {tabella} SET {colonna}=%s, {colonnatemp}=%s,{colonnastato}=%s,{colonnanuova}=%s 
         WHERE {colonnanome}=%s;COMMIT;""").format(
        tabella=sql.Identifier("prestiti"),colonna1=sql.Identifier("cliente"),
        colonna2=sql.Identifier("id_cliente"),colonna3=sql.Identifier("nome_completo"),
        colonna4=sql.Identifier("numero_account"),tabella2=sql.Identifier("clienti"),
        colonna5=sql.Identifier("nome_completo"),colonna=sql.Identifier("denaro_in_prestito")
        ,colonnatemp=sql.Identifier("data_prestito"),colonnastato=sql.Identifier("prestito_attivo"),
        colonnanuova=sql.Identifier("somma_restituita"),colonnanome=sql.Identifier("cliente")),
        (nome_completo,cifra,data_prestito,"si",0,nome_completo))
        
        self.connessione.commit()
        fine = time.perf_counter()
        print(f"Query eseguita in {fine-inizio:0.4} secondi.")
    
    def somma_prestata(self,cliente):
        self.cursore.execute(sql.SQL("SELECT {colonna} FROM {tabella} WHERE {colonna2}=%s").format(colonna=sql.Identifier("denaro_in_prestito"),
        tabella=sql.Identifier("prestiti"),colonna2=sql.Identifier("cliente")),(cliente,))
        rows = self.cursore.fetchone()
        return rows[0]

    def somma_restituita(self,cliente):
        self.cursore.execute(sql.SQL("SELECT somma_restituita FROM prestiti WHERE {colonna}= %s").format(
            colonna=sql.Identifier("cliente")),(cliente,))
        row = self.cursore.fetchone()
        return row[0]
        

    def check_prestito(self,cliente,data):
        """Controlla se la somma restituita estingue il prestito ricevuto dalla banca,in tal caso 
        aggiorna lo stato del prestito da attivo a inattivo e aggiorna la data di chiusura del prestito """
        prestito = self.somma_prestata(cliente)
        somma = self.somma_restituita(cliente)
        if somma == prestito:
            self.cursore.execute(sql.SQL("UPDATE {tabella} SET {stato}=%s,{colonna2}=%s WHERE {colonna3}=%s").format(
            tabella=sql.Identifier("prestiti"),stato=sql.Identifier("prestito_attivo"),
            colonna2=sql.Identifier("prestito_concluso"),colonna3=sql.Identifier("cliente")),
            ("no",data,cliente))
            print("Il debito è stato estinto!!!")
            self.connessione.commit()

    def aggiorna_prestito(self,cliente,cifra,data):
        """ Aggiorna la somma restituita richiamando la funzione check_prestito che controlla
        se la somma restituita estingue o meno il prestito ricevuto dalla banca"""
        inizio = time.perf_counter()
        prestito = self.somma_prestata(cliente)
        somma = self.somma_restituita(cliente)
        self.cursore.execute(sql.SQL("""UPDATE {tabella} SET {colonna1}=%s,{stato}=%s
             WHERE {colonna2}=%s""").format(tabella=sql.Identifier("prestiti"),
            colonna1=sql.Identifier("somma_restituita"),
            stato=sql.Identifier("prestito_attivo"),
            colonna2=sql.Identifier("cliente")),
            (cifra + somma,"si",cliente))
        self.connessione.commit()
        self.check_prestito(cliente,data)
        fine = time.perf_counter()
        print(f"Query eseguita in {fine-inizio:0.4} secondi.")
        print("Ho aggiornato")  
    
    def prestito_in_corso(self,cliente):
        self.cursore.execute(sql.SQL("""SELECT ({colonna1}-{colonna2}) FROM {tabella}
             WHERE {colonna3}=%s""").format(colonna1=sql.Identifier("denaro_in_prestito"),
             colonna2=sql.Identifier("somma_restituita"),tabella=sql.Identifier("prestiti"),
             colonna3=sql.Identifier("cliente")),(cliente,))
        row = self.cursore.fetchone()
        return row[0]

    
#--------------------Trasferimento Soldi da Account a Account
    def trasferisci_denaro(self,Mittente,destinatario,cifra):
        """ Funzione Per il Trasferimento del denaro da un account all'altro utilizzando
        una transazione in modo che le operazioni vengono effettuate correttamente
        o tutto o niente """
        query = sql.SQL("""BEGIN; UPDATE {tabella} SET {colonna1}=%s WHERE {colonna2}=%s;
         UPDATE {tabella} SET {colonna1}=%s WHERE {colonna2}=%s; COMMIT;""").format(
             tabella=sql.Identifier("clienti"),colonna1=sql.Identifier("saldo_corrente"),
             colonna2=sql.Identifier("nome_completo"))
        colonne = (self.saldo_corrente(Mittente) - cifra,Mittente,self.saldo_corrente(destinatario) + cifra,destinatario)
        self.cursore.execute(query,colonne)
# {query per inserire dei dati specifici da una tabella all'altra } 
#insert into prestiti(cliente,id_cliente)select nome_completo,numero_account from clienti 
#where nome_completo='nome_completo' 
#        
#--------------------Cronologia-Prestiti
    def cronologia(self):
        """Funzione che copia le informazioni di un prestito dalla tabella prestiti alla tabella
            cronologia_prestiti solo se il prestito è stato saldato ed elimina la riga corrispondente
            dalla tabella prestiti utilizzando la transazione che inizia con BEGIN;codice..;COMMIT;"""
        self.cursore.execute(sql.SQL("""BEGIN; INSERT INTO {tabella}({colonna1},{colonna2},{colonna3},{colonna4},{colonna5})
        SELECT {colonna6},{colonna7},{colonna8},{colonna9},{colonna10} FROM {tabella2} WHERE {colonna11}=%s;
         DELETE FROM {tabella2} WHERE {colonna11}=%s;COMMIT;""").format(
            tabella=sql.Identifier("cronologia_prestiti"),colonna1=sql.Identifier("id_cliente"),
            colonna2=sql.Identifier("cliente"),colonna3=sql.Identifier("data_prestito"),
            colonna4=sql.Identifier("denaro_prestato"),colonna5=sql.Identifier("prestito_terminato"),
            colonna6=sql.Identifier("id_cliente"),colonna7=sql.Identifier("cliente"),
            colonna8=sql.Identifier("data_prestito"),colonna9=sql.Identifier("denaro_in_prestito"),
            colonna10=sql.Identifier("prestito_concluso"),tabella2=sql.Identifier("prestiti"),
            colonna11=sql.Identifier("prestito_attivo")),("no","no"))
        self.connessione.commit()
        print("Salvataggio completato!")

    def mostra_prestiti_cliente(self,cliente):
        self.cursore.execute(sql.SQL("SELECT * FROM {tabella} WHERE {colonna}=%s").format(
            tabella=sql.Identifier("cronologia_prestiti"),colonna=sql.Identifier("cliente")),(cliente,))
        rows = self.cursore.fetchall()
        nuova_lista = []
        for row in rows:
            row[2].strftime("%d/%m/%Y")
            nuova_lista += row
        return nuova_lista
     
#{ Stessa query per trasferire dati da una tabella all'altra
#insert into cronologia_prestiti(id_cliente,cliente,data_prestito,denaro_prestato,prestito_terminato)
#select id_cliente,cliente,data_prestito,denaro_in_prestito,prestito_concluso from prestiti
#where prestito_attivo='no'

        


#def crea_db():
#connessione = psycopg2.connect(db2)
#cursore = connessione.cursor()
#cursore.execute("CREATE DATABASE clienti_data")
#connessione.commit()

database = Database(db)
#print(database.prestito_in_corso("Johnzy"))
#database.aggiorna_cliente("ultimo","M","1010-11-19",3332321123,"mobile","Funzioni o no?","casa",300,"Forse 12","2020-04-21")
#print(database.mostra_prestiti_cliente("Johnzy"))
#database.aggiorna_prestito("Johnzy",100)
#print(database.somma_restituita("Johnzy"))
#print(database.cronologia("Johnzy"))
#database.Trasferisci_denaro("Johnzy","Pinocchio",100)
#print(database.visiona_prestito("Johnzy"))
#print(database.aggiorna_prestito("Johnzy",100))
#print(database.somma_restituita("Johnzy"))
#database.crea_prestito("Johnzy",200,"2020-04-11")
#database.aggiungi_in_Massa()
#print(database.saldo_corrente("Johnzy"))
#print(database.deposita(100,"Johnzy"))
#print(database.ritira("Johnzy",100))
#print(database.ritira("Johnzy"))
#print(database.Cerca_numero_account(12345))
#print(database.Cerca_nome("Johnzy"))
#self.elimina_cliente()
#database.mod_cliente(12344,"Johnzy")
#database.mod_col(cellulare,bigint)
#database.aggiungi_cliente("Jack Sparrow","M","22-03-1943","3333445891","giochino","Pizzaiolo","Nessuna",000,"Tokyo 11","07-04-2020",10000)
#print(database.visualizza_Staff())
#print(database.Visualizza_clienti())

#Staff_sql = "INSERT INTO Staff (nome,password,email) VALUES(%s,%s,%s)"
#staff_list = [("Ronaldo","admin","email@com"),
# ("Itachi","admin","email@com"),
# ("Admin1","admin","email@com"),
# ("Admin2","admin","email@com"),
# ("Admin3","admin","email@com")]
# self.cursore.executemany(Staff_sql,staff_list)
#ALTER TABLE clienti 
#ALTER COLUMN cellulare TYPE BIGINT,
#ALTER COLUMN numero_account TYPE BIGINT
