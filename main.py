import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from PIL import Image

from tkinter import *
from PIL import ImageTk
# Toutes les variables et fonctions liées à l'interface Tkinter sont préfixées "ui"

uiWindow = Tk()


uiWindow.title('La Colle')
uiWindow.geometry('400x250')

questions_list = []
nb_points = 0
id_q = IntVar()
tot_q = IntVar()
uiTxt_question = StringVar()
uiCanvas_reponses = Canvas(uiWindow)

# uiWindow.mainloop()

nl = 1

themes_jeu = {
  'A' : 'culture',
  'B' : 'suisse',
  'C' : 'histoire',
  'D' : 'musique'
}

themes_revision = {
  'A' : 'géologie',
  'B' : 'écologie',
  'C' : 'equadiffs',
  'D' : 'genetique',
  'E' : 'hydrologie',  
  'F' : 'chimie_orga',
  'G' : 'pedologie',
  'H' : 'informatique'
}

def uiClear(type):
    list = uiWindow.pack_slaves()
    if type == '':
      for i in list:
        i.destroy()
    else:
      for i in list:
        if i.winfo_class() == type:
          i.destroy()

def uiHome_Click():
  uiClear('')
  uiWelcome()

uiTxt_welcome = StringVar()
uiMenubar = Menu(uiWindow)
uiMenu1 = Menu(uiMenubar, tearoff=0)
uiMenubar.add_command(label="Retour", command=uiHome_Click)
uiMenubar.add_command(label='           ')
uiMenubar.add_command(label='')
uiMenubar.add_command(label='')

# --- Fonction : Accueil dans le quiz ---
def uiWelcome():
  uiMenuEmpty = Menu(uiWindow)
  uiMenuEmpty.add_command(label='')
  uiWindow.config(menu=uiMenuEmpty)

  print ('Bienvenue dans le quiz : La Colle', '\U0001F9D0\n\nPrêt.e à répondre aux questions ?\n ')

  uiTxt_welcome.set('Bienvenue dans le quiz : La Colle  \U0001F9D0\n\nPrêt.e à répondre aux questions ?\n\nQue voulez-vous faire ?\n')

  uiLabel_welcome = Label(uiWindow, textvariable=uiTxt_welcome)
  uiLabel_welcome.pack(side=TOP, pady=15)

  uiBtnPlay = Button(uiWindow, text ='Jouer', command=uiBtnPlay_Click).pack(side=LEFT, padx=15, pady=5)
  uiBtnRevise = Button(uiWindow, text ='Réviser', command=uiBtnRevise_Click).pack(side=RIGHT, padx=15, pady=5)


# --- Fonction : Évalue la réponse ---
def bot_answer(user_input, row):
  global nb_points 
  global reponses
  abcd = 'abcd'
  answer_2 = ""
  if user_input.lower() in abcd:
    answer = abcd.index(user_input.lower())
    answer_2 = reponses[answer]
  
  if answer_2 == row[1] :
    nb_points += 1
    message = ['Vrai', 'Bien joué', 'Super', 'Génial', 'Bravo', 'Juste',]
    a = random.choice(message) 
    g = (f'{a} ! Vous avez {nb_points} points !')
  else :
    message = ['Oh non !', 'Elle est où la culture ?', 'Zut !', 'Loupé !', 'Bien tenté !']
    a = random.choice(message)
    g = f'{a}\nLa réponse correcte est {row[1]} !'
  return g

# --- Fonction : Permet de choisir entre le dico du jeu et celui de la révision ---
def theme_choix (type) :
    global themes_jeu
    global themes_revision
    if type.lower() == 'a':
      return themes_jeu
    else :
      return themes_revision


# --- Fonction : Permet de choisr le thème voulu ---
def theme (c) :
  choix = ""
  for key, value in theme_choix(type).items() :
    if c.upper() == key :
      choix = value
  return choix


# --- Fonction : Commente le score ---
def commentaire_score () :
  global score
  if score == 0 :
    return 'Bonne nouvelle : Vous ne pourrez que faire mieux la prochaine fois !'
  elif 0 < score <= 20 :
    return 'Mettre les réponses au hasard aurait autant d\'efficacité !'
  elif 20 < score <= 40 :
    return 'Vous êtes encore loin du 100%, réessayez ! '
  elif 40 < score <= 60 :
    return 'Pas fameux ! Vous êtes capable de faire mieux !'
  elif 60 < score <= 80 :
    return 'Pas mal !'
  elif 80 < score < 100 :
    return 'Bravo !'
  elif score == 100 :
    return 'Félicitations \U0001F973 \U0001F973 \U0001F973'


def create_question():
  global uiCanvas_reponses
  global uiWaitVar
  global uiTxt_question

  id_q_local = id_q.get()

  row = questions_list[id_q_local-1]

  uiTxt_question.set(row[0])

  uiMenubar.entryconfigure(3,uiMenubar.entryconfigure(3, label=f'Question {id_q_local}/{tot_q.get()}'))

  reponses = [row[1], row[2], row[3], row[4]]
  random.shuffle(reponses) # réponses dans un ordre aléatoire

  uiGridList = uiSetGrid(reponses)

  uiCanvasList = []

  uiCanvas_reponses.destroy()

  uiCanvas_reponses_local = Canvas(uiWindow)
  uiCanvas_reponses_local.pack()
  uiCanvas_reponses = uiCanvas_reponses_local

  for i in reponses:
    print((row.index(i), reponses.index(i)))
    irow, icol = uiGridList[reponses.index(i)]
    uiBtn_reponse = Button(uiCanvas_reponses, text=i, command=lambda id_reponse=i: uiReponse_Click(row.index(id_reponse)))
    uiBtn_reponse.grid(row=irow, column=icol, sticky='nesw')
    
  # uiCanvas_reponses.pack()
  

def uiReponse_Click(i):
  global nb_points
  global id_q
  global tot_q

  id_q_local = id_q.get()

  line = questions_list[id_q_local-1]
  print(i)
  if i == 1:
    nb_points += 1
    uiMenubar.entryconfigure(4, label=f'Points : {nb_points}')
    message = ['Vrai', 'Bien joué', 'Super', 'Génial', 'Bravo', 'Juste',]
    a = random.choice(message)
    output = f'{a} ! Vous avez {nb_points} points !'
    messagebox.showinfo(title='La Colle', message=output)
  else :
    message = ['Oh non !', 'Elle est où la culture ?', 'Zut !', 'Loupé !', 'Bien tenté !']
    a = random.choice(message)
    output = f'{a}\nLa réponse correcte est {line[1]} !'
    messagebox.showerror(title='La Colle', message=output)

  if id_q_local < tot_q.get():
    id_q.set(id_q_local+1)
    create_question()


def play():
  global id_q
  global nb_points
  
  uiImg_question = StringVar()

  uiImg_question.set('pyrite.jpeg')

  uiImg_canvas = Canvas(uiWindow, height=120, bg='grey')

  uiImg_canvas.pack(side=TOP, padx=5, pady=5)

  #uiImg = ImageTk.PhotoImage(file = uiImg_question.get())
  #uiImg_canvas.create_image(0, 0, image = uiImg, anchor = nesw)

  

  Label(uiWindow, textvariable=uiTxt_question, wraplengt=380).pack()
  
  print("c'est parti")

  nb_points = 0
  uiMenubar.entryconfigure(4, label='Points : 0')
  answered_q = []
  id_q.set(1)
  create_question()
  # La 2e fois qu'on fait, il s'arrête avant le create_question
  

def uiBtnRoundsNb_Click():
  tot_q_local = tot_q.get()
  if tot_q_local > 0 and tot_q_local <= nl:
    uiClear('')
    play()



def SetRoundsNb(theme):
  # --- Ouverture du fichier ---
  global nl
  global questions_list

  f = open(f'{theme}.csv', encoding='utf-8')

  nl = len(f.readlines())
  f.seek(0)

  print((theme, nl))

  reader = csv.reader(f, delimiter=';')

  questions_list = [] # Permet d'éviter la répétition des questions
  for row in reader:
    questions_list.append(row)
  random.shuffle(questions_list)

  uiClear('Canvas')
  uiTxt_welcome.set(f"Entrez le nombre de tours de la partie\n(entre 1 et {nl}) : ")

  Entry(uiWindow, width = 5, textvariable = tot_q).pack()
  Button(uiWindow, text="C'est parti !", command=uiBtnRoundsNb_Click).pack(pady=15)


def uiSetGrid(themeDict):
  uiGridList = []
  # gridSize = int(sqrt(len(themeDict)) + 0.5) # grille carrée
  gridSize = int(len(themeDict)/2 + 0.5) # grille à 2 colonnes
  for irow in range(1, gridSize+1):
    for icol in range(1, 3):
      uiGridList.append((irow, icol))
  return uiGridList

def uiThemes_Click(v):
  for k, vt in themes_jeu.items():
    if v == vt:
      SetRoundsNb(themes_jeu[k])
      #return
  for k, vt in themes_revision.items():
    if v == vt:
      SetRoundsNb(themes_revision[k])
      #return

def uiGetThemes(themeDict):
  uiClear('Button')
  uiCanvas_themes = Canvas(uiWindow)
  uiGridList = uiSetGrid(themeDict)
  for i, v in enumerate(themeDict.values()):
    print(v)
    irow, icol = uiGridList[i]
    uiBtn_theme = Button(uiCanvas_themes, text=v.capitalize(), command=lambda theme=v: uiThemes_Click(theme)).grid(row=irow, column=icol, sticky='nesw')
  uiCanvas_themes.pack(side=BOTTOM, pady=15)
  uiMenubar.entryconfigure(3, label='')
  uiMenubar.entryconfigure(4, label='')
  uiWindow.config(menu=uiMenubar)

def uiBtnPlay_Click():
  uiTxt_welcome.set('Sur quel thème voulez-vous jouer ?')
  uiGetThemes(themes_jeu)
  
def uiBtnRevise_Click():
  uiTxt_welcome.set('Quel thème voulez-vous réviser ?')
  uiGetThemes(themes_revision)  


# --- Bienvenue ! ---
uiClear('')
uiWelcome()

# --- Effaçage du contenu du fichier progression ---
e = open ('progression.csv', 'w') # Permet d'avoir un fichier avec seulement les scores de cette partie
e.close()                         


# --- Boucle qui permet la partie, une fois terminée, d'être recommencée ---
retry = True 
nb_partie = 1
while retry == True :
  
# --- Choix du type de partie ---
  type = input ('\nQue voulez-vous faire ?\nA | Jouer\tB | Réviser\n\n')
  

# --- Choix du thème en début de partie ---
  if type == 'a' :
    print ('\nThèmes :\nA | Culture\tB | Suisse\tC | Histoire\tD | Musique\n')
    c = input('Quel thème voulez-vous étudier ? ') 
  else :
    print ('\nThèmes :\nA | Géologie\tB | Ecologie\tC | Equations différentielles\nD | Génétique\tE | Hydrologie\tF | Chimie organique \nG | Pédologie  \tH | Informatique\n')
    c = input('Quel thème voulez-vous étudier ? ')


# --- Ouverture du fichier ---
  questions_list = SetRoundsNb(theme(c))

# --- Choix du nombre de questions en début de partie ---
  repeat = True
  while repeat == True:
    tot_q = int(input("Entrez le nombre de tours de la partie : "))
    if tot_q > nl: # S'il n'y a pas assez de questions dans le csv, redemande d'entrer un autre nombre
      print(f"Il n'y a pas assez de questions disponibles ! Le nombre doit être compris entre 1 et {nl}.")
      repeat = True
    elif tot_q < 1:
      print(f"Le nombre doit être compris entre 1 et {nl}.")
    else: repeat = False

# --- Alterne entre question du bot, entrée de l'utilisateur et réponse du bot ---
  nb_points = 0
  answered_q = []

  for id_q in range(1, tot_q+1):
    re_ask = True
    row = questions_list[id_q-1]
 
    print (f'\nQuestion {id_q}/{tot_q}\n')
    reponses = [row[1], row[2], row[3], row[4]]
    reponses.sort() # réponses dans un ordre aléatoire
    a = reponses[0] # Il permet de mettre comme réponse a ou b ou c ou d
    b = reponses[1] 
    c = reponses[2]
    d = reponses[3]
    
    if row[5] == 'p' : # affiche une image si une image doit être visualiser
      myImage = Image.open(f"{row[6]}.jpeg");
      myImage.show();

    print(f"{row[0]}\nA | {a}\tB | {b}\tC | {c}\tD | {d}\n")    
    user_input = str(input("Votre réponse : "))
    print(f'\n {bot_answer(user_input, row)} \n')
    #f.seek(0)


# --- Mémorisation des scores ---

  score = nb_points/tot_q*100
  g = open ('progression.csv', 'a')
  writer = csv.writer(g, delimiter = ',')
  writer.writerow([nb_partie, score, tot_q, nb_points])
  g.close()


  # --- Fin de la partie ---
  print (f'La partie est terminée !\nVotre score final est de {round(score, 2)} % ({nb_points} points sur {tot_q}).\n')
  print (commentaire_score())
  recommence = str(input('\nVoulez-vous recommencer ? '))
  oui = ['oui', 'yes','o','y']
  if recommence.lower() in oui :
    nb_partie += 1
    retry = True
  else :
    retry = False

# --- Permet de faire le graphe des scores ---
h = open ('progression.csv', 'r')
reader_h = csv.reader(h, delimiter = ',')
x = []
y = []
s = []
p = []
for row in reader_h:
  x.append(float(row[0]))
  y.append(float(row[1]))
  s.append(float(row[2]))
  p.append(float(row[3]))
h.close()

# --- Propose de voir le graphe de la progression ---  
voir_score = input ('Voulez-vous voir vos scores ? ')
if voir_score.lower()in oui :
  print (f'Vous avez obtenu {sum(p)} points sur {sum(s)}.\n'f'La moyenne est de {round(sum(p)/sum(s)*100,2)}%\n')
  plt.plot(x,y)
  plt.show ()
  print ('\nLe quiz est terminé ! A bientôt !')  
else :
  print ('\nLe quiz est terminé ! A bientôt !')
    
