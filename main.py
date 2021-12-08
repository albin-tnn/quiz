# Quiz
# Projet dans le cadre du cours de programmation I
# Auteur.e.s : Rémi Stamp, Albin Tanné, Johanna Puglia


import os
import csv
import random
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from matplotlib.figure import Figure
from matplotlib.pyplot import *
from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.font as font
from PIL import ImageTk,Image
import time
matplotlib.use('TkAgg')


themes_jeu = {
  'culture' : 'Culture',
  'suisse' : 'Suisse',
  'histoire' : 'Histoire',
  'musique' : 'Musique',
  'citations' : 'Citations',
  'tout_jeu' : 'Tous'
}

themes_revision = {
  'géologie' : 'Géologie',
  'écologie' : 'Écologie',
  'equadiffs' : 'Équations diff.',
  'genetique' : 'Génétique',
  'hydrologie' : 'Hydrologie',  
  'chimie_orga' : 'Chimie organique',
  'pedologie' : 'Pédologie',
  'informatique' : 'Informatique',
  'tout_revision' : 'Tous'
}

themes_images = {
  'géologie' : 'geologie.jpg',
  'écologie' : 'ecologie.jpg',
  'equadiffs' : 'equa_diff.jpg',
  'genetique' : 'genetique.jpg',
  'hydrologie' : 'hydro.jpg',  
  'chimie_orga' : 'chimie_orga.jpg',
  'pedologie' : 'pedologie.jpg',
  'informatique' : 'informatique.png',
  'culture' : 'culture.jpg',
  'suisse' : 'suisse.png',
  'histoire' : 'histoire.jpg',
  'musique' : 'musique.png',
  'citations' : 'citation.png'
}

# Les variables et fonctions purement liées à l'interface Tkinter sont préfixées "ui"

window = Tk()
window.title('La Colle')
window.geometry('600x400')
isWindowBig = False

if os.name == 'nt': # si exécuté sur Windows
  window.configure(bg='#F0F0F0') # évite un bug lors de la création du graph

uiTxt_welcome = StringVar()
uiTxt_question = StringVar()
uiCanvas_reponses = Canvas(window)
uiCanvas_progress = Canvas(window, height=30)
uiProgressbar = Progressbar(uiCanvas_progress, length=500)

questions_list = []
nb_points = 0
nl = 1
id_q = IntVar() # Index de la question
tot_q = IntVar() # Nombre de tours choisis par l'utilisateur
tot_q.set(1)

# Compte à rebours (càr.)
timerOn = IntVar() # Valeur booléenne, 1 si utilisateur utilise le càr.
timerVal = IntVar() # Temps du càr. défini par l'utilisateur
timerVal.set(10)
timerSeconds = IntVar() # Temps restant affiché en direct
isPaused = False # Pause quand réponse choisie ou càr. à 0
timerList = [] # Liste des temps passés sur chaque question, pour afficher le total à la fin

uiCanvas_image = Canvas(window, height=int(window.winfo_height()/3))
uiEntry_timer = Entry(window, width=5, textvariable=timerVal)
uiLabel_timer = Label(window, text='Entrez le temps du compte à rebours (en secondes) :')


def uiClear(objType):
  global uiMenuLabel
  global uiMenuPoints

  objList = window.pack_slaves()
  if objType == '': # Supprime tous les objets de la fenêtre, sauf canvas4 (qui contient le bouton Retour)
    uiMenuLabel.config(text=' ')
    uiMenuPoints.config(text=' ')
    for i in objList:
      if str(i) != '.!canvas4':
        i.destroy()
  else:
    for i in objList: # Supprime tous les objets du type spécifié
      if i.winfo_class() == objType and str(i) != '.!canvas4':
        i.destroy()
  font.nametofont("TkDefaultFont").configure(family="")


def uiHome_Click():
  uiClear('')
  Welcome()


uiMenubar = Canvas(window, height=30)
uiMenubar.myId = 'menubar'
uiMenuBtn = Button(uiMenubar, text="Retour", command=uiHome_Click)
uiMenuLabel = Label(uiMenubar)
uiMenuPoints = Label(uiMenubar)
uiMenuBtn.pack(side=LEFT)
uiMenuPoints.pack(side=RIGHT, padx=50)
uiMenuLabel.pack(side=RIGHT, padx=10)

print('Il ne se passe rien ici, utilisez la fenêtre Tkinter !')

def uiSetWindowSize():
  global isWindowBig

  isWindowBig = not isWindowBig
  if isWindowBig:
    window.geometry('1000x600')
    font.nametofont("TkDefaultFont").configure(size=16)
    rcParams.update({'font.size': 16})
  else:
    window.geometry('600x400')
    font.nametofont("TkDefaultFont").configure(size=10)
    rcParams.update({'font.size': 10})
  

# --- Fonction : Accueil dans le quiz ---
def Welcome():
  uiMenuBtn.pack_forget()
  uiMenubar.pack(side=TOP, fill=BOTH)

  uiTxt_welcome.set('Bienvenue dans le quiz : La Colle \n\nPrêt.e à répondre aux questions ?\n\nQue voulez-vous faire ?\n')

  uiLabel_welcome = Label(window, textvariable=uiTxt_welcome)
  uiLabel_welcome.pack(side=TOP, pady=15)

  Button(window, text ='Jouer', command=uiBtnPlay_Click).pack(side=LEFT, padx=50, pady=5)
  Button(window, text ='Réviser', command=uiBtnRevise_Click).pack(side=RIGHT, padx=50, pady=5)
  Button(window, text = 'Taille de la fenêtre', command=uiSetWindowSize).pack(side=BOTTOM, pady=20)

def uiBtnPlay_Click():
  uiTxt_welcome.set('Sur quel thème voulez-vous jouer ?')
  displayThemes(themes_jeu)
  
def uiBtnRevise_Click():
  uiTxt_welcome.set('Quel thème voulez-vous réviser ?')
  displayThemes(themes_revision)

# --- Retourne une liste des positions de chaque élément d'une liste dans une grille ---
def uiSetGrid(itemsList):
  uiGridList = []
  # gridSize = int(sqrt(len(themeDict)) + 0.5) # si grille carrée
  gridSize = int(len(itemsList)/2 + 0.5) # si grille à 2 colonnes
  for irow in range(1, gridSize+1):
    for icol in range(1, 3):
      uiGridList.append((irow, icol))
  return uiGridList

# --- Affiche les boutons pour chaque thème dans une grille ---
def displayThemes(themeDict):
  uiClear('Button')
  uiMenuBtn.pack(side=LEFT)
  uiMenuPoints.config(text=' ')
  uiMenuLabel.config(text=' ')
  uiMenubar.pack()
  uiCanvas_themes = Canvas(window)
  uiGridList = uiSetGrid(themeDict)
  i = 0
  for k, v in themeDict.items():
    irow, icol = uiGridList[i]
    uiBtn_theme = Button(uiCanvas_themes, text=v, command=lambda theme=k: setRoundsNb((themeDict, theme))).grid(row=irow, column=icol, sticky='nesw')
    i += 1
  uiCanvas_themes.pack(side=BOTTOM, pady=15)

# --- Menu pour entrer le nombre de tours et choisir l'utilisation ou non du compte à rebours
def setRoundsNb(themeArg):
  # --- Ouverture du fichier ---
  global nl
  global questions_list
  
  flist = []
  nl = 0
  questions_list = []

  themeDict, theme = themeArg

  if theme == "tout_revision":
    # pour chaque fichier, si le fichier est dans themes_revision, ajoute le fichier à flist
    for f in os.listdir("./questions"):
      if f.endswith(".csv") and f[0:len(f)-4] in themes_revision.keys():
        flist.append((open(f'questions/{f}', encoding='utf-8'), f))
  elif theme == "tout_jeu":
    # pour chaque fichier, si le fichier est dans themes_jeu, ajoute le fichier à flist
    for f in os.listdir("./questions"):
      if f.endswith(".csv") and f[0:len(f)-4] in themes_jeu.keys(): 
        flist.append((open(f'questions/{f}', encoding='utf-8'), f))
  else:
    flist.append((open(f'questions/{theme}.csv', encoding='utf-8'), theme+'.csv'))

  for f, fpath in flist:
    nl += len(f.readlines())
    f.seek(0)
    reader = csv.reader(f, delimiter=';')
    for row in reader:
      questions_list.append((row, fpath))

  random.shuffle(questions_list) # Questions dans un ordre aléatoire

  uiClear('Canvas')
  uiTxt_welcome.set(f"Entrez le nombre de tours de la partie\n(entre 1 et {nl}) : ")
  
  Entry(window, width=5, textvariable=tot_q).pack()

  Checkbutton(window, text="Compte à rebours (le temps compte pour le score !)", variable=timerOn, onvalue=1, offvalue=0, command=uiCheckBtnTimer_Click).pack(pady=50)

  Button(window, text="C'est parti !", command=uiBtnRoundsNb_Click).pack(side=BOTTOM, pady=15)

  if timerOn.get() == 1:
    uiCheckBtnTimer_Click()

# Si compte à rebours coché, affiche le choix du temps
def uiCheckBtnTimer_Click():
  global uiEntry_timer
  global uiLabel_timer

  if timerOn.get() == 1:
    uiEntry_timer = Entry(window, width=5, textvariable=timerVal)
    uiLabel_timer = Label(window, text='Entrez le temps du compte à rebours (en secondes) :')
    uiEntry_timer.pack(side=BOTTOM, pady=15)
    uiLabel_timer.pack(side=BOTTOM)
  else:
    uiEntry_timer.pack_forget()
    uiLabel_timer.pack_forget()

# Vérifie que le nombre de tours choisi est cohérent avant de jouer
def uiBtnRoundsNb_Click():
  tot_q_local = tot_q.get()
  if tot_q_local > 0 and tot_q_local <= nl:
    uiClear('')
    play()


# === INITIALISATION DU JEU ! ===
def play():
  global id_q
  global nb_points
  global uiCanvas_image
  global uiCanvas_progress
  global uiProgressbar
  global timerList

  timerList = []
  timerSeconds.set(timerVal.get())

  if timerOn.get() == 1:
    uiCanvas_progress = Canvas(window, height=30)
    uiProgressbar = Progressbar(uiCanvas_progress, length=int(window.winfo_width())-100)
    uiCanvas_progress.pack()
    uiProgressbar.pack(side=LEFT, padx=20)
    Label(uiCanvas_progress, textvariable=timerSeconds, width=15).pack(side=RIGHT, padx=20)
  
  uiCanvas_image = Canvas(window, height=int(window.winfo_height()/3))
  uiCanvas_image.pack(side=TOP, padx=5, pady=5)
  Label(window, textvariable=uiTxt_question, wraplengt=550).pack()

  e = open ('progression.csv', 'w') # Permet d'avoir un fichier avec seulement les scores de cette partie
  e.close()

  nb_points = 0
  uiMenuPoints.config(text='Points : 0')
  writeProgression(0, tot_q.get())
  id_q.set(1)
  createQuestion()


# === À CHAQUE TOUR DE LA PARTIE ===

# Définit l'image de la question
def uiSetImage(image):
  uiSize_img = int(window.winfo_height()/3)
  uiImg = Image.open('images/' + image)
  uiImg_newWidth = int(uiImg.width/uiImg.height*uiSize_img)
  uiImg_resized = uiImg.resize((uiImg_newWidth,uiSize_img), Image.ANTIALIAS)
  uiCanvas_image.image = ImageTk.PhotoImage(uiImg_resized)
  uiCanvas_image.create_image(190, uiSize_img/2, image=uiCanvas_image.image, anchor='center')

# Compte à rebours, si choisi
def countdown(t):
  global timerSeconds
  if isPaused == True or uiProgressbar.winfo_exists() == 0:
    return
  uiProgressbar['value'] -= 0.1
  
  timerSeconds.set(int(t))

  if t > 0:
    window.after(timerVal.get(), countdown, t-timerVal.get()*0.001)
  else:
    QuizAnswer_Click(-1)

# Affiche la question et les réponses proposées
def createQuestion():
  global uiCanvas_reponses
  global uiWaitVar
  global uiTxt_question
  global isPaused
  global timerList

  isPaused = False
  
  if timerOn.get() == 1:
    uiProgressbar['value'] = 100
    countdown(timerVal.get())

  id_q_local = id_q.get()

  row, theme = questions_list[id_q_local-1]

  uiTxt_question.set(row[0])

  if theme == 'informatique.csv':
    font.nametofont("TkDefaultFont").configure(family="Consolas")
    uiMenuLabel.config(text=f'Index {id_q_local-1}/{tot_q.get()-1}') # Easter egg : renvoie l'index de la question en commençant par 0
  else:
    font.nametofont("TkDefaultFont").configure(family="")
    uiMenuLabel.config(text=f'Question {id_q_local}/{tot_q.get()}')

  uiImageRef = ''
  if len(row) > 5:
    uiImageRef = row[5]

  if uiImageRef == '' or uiImageRef == ' ' or uiImageRef == "''":
    uiSetImage(themes_images[theme[0:len(theme)-4]])
  else: uiSetImage(uiImageRef)

  reponses = [row[1], row[2], row[3], row[4]]
  random.shuffle(reponses) # réponses dans un ordre aléatoire

  uiGridList = uiSetGrid(reponses)

  uiCanvas_reponses.destroy()

  uiCanvas_reponses_local = Canvas(window)
  uiCanvas_reponses_local.pack()
  uiCanvas_reponses = uiCanvas_reponses_local

  for i in reponses:
    irow, icol = uiGridList[reponses.index(i)]
    uiBtn_reponse = Button(uiCanvas_reponses, text=i, wraplengt=250, command=lambda id_reponse=i: QuizAnswer_Click(row.index(id_reponse)))
    uiBtn_reponse.grid(row=irow, column=icol, sticky='nesw')

  timerList.append(time.time())


# === L'UTILISATEUR CHOISIT SA RÉPONSE (ou alors le temps est écoulé) ===
def QuizAnswer_Click(i):
  global nb_points
  global id_q
  global tot_q
  global isPaused

  isPaused = True

  id_q_local = id_q.get()

  timerList[id_q_local-1] = time.time() - timerList[id_q_local-1]
  if os.name == 'nt':
        timerList[id_q_local-1] -= timerList[id_q_local-1]/3 # Correcton d'un bug sur Windows où le temps calculé est plus long que la réalité

  line, theme = questions_list[id_q_local-1]

  if i == 1:
    message = ['Vrai', 'Bien joué', 'Super', 'Génial', 'Bravo', 'Juste']
    a = random.choice(message)

    add_points = 1

    if timerOn.get() == 1:
      points_ponderation = timerVal.get()*1.3 - timerList[id_q_local-1]
      add_points = points_ponderation / timerVal.get()
      if add_points < 1:
        b = [", mais attention au temps", ", mais vous n'avez pas répondu assez vite"]
        a += random.choice(b)
      else: add_points = 1

    nb_points += add_points
    uiMenuPoints.config(text=f'Points : {round(nb_points, 1)}')
    output = f'{a} ! Vous gagnez {round(add_points, 1)} point supplémentaire.'
    messagebox.showinfo(title='La Colle', message=output)
  elif i == -1:
    message = ['Le temps est passé !', 'Pas eu le temps ?', 'Trop tard !', 'Le temps est écoulé !']
    a = random.choice(message)
    output = f'{a}\nLa réponse correcte est {line[1]} !'
    messagebox.showerror(title='La Colle', message=output)
  else :
    message = ['Oh non !', 'Elle est où la culture ?', 'Zut !', 'Loupé !', 'Bien tenté !']
    a = random.choice(message)  
    output = f'{a}\nLa réponse correcte est {line[1]} !'
    messagebox.showerror(title='La Colle', message=output)

  tot_q_local = tot_q.get()
  writeProgression(id_q_local, tot_q_local)

  if id_q_local < tot_q_local:
    id_q.set(id_q_local+1)
    createQuestion()
  else:
    endGame()

# Ecrit la progression dans le fichier
def writeProgression(id_q_local, tot_q_local):
  score = nb_points/tot_q_local*100
  g = open ('progression.csv', 'a')
  writer = csv.writer(g, delimiter = ',')
  writer.writerow([id_q_local, score, tot_q_local, nb_points])
  g.close() 


# === FIN DE LA PARTIE ! ===
def endGame():
  global uiMenuLabel
  global uiMenuPoints

  uiClear('')
  uiMenuLabel.config(text=' ')
  uiMenuPoints.config(text=' ')

  score = nb_points/tot_q.get()*100

  timerTot = 0
  for t in timerList:
    timerTot += t

  timeMinSec = str(time.strftime("%M min %S", time.gmtime(int(timerTot))))

  if timeMinSec[0:2] == '00':
    timeMinSec = timeMinSec[len(timeMinSec)-2:]

  Label(window, text=f'La partie est terminée, elle a duré {timeMinSec} secondes !\nVotre score final est de {round(score, 2)} % ({round(nb_points, 1)} points sur {tot_q.get()}).\n{scoreComment(score)}', wraplengt=550).pack(pady=5)
  createGraph()
  Button(window, text='Revenir au menu', command=uiHome_Click).pack()
  
def scoreComment(score) :
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
    return 'Félicitations'

def createGraph():
  h = open ('progression.csv', 'r')
  reader_h = csv.reader(h, delimiter = ',')
  x = []
  y = []
  s = []
  p = []
  for row in reader_h:
    if len(row) == 4:
      x.append(float(row[0]))
      y.append(float(row[1]))
      s.append(float(row[2]))
      p.append(float(row[3]))
  h.close()

  size = (4,2)
  if window.winfo_width() > 800 and window.winfo_height() > 500:
    size = (6,3)
  uiFigure = Figure(figsize=size, facecolor=window['bg'])
  uiSubPlot = uiFigure.add_subplot()
  uiSubPlot.plot(x,y)
  uiSubPlot.set_ylim([0, 100])
  uiSubPlot.set_xlim([0, tot_q.get()])
  uiSubPlot.yaxis.set_major_locator(MultipleLocator(20))
  uiSubPlot.xaxis.set_major_locator(MaxNLocator(integer=True))
  uiSubPlot.set_ylabel("Score (%)")
  #uiSubPlot.set_xlabel("Questions")
  uiSubPlot.patch.set_alpha(0.0)
  uiFigure.tight_layout()
  uiFigure_canvas = FigureCanvasTkAgg(uiFigure, master=window)
  uiFigure_canvas.get_tk_widget().pack()


# --- Bienvenue ! ---
uiClear('')
Welcome()
window.mainloop()
