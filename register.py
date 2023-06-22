from tkinter import *
from tkinter import ttk, messagebox
import pymysql


class Register:

    def __init__(self):
        self.window = Tk()
        self.window.title("Register")
        self.window.geometry("750x580+0+0")
        self.window.minsize(480, 360)
        self.window.config(background='#41B77F')

        # initialization des composants
        self.frame = Frame(self.window, bg='red')

        self.frame.place(x=90, y=60, width=600, height=470)

        Label(self.frame, text=" Créer un compte", font=("Helvetica", 18, "bold"), bg="red", fg="#FFFFff").place(x=60,
                                                                                                                 y=10)

        Label(self.frame, text="Nom :", font=("Helvetica", 14), bg="red", fg="#FFFFff").place(x=16, y=50)
        self.txtNom = Entry(self.frame, font=("Helvetica", 14), bg="lightgrey")
        self.txtNom.place(x=16, y=90, width=250)

        Label(self.frame, text="Prénom :", font=("Helvetica", 14), bg="red", fg="#FFFFFF").place(x=300, y=50)
        self.txtPrenom = Entry(self.frame, font=("Helvetica", 14), bg="lightgrey")
        self.txtPrenom.place(x=300, y=90, width=250)

        Label(self.frame, text="Téléphone :", font=("Helvetica", 14), bg="red", fg="#FFFFff").place(x=16,
                                                                                                    y=120)
        self.txtPhone = Entry(self.frame, font=("Helvetica", 14), bg="lightgrey")
        self.txtPhone.place(x=16, y=150, width=250)

        Label(self.frame, text="Mail :", font=("Helvetica", 14), bg="red", fg="#FFFFff").place(x=300, y=120)

        self.txtMail = Entry(self.frame, font=("Helvetica", 14), bg="lightgrey")
        self.txtMail.place(x=300, y=150, width=250)

        Label(self.frame, text="Sélectionner une question :", font=("Helvetica", 14), bg="red", fg="#FFFFff").place(
            x=16,
            y=190)
        # state="readonly" permet de ne pas modifier les valeur ds le champs du combobox
        self.txt_question = ttk.Combobox(self.frame, font=("Helvetica", 14), state="readonly")
        self.txt_question["values"] = (
            "Votre choix", "Ton surnom", "Ton lieu de naissance", "Le nom de ton meilleur ami")
        self.txt_question.place(x=16, y=220, width=250)
        # Elle permet d'affiche la case 0 = votre choix par defaut dans le combobox
        self.txt_question.current(0)

        Label(self.frame, text="Réponse :", font=("Helvetica", 14), bg="red", fg="#FFFFff").place(x=300, y=190)

        self.txt_Reponse = Entry(self.frame, font=("Helvetica", 14), bg="lightgrey")
        self.txt_Reponse.place(x=300, y=220, width=250)

        Label(self.frame, text="Mot de passe :", font=("Helvetica", 14), bg="red", fg="#FFFFff").place(x=16, y=260)

        self.txt_MotDepasse = Entry(self.frame, show="*", font=("Helvetica", 14), bg="lightgrey")
        self.txt_MotDepasse.place(x=16, y=300, width=250)

        Label(self.frame, text="Confirmation mot de passe :", font=("Helvetica", 14), bg="red", fg="#FFFFff").place(
            x=300, y=260)

        # show = "*" permet de cacher le mot de passe dans le champs
        self.txt_Confirmation_MotDepasse = Entry(self.frame, show="*", font=("Helvetica", 14), bg="lightgrey")
        self.txt_Confirmation_MotDepasse.place(x=300, y=300, width=250)

        self.Txt_Var_Check = IntVar()
        Checkbutton(self.frame, variable=self.Txt_Var_Check, onvalue=1, offvalue=0, cursor="hand2",
                    text="J'accepte les condition et les termes",
                    font=("Helvetica", 14), bg="red").place(x=16, y=350)

        # Creation de boutton

        Button(self.frame, text="Enregistre", command=self.create, font=("Helvetica", 14), bg="lightgrey",
               width="20").place(x=180, y=390)

        Button(self.frame, text="Connexion....", command=self.window_login, font=("Helvetica", 12), bg="lightgrey").place(x=465, y=20)

    def create(self):
        if self.txtNom.get() == "" or self.txtPrenom.get() == "" or self.txt_Reponse.get() == '' or self.txtMail.get() == "" or self.txt_question.get() == "" or self.txtPhone.get() == "" or self.txt_MotDepasse.get() == "" or self.txt_Confirmation_MotDepasse.get() == "":
            messagebox.showerror("Erreur", "Remplir les champs")
        elif self.txt_MotDepasse.get() != self.txt_Confirmation_MotDepasse.get():
            messagebox.showerror("Erreur", "Les mots de passes ne sont pas conformes")
        elif self.Txt_Var_Check.get() == 0:
            messagebox.showerror("Erreur", "Veuillez accepter les conditions et terme")

        else:
            try:
                # On se connecte à la base de données
                connexion = pymysql.connect(host="localhost", user="root", password="berenger1996",
                                            database="python_etudiants")
                # On se connecte table
                cur = connexion.cursor()
                # On va et on va recupèrer le mail saisit  self.txtMail.get()
                # et les comparer aux mails aux bases données et les amene message d'erreur s'il existe
                cur.execute("select *from comptes where email=%s", self.txtMail.get())
                row = cur.fetchone()

                # si Row est different alors le mail exite ds la base de données
                if row is not None:
                    messagebox.showerror("Erreur", "Le mail est existe déja")
                else:
                    cur.execute(
                        "insert into comptes(nom, prenom, phone, email, motdepasse, question, reponse) values(%s,%s,%s,%s,%s,%s,%s)",
                        (self.txtNom.get(),  # elle sert à inserer les données saisir ds la base de données
                         self.txtPrenom.get(),
                         self.txtPhone.get(),
                         self.txtMail.get(),
                         self.txt_MotDepasse.get(),
                         self.txt_question.get(),
                         self.txt_Reponse.get(),
                         ))
                    messagebox.showinfo("Success", "Votre compte a été créer")
                connexion.commit()  # on envoye les données à la base de données
                self.initialize()
                connexion.close()  # on ferme la connexion après envoie

            except Exception as es:
                # s'il y a des problème de connexion on rentre ds le except
                messagebox.showerror("Erreur", f"erreur de connexion,{str(es)}")

    def initialize(self):
        self.txtNom.delete(0, END),
        self.txtPrenom.delete(0, END),
        self.txtPhone.delete(0, END),
        self.txtMail.delete(0, END),
        self.txt_Confirmation_MotDepasse.delete(0, END)
        self.txt_MotDepasse.delete(0, END)
        self.txt_question.delete(0, END)
        self.txt_Reponse.delete(0, END)

    # Cette fonction permet d'aller sur la page register
    def window_login(self):
        self.window.destroy()
        import login


# afficher
app = Register()
app.window.mainloop()
