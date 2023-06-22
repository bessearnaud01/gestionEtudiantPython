from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import os  # elle nous permet de faire des actions au niveau du system


class Etudiant:

    def __init__(self):
        self.window = Tk()
        self.window.title("Etudiant")
        self.window.geometry("1250x580+0+0")
        self.window.minsize(480, 360)
        self.window.config(background='#e3e3e3')

        # initialization des components
        self.frame = Frame(self.window, bd=5, relief=GROOVE, bg='white')
        self.frame.place(x=10, y=50, width=330, height=470)

        Label(self.frame, text="Les informations de l'étudiant", font=("Matey", 12, "bold"), bg="#FFFFFF").place(
            x=20, y=20)

        # Déclaration des variables

        self.id = StringVar()
        self.nom = StringVar()
        self.mail = StringVar()
        self.sexe = StringVar()
        self.nom = StringVar()
        # self.adresse = StringVar() avec adresse on ne va pas declarer sa variable on l'a deja fait en bas
        self.date = StringVar()
        self.contact = StringVar()
        self.val_Recherche_par = StringVar()
        self.val_Recherche = StringVar()

        Label(self.frame, text="ID étudiant :", font=("Helvetica", 10, "bold"), bg="#FFFFFF").place(x=10, y=70)
        txtId = Entry(self.frame, textvariable=self.id, font=("Helvetica", 10), bg="lightgrey")
        txtId.place(x=119, y=70.5, width=150)

        Label(self.frame, text="Nom et prénom :", font=("Helvetica", 10, "bold"), bg="#FFFFFF").place(x=10, y=100)
        txtNomCplet = Entry(self.frame, textvariable=self.nom, font=("Helvetica", 10), bg="lightgrey")
        txtNomCplet.place(x=119, y=100.5, width=150)

        Label(self.frame, text="E-Mail :", font=("Helvetica", 10, "bold"), bg="#FFFFFF").place(x=10, y=130)
        txtMail = Entry(self.frame, textvariable=self.mail, font=("Helvetica", 10), bg="lightgrey")
        txtMail.place(x=119, y=130.5, width=150)

        Label(self.frame, text="Sexe :", font=("Helvetica", 10, "bold"), bg="#FFFFFF").place(x=10, y=160)
        txt_Sexe = ttk.Combobox(self.frame, textvariable=self.sexe, font=("Helvetica", 10), state="readonly")
        txt_Sexe["values"] = ("Select", "M", "F")
        txt_Sexe.place(x=119, y=160, width=100)
        txt_Sexe.current(0)

        Label(self.frame, text="Contact :", font=("Helvetica", 10, "bold"), bg="#FFFFFF").place(x=10, y=190)
        txtContact = Entry(self.frame, textvariable=self.contact, font=("Helvetica", 10), bg="lightgrey")
        txtContact.place(x=119, y=190.5, width=150)

        Label(self.frame, text="Date naissance:", font=("Helvetica", 10, "bold"), bg="#FFFFFF").place(x=10, y=220)
        txtDate = Entry(self.frame, textvariable=self.date, font=("Helvetica", 10), bg="lightgrey")
        txtDate.place(x=119, y=220.5, width=148)

        Label(self.frame, text="Adresse:", font=("Helvetica", 10, "bold"), bg="#FFFFFF").place(x=10, y=250)
        self.txtAdresse = Text(self.frame, font=("Helvetica", 10), bg="lightgrey")
        self.txtAdresse.place(x=119, y=250.5, width=150, height=50)

        Button(self.frame, text="Ajouter", font=("Helvetica", 10), command=self.add, relief=GROOVE, bd=6,
               bg="lightgrey",
               cursor="hand2").place(x=0, y=350, width=70)
        Button(self.frame, text="Modifier", font=("Helvetica", 10), command=self.update, relief=GROOVE, bd=6,
               bg="lightgrey",
               cursor="hand2").place(x=75, y=350, width=70)
        Button(self.frame, text="Supprimer", font=("Helvetica", 10), command=self.delete, relief=GROOVE, bd=6,
               bg="lightgrey",
               cursor="hand2").place(x=150, y=350, width=75)
        Button(self.frame, text="Réinitialiser", font=("Helvetica", 10), command=self.initialize, relief=GROOVE, bd=6,
               bg="lightgrey",
               cursor="hand2").place(x=230, y=350, width=90)

        # Affichage du tableau

        self.frame1 = Frame(self.window, bd=5, relief=GROOVE, bg='white')
        self.frame1.place(x=350, y=50, width=860, height=470)
        Label(self.frame1, text="Tableau des étudiants", font=("Helvetica", 12, "bold"), bg="#FFFFFF").place(x=320,
                                                                                                             y=10)
        Label(self.frame1, text="Rechercher nom :", font=("Helvetica", 9, "bold"), bg="#FFFFFF").place(x=150, y=70)
        #Recherche = ttk.Combobox(self.frame1, textvariable=self.val_Recherche_par, font=("Helvetica", 10),
                             #    state="readonly")
        #Recherche["values"] = ("Select", "id", "nom", "contact")
        #Recherche.place(x=235, y=70, width=90)
        #Recherche.current(0)
        # Texte d'entée
        txtRecherche = Entry(self.frame1, font=("Helvetica", 10), bg="lightgrey", textvariable=self.val_Recherche)
        txtRecherche.place(x=300, y=70, width=150)

        Button(self.frame1, text="Recherche", font=("Helvetica", 10), command=self.rechercheEtudiant, relief=GROOVE,
               bd=6, bg="lightgrey",
               cursor="hand2").place(x=480, y=62, width=90)
        Button(self.frame1, text="Afficher tous", font=("Helvetica", 10), command=self.afficherRecherche, relief=GROOVE,
               bd=6, bg="lightgrey",
               cursor="hand2").place(x=595, y=62, width=100)

        self.frame2 = Frame(self.window, bd=5, relief=GROOVE, bg='white')
        self.frame2.place(x=350, y=170, width=800, height=300)

        scrollx = Scrollbar(self.frame2, orient=HORIZONTAL)
        scrolly = Scrollbar(self.frame2, orient=VERTICAL)
        self.tableau = ttk.Treeview(self.frame2, columns=("id", "nom", "mail", "sexe", "contact", "date", "adresse"),
                                    xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        self.tableau.heading("id", text="Id-user")
        self.tableau.heading("nom", text="Nom complet")
        self.tableau.heading("mail", text="Mail")
        self.tableau.heading("sexe", text="Sexe")
        self.tableau.heading("contact", text="Contact")
        self.tableau.heading("date", text="Date de naissance")
        self.tableau.heading("adresse", text="Adresse")

        self.tableau["show"] = "headings"

        self.tableau.column("id", width=100)
        self.tableau.column("nom", width=100)
        self.tableau.column("mail", width=100)
        self.tableau.column("sexe", width=100)
        self.tableau.column("contact", width=100)
        self.tableau.column("date", width=100)
        self.tableau.column("adresse", width=100)
        self.tableau.pack()
        self.tableau.bind("<ButtonRelease-1>", self.getInformation)
        self.afficherRecherche()

    def add(self):
        if self.id.get() == "" or self.nom.get() == "" or self.mail.get() == "" or self.txtAdresse.get("1.0",
                                                                                                       END) == "":

            messagebox.showerror("Erreur", "Vous n'avez pas remplit les champs obligatoire")
        else:
            # On se connecte à la base de données
            con = pymysql.connect(host="localhost", user="root", password="berenger1996", database="python_etudiants")
            # On se connecte table
            cur = con.cursor()
            # on va teste si le mail existe apres la question et le reponse existe et en comparant les saisit du formulaire et de la base de données
            cur.execute("insert into etudiants values(%s,%s,%s,%s,%s,%s,%s)",
                        (self.id.get(), self.nom.get(), self.mail.get(), self.sexe.get(), self.contact.get(),
                         self.date.get(), self.txtAdresse.get("1.0", END)))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "L'utilisateur est enregistré")
            self.afficherRecherche()

    # Elle permet de vider les champs
    def initialize(self):
        self.id.set(''),
        self.nom.set(''),
        self.mail.set(''),
        self.contact.set(''),
        self.date.set(''),

        self.txtAdresse.delete("1.0", END)

    # elle sert à raffraichir la table des étudiants
    def afficherRecherche(self):
        # On se connecte à la base de données
        con = pymysql.connect(host="localhost", user="root", password="berenger1996", database="python_etudiants")
        # On se connecte table
        cur = con.cursor()
        cur.execute("select *from etudiants")
        # On va recuperer les étudiants avec fetchall
        rows = cur.fetchall()

        if len(rows) != 0:
            self.tableau.delete(*self.tableau.get_children())
            for row in rows:
                self.tableau.insert("", END, values=row)
        con.commit()
        con.close()

    # Elle permet de recuperer 1 user dans le formulaire
    def getInformation(self, ev):

        cursors_row = self.tableau.focus()
        contents = self.tableau.item(cursors_row)
        row = contents["values"]
        self.id.set(row[0]),
        self.nom.set(row[1]),
        self.mail.set(row[2]),
        self.sexe.set(row[3]),
        self.contact.set(row[4]),
        self.date.set(row[5]),
        self.txtAdresse.delete("1.0", END)
        self.txtAdresse.insert(END, row[6])

    def update(self):
        # On se connecte à la base de données
        con = pymysql.connect(host="localhost", user="root", password="berenger1996", database="python_etudiants")
        # On se connecte table
        cur = con.cursor()
        cur.execute("update etudiants set nom=%s,mail=%s,sexe=%s,contact=%s,date=%s,adresse=%s where id=%s", (
            self.nom.get(), self.mail.get(), self.sexe.get(), self.contact.get(), self.date.get(),
            self.txtAdresse.get("1.0", END),
            self.id.get()
        ))

        # On va recuperer les étudiants avec fetchall
        con.commit()
        messagebox.showinfo("Succès", "Enregistrement éffectué")
        self.afficherRecherche()
        self.initialize()
        con.close()

    def delete(self):
        # On se connecte à la base de données
        con = pymysql.connect(host="localhost", user="root", password="berenger1996", database="python_etudiants")
        # On se connecte table
        cur = con.cursor()
        cur.execute("delete from etudiants where id=%s", self.id.get())
        # On va recuperer les étudiants avec fetchall
        con.commit()
        messagebox.showinfo("Succès", "Enregistrement éffectué")
        self.afficherRecherche()
        self.initialize()
        con.close()

    def rechercheEtudiant(self):
        # On se connecte à la base de données
        con = pymysql.connect(host="localhost", user="root", password="berenger1996", database="python_etudiants")
        # On se connecte table
        cur = con.cursor()
        cur.execute("""select * from etudiants where nom = %s""",
                    (self.val_Recherche.get()))

        rows = cur.fetchall()
        if len(rows) != 0:
            self.tableau.delete(*self.tableau.get_children())
            for row in rows:
                self.tableau.insert("", END, values=row)
        # On va recuperer les étudiants avec fetchall
       # else:
             # print("Rien trouve") print("select * from etudiants where %s like %s",)
            #(self.val_Recherche_par.get(), "'%" + self.val_Recherche.get() + "%'"))
        con.close()


# afficher
app = Etudiant()
app.window.mainloop()
