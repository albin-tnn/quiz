import os
import csv
import random
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from matplotlib.figure import Figure
from matplotlib.pyplot import *
from math import sqrt
from tkinter import *
import tkinter.font as font
from PIL import ImageTk,Image

themes_jeu = {
  'culture' : 'Culture',
  'suisse' : 'Suisse',
  'histoire' : 'Histoire',
  'musique' : 'Musique',
  'citations' : 'Citations',
  'tout_jeu' : 'Tous'
}

themes_jeu2 = ['culture','suisse','histoire','musique','citation','tout_jeu']
theme_revision2 = ['géologie','écologie','equadiffs','genetique','hydrologie','chimie_orga','pedologie','informatique','tout_revision']

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

# Toutes les variables et fonctions liées à l'interface Tkinter sont préfixées "ui"

window = Tk()
window.title('La Colle')
window.geometry('600x300')

uiMenuEmpty = Menu(window)
uiMenuEmpty.add_command(label=' ')

uiTxt_welcome = StringVar()
uiTxt_question = StringVar()
uiCanvas_reponses = Canvas(window)

questions_list = []
nb_points = 0
nl = 1
id_q = IntVar()
tot_q = IntVar()

uiCanvas_image = Canvas(window, height=120)

def uiClear(type):
  list = window.pack_slaves()
  if type == '':
    for i in list:
      i.destroy()
  else:
    for i in list:
      if i.winfo_class() == type:
        i.destroy()
  font.nametofont("TkDefaultFont").configure(family="")

def uiHome_Click():
  uiClear('')
  Welcome()

# --- Fonction : Accueil dans le quiz ---
def Welcome():
  window.config(menu=uiMenuEmpty)

  uiTxt_welcome.set('Bienvenue dans le quiz : La Colle  \U0001F9D0\n\nPrêt.e à répondre aux questions ?\n\nQue voulez-vous faire ?\n')

  uiLabel_welcome = Label(window, textvariable=uiTxt_welcome)
  uiLabel_welcome.pack(side=TOP, pady=15)

  uiBtnPlay = Button(window, text ='Jouer', command=uiBtnPlay_Click).pack(side=LEFT, padx=15, pady=5)
  uiBtnRevise = Button(window, text ='Réviser', command=uiBtnRevise_Click).pack(side=RIGHT, padx=15, pady=5)

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
    return 'Félicitations \U0001F973 \U0001F973 \U0001F973'

def createGraph():
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

  uiFigure = Figure(figsize=(4,2), facecolor=window['bg'])
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

def endGame():
  uiClear('')
  window.config(menu=uiMenuEmpty)

  score = nb_points/tot_q.get()*100
  Label(window, text=f'La partie est terminée !\nVotre score final est de {round(score, 2)} % ({nb_points} points sur {tot_q.get()}).\n{scoreComment(score)}', wraplengt=550).pack(pady=5)
  createGraph()
  Button(window, text='Revenir au menu', command=uiHome_Click).pack()



def uiSetImage(image):
  uiImg = Image.open('images/' + image)
  uiImg_newWidth = int(uiImg.width/uiImg.height*120)
  uiImg_resized = uiImg.resize((uiImg_newWidth,120), Image.ANTIALIAS)
  uiCanvas_image.image = ImageTk.PhotoImage(uiImg_resized)
  uiCanvas_image.create_image(190, 60, image=uiCanvas_image.image, anchor='center')

def create_question():
  global uiCanvas_reponses
  global uiWaitVar
  global uiTxt_question

  id_q_local = id_q.get()
  print(id_q_local)

  row, theme = questions_list[id_q_local-1]

  uiTxt_question.set(row[0])

  if theme == 'informatique.csv':
    font.nametofont("TkDefaultFont").configure(family="Consolas")
    uiMenubar.entryconfigure(3, label=f'Index {id_q_local-1}/{tot_q.get()-1}') # Easter egg : renvoie l'index de la question en commençant par 0
  else:
    font.nametofont("TkDefaultFont").configure(family="")
    uiMenubar.entryconfigure(3, label=f'Question {id_q_local}/{tot_q.get()}')

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
    print((row.index(i), reponses.index(i)))
    irow, icol = uiGridList[reponses.index(i)]
    uiBtn_reponse = Button(uiCanvas_reponses, text=i, wraplengt=250, command=lambda id_reponse=i: QuizAnswer_Click(row.index(id_reponse)))
    uiBtn_reponse.grid(row=irow, column=icol, sticky='nesw')

def writeProgression(id_q_local, tot_q_local):
  score = nb_points/tot_q_local*100
  g = open ('progression.csv', 'a')
  writer = csv.writer(g, delimiter = ',')
  writer.writerow([id_q_local, score, tot_q_local, nb_points])
  g.close()

def QuizAnswer_Click(i):
  global nb_points
  global id_q
  global tot_q

  id_q_local = id_q.get()

  line, theme = questions_list[id_q_local-1]
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
 
  tot_q_local = tot_q.get()
  writeProgression(id_q_local, tot_q_local)

  if id_q_local < tot_q_local:
    id_q.set(id_q_local+1)
    create_question()
  else:
    endGame()


def play():
  global id_q
  global nb_points
  global uiCanvas_image
  
  uiCanvas_image = Canvas(window, height=120)
  uiCanvas_image.pack(side=TOP, padx=5, pady=5)
  Label(window, textvariable=uiTxt_question, wraplengt=550).pack()

  e = open ('progression.csv', 'w') # Permet d'avoir un fichier avec seulement les scores de cette partie
  e.close()

  nb_points = 0
  uiMenubar.entryconfigure(4, label='Points : 0')
  writeProgression(0, tot_q.get())
  id_q.set(1)
  create_question()


def uiBtnRoundsNb_Click():
  tot_q_local = tot_q.get()
  if tot_q_local > 0 and tot_q_local <= nl:
    uiClear('')
    play()


def SetRoundsNb(themeArg):
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
    print((theme, nl))
    reader = csv.reader(f, delimiter=';')
    for row in reader:
      questions_list.append((row, fpath))

  random.shuffle(questions_list) # Questions dans un ordre aléatoire

  uiClear('Canvas')
  uiTxt_welcome.set(f"Entrez le nombre de tours de la partie\n(entre 1 et {nl}) : ")

  Entry(window, width = 5, textvariable = tot_q).pack()
  Button(window, text="C'est parti !", command=uiBtnRoundsNb_Click).pack(pady=15)


def uiSetGrid(themeDict):
  uiGridList = []
  # gridSize = int(sqrt(len(themeDict)) + 0.5) # si grille carrée
  gridSize = int(len(themeDict)/2 + 0.5) # si grille à 2 colonnes
  for irow in range(1, gridSize+1):
    for icol in range(1, 3):
      uiGridList.append((irow, icol))
  return uiGridList


def DisplayThemes(themeDict):
  uiClear('Button')
  uiCanvas_themes = Canvas(window)
  uiGridList = uiSetGrid(themeDict)
  i = 0
  for k, v in themeDict.items():
    print(v)
    irow, icol = uiGridList[i]
    uiBtn_theme = Button(uiCanvas_themes, text=v, command=lambda theme=k: SetRoundsNb((themeDict, theme))).grid(row=irow, column=icol, sticky='nesw')
    i += 1
  uiCanvas_themes.pack(side=BOTTOM, pady=15)
  uiMenubar.entryconfigure(3, label=' ')
  uiMenubar.entryconfigure(4, label=' ')
  window.config(menu=uiMenubar)

def uiBtnPlay_Click():
  uiTxt_welcome.set('Sur quel thème voulez-vous jouer ?')
  DisplayThemes(themes_jeu)
  
def uiBtnRevise_Click():
  uiTxt_welcome.set('Quel thème voulez-vous réviser ?')
  DisplayThemes(themes_revision)  


# --- Bienvenue ! ---
uiMenubar = Menu(window)
uiMenu1 = Menu(uiMenubar, tearoff=0)
uiMenubar.add_command(label="Retour", command=uiHome_Click)
uiMenubar.add_command(label='           ')
uiMenubar.add_command(label=' ')
uiMenubar.add_command(label=' ')


uiClear('')
Welcome()
window.mainloop()