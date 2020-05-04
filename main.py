import tkinter as tk
import sys
import backend_bank
from pannello import Pannello


def staff_log():
    try:
        for row in backend_bank.database.visualizza_staff():
            if user_entry.get() == row[0] and password_entry.get() == row[1]:
                root.wm_state("iconic")
                app = tk.Toplevel(width=700,height=625)
                Pannello(app)
                app.title("Benvenuto nel Sistema Bancario senza Interessi")
        else:
            info.config(bg="red",fg="white",text="Acceso negato ,Username o password incorrette")              
    except:
        pass

root = tk.Tk()
root.title("Banca Future")
Font = ("ariel",12)
#--------------------Widgtes
finestra = tk.Canvas(root,width=400,height=400)
sfondo = tk.PhotoImage(file="img\sfondo1.png")
sfondo_label = tk.Label(root,image=sfondo)
sfondo_label.place(relwidth=1,relheight=1)
finestra.pack()
user_text = tk.StringVar()
user = tk.Label(root,text="Username",font=Font)
user.place(relx=0.22,rely=0.54)
user_entry = tk.Entry(root,textvariable=user_text,font=Font,bd=2)
user_entry.place(relx=0.075,rely=0.60,relheight=0.07,relwidth=0.4)
password = tk.Label(root,text="Password",font=Font)
password.place(relx=0.59,rely=0.54)
password_text = tk.StringVar()
password_entry= tk.Entry(root,textvariable=password_text,font=Font,bd=2,show="*")
password_entry.place(relx=0.52,rely=0.60,relheight=0.07,relwidth=0.4)
accedi_img = tk.PhotoImage(file="img\login.png")
accedi = tk.Button(root,text=" Accedi",font=Font,bg="white",image=accedi_img,compound=tk.LEFT,command=staff_log)
accedi.place(relx=0.35,rely=0.70,relheight=0.125)
info = tk.Label(root,text="Possono accedere solo gli operatori bancari",font=("arial",9),bg="white")
info.place(relx=0.07,rely=0.83)
root.mainloop()

