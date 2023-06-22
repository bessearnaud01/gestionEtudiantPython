from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import os  # elle nous permet de faire des actions au niveau du system


class Login:

    def __init__(self):


        self.window1 = None
        self.window = Tk()
        self.window.title("Register")
        self.window.geometry("750x580+0+0")
        self.window.minsize(480, 360)
        self.window.config(background='#41B77F')
        self.window.focus_force()  # on veut force la fénêtre

        # initialization des composants
        self.frame = Frame(self.window, bg='red')

        self.frame.place(x=220, y=150, width=350, height=320)

        Label(self.frame, text="Connexion", font=("Helvetica", 18, "bold"), bg="red", fg="#FFFFff").place(x=100, y=10)

        Label(self.frame, text="Mail", font=("Helvetica", 14), bg="red", fg="#FFFFff").place(x=150, y=60)
        self.txtMail = Entry(self.frame, font=("Helvetica", 14), bg="lightgrey")
        self.txtMail.place(x=65, y=90, width=220)

        Label(self.frame, text="Mot de passe", font=("Helvetica", 14), bg="red", fg="#FFFFFF").place(x=110, y=130)

        self.txt_MotDepasse = Entry(self.frame, show="*", font=("Helvetica", 14), bg="lightgrey")
        self.txt_MotDepasse.place(x=65, y=160, width=220)

        Button(self.frame, text="Créer un nouveau un compte", command=self.window_register,font=("Helvetica", 8), bd=0, bg="red",
               cursor="hand2").place(x=15, y=190)
        Button(self.frame, text="Mot de passe oublié", command=self.fenetre_MotdePasseOuBlie, font=("Helvetica", 8), bd=0,
               bg="red", cursor="hand2").place(
            x=215, y=190)
        Button(self.frame, text="Connexion..", command=self.login, font=("Helvetica", 10), bg="lightgrey",
               cursor="hand2").place(x=120, y=220, width=100)

    def login(self):
        if self.txt_MotDepasse.get() == "" or self.txtMail.get() == "":
            messagebox.showerror("Erreur", "Veuillez saisir le mail et le mot de passe")
        else:
            try:
                # On se connecte à la base de données
                connexion = pymysql.connect(host="localhost", user="root", password="berenger1996",
                                            database="python_etudiants")
                # On se connecte table
                cur = connexion.cursor()
                # On va et on va recupèrer nos mails et %s est une valeur par défaut parce qu'on ne connait pas
                # les valeurs de mail et mot de passe
                cur.execute("select *from comptes where email=%s and motdepasse=%s ", (self.txtMail.get(),
                                                                                       self.txt_MotDepasse.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Erreur", "Le mail et le mot de passe sont incorrectes")
                else:
                    messagebox.showinfo("Success", "Bienvenu")
                    import etudiant
                    connexion.close()

            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion{str(ex)}")

        # Elle sert vider les champs dans le formulaire e
    def vider_Champs(self):
        self.question.current(0) # question est combobox donc utilise ça
        self.Reponse.delete(0, END)
        self.new_motdepasse.delete(0, END)

    # Elle permet d'afficher le formulaire de mot de passe oublié
    def fenetre_MotdePasseOuBlie(self):
        if self.txtMail.get() == "":
            messagebox.showerror("Erreur", "Veuillez saisir uniquement votre mail")
        else:
            try:
                # On se connecte à la base de données
                connexion = pymysql.connect(host="localhost", user="root", password="berenger1996",
                                            database="python_etudiants")
                # On se connecte table
                cur = connexion.cursor()
                # on veut tester si le mail existe dans la base de données
                # On va et on va recupèrer nos mails et %s est une valeur par défaut parce qu'on ne connait pas
                # on va comparer le mail saisit eslf.txtMail.get()
                cur.execute("select *from comptes where email=%s ", self.txtMail.get())
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Erreur", "Veuillez saisir le mail n'est pas correcte")
                else:
                    connexion.close() # on ferme la connexion
                    self.window1 = Toplevel()
                    self.window1.title("Mot de passe oublié")
                    self.window1.config(bg="white")
                    self.window1.geometry("750x580+0+0")
                    # lorsqu'on ouvre cette fénêtre on peut pas clique sur autre fénête
                    self.window1.focus_force()
                    self.window1.grab_set()
                    title = Label(self.window1, text=" Le mot de passe oublié", font=("Helvetica", 18), bg="red",
                                  fg="#FFFFFF")
                    title.pack(side=TOP, fill=X)
                    Label(self.window1, text="Sélectionner une question :", font=("Helvetica", 14), bg="white",
                          fg="black").place(x=82, y=150)
                    # state="readonly" permet de ne pas modifier les valeur ds le champs du combobox
                    self.question = ttk.Combobox(self.window1, font=("Helvetica", 14), state="readonly")
                    self.question["values"] = ( "Select", "Ton surnom", "Ton lieu de naissance", "Le nom de ton meilleur ami")
                    self.question.place(x=320, y=150, width=250)
                    # Elle permet d'affiche la case 0 = votre choix par defaut dans le combobox
                    self.question.current(0)


                    Label(self.window1, text="Réponse :", font=("Helvetica", 14), bg="white",
                          fg="black").place(x=220, y=200)
                    self.Reponse = Entry(self.window1, font=("Helvetica", 14), bg="#FFFFFF")
                    self.Reponse.place(x=324, y=200, width=250)

                    Label(self.window1, text="Nouveau mot de passe :", font=("Helvetica", 14), bg="white",
                          fg="black").place(x=50, y=260)
                    self.new_motdepasse = Entry(self.window1, font=("Helvetica", 14), bg="#FFFFFF",show="*",)
                    self.new_motdepasse.place(x=320, y=260, width=250)
                    Button(self.window1, text="Modifier Mot de passe", command=self.motDePasseOublie,font=("Helvetica", 16),
                           bg="red",cursor="hand2").place(x=320, y=300, width=250)
            except Exception as ex:
                # lorsqu'on arrive pas à se connecte sur une base de données
                # et tranforme l'erreur en chaîne de caractère avec connexion{str(ex)}
                messagebox.showerror("Erreur", f"Erreur de connexion{str(ex)}")

    # Cette fonction à le  modifier mot de passe
    def motDePasseOublie(self):
        if self.Reponse.get() == "" or self.question.get() == "" or self.new_motdepasse.get() == "":
            messagebox.showerror("Erreur", "Veuillez Remplir les champs")
        else:
            try:
                # On se connecte à la base de données
                con = pymysql.connect(host="localhost", user="root", password="berenger1996", database="python_etudiants")
                # On se connecte table
                cur = con.cursor()
                # on va teste si le mail existe apres la question et le reponse existe et en comparant les saisit du formulaire et de la base de données
                cur.execute("select *from comptes where email=%s and question=%s and reponse=%s ", (self.txtMail.get(),self.question.get(), self.Reponse.get()))

                row = cur.fetchone()
                # si  la question et la reponse ne st pas correcte
                if row is None:  # row == None
                    messagebox.showerror("Erreur", "la question et la réponse données ne correspond pas l'or de votre inscription")

                else: # on veut modifier le mot de passe sachant qu'on connait le le mail
                    cur.execute("update comptes set motdepasse=%s where email=%s ",(self.new_motdepasse.get(), self.txtMail.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Le mot de passe a été modifier")
                    self.vider_Champs()
                    self.window1.destroy()

            except Exception as es:
                messagebox.showerror("Erreur", "Veuillez saisir votre question et reponse")

    # Cette fonction permet d'aller sur la page register
    def window_register(self):
        self.window.destroy()
        import register





app = Login()
app.window.mainloop()
