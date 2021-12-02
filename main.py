import os
import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from tkinter import *
from PIL import ImageTk,Image

nl = 1

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
window.geometry('400x250')

uiTxt_welcome = StringVar()
uiTxt_question = StringVar()
uiCanvas_reponses = Canvas(window)

questions_list = []
nb_points = 0
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

def uiHome_Click():
  uiClear('')
  Welcome()

# --- Fonction : Accueil dans le quiz ---
def Welcome():
  uiMenuEmpty = Menu(window)
  uiMenuEmpty.add_command(label=' ')
  window.config(menu=uiMenuEmpty)


  uiTxt_welcome.set('Bienvenue dans le quiz : La Colle  \U0001F9D0\n\nPrêt.e à répondre aux questions ?\n\nQue voulez-vous faire ?\n')

  uiLabel_welcome = Label(window, textvariable=uiTxt_welcome)
  uiLabel_welcome.pack(side=TOP, pady=15)

  uiBtnPlay = Button(window, text ='Jouer', command=uiBtnPlay_Click).pack(side=LEFT, padx=15, pady=5)
  uiBtnRevise = Button(window, text ='Réviser', command=uiBtnRevise_Click).pack(side=RIGHT, padx=15, pady=5)

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

  uiMenubar.entryconfigure(3,uiMenubar.entryconfigure(3, label=f'Question {id_q_local}/{tot_q.get()}'))

  uiImageRef = row[5]

  if uiImageRef == '':
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
    uiBtn_reponse = Button(uiCanvas_reponses, text=i, command=lambda id_reponse=i: QuizAnswer_Click(row.index(id_reponse)))
    uiBtn_reponse.grid(row=irow, column=icol, sticky='nesw')
    
  # uiCanvas_reponses.pack()
  

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

  if id_q_local < tot_q.get():
    id_q.set(id_q_local+1)
    create_question()


def play():
  global id_q
  global nb_points
  global uiCanvas_image
  
  uiCanvas_image = Canvas(window, height=120)
  uiCanvas_image.pack(side=TOP, padx=5, pady=5)
  Label(window, textvariable=uiTxt_question, wraplengt=380).pack()

  nb_points = 0
  uiMenubar.entryconfigure(4, label='Points : 0')
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
  questions_list = [] # Permet d'éviter la répétition des questions

  themeDict, theme = themeArg

  if theme == "tout_revision":
    for f in os.listdir("./questions"):
      if f.endswith(".csv") and f[0:len(f)-4] in themes_revision.keys():
        flist.append((open(f'questions/{f}', encoding='utf-8'), f))
    # pour chaque fichier, si le fichier est dans themes_revision, ajoute le fichier à flist
  elif theme == "tout_jeu":
    for f in os.listdir("./questions"):
      if f.endswith(".csv") and f[0:len(f)-4] in themes_jeu.keys():
        flist.append((open(f'questions/{f}', encoding='utf-8'), f))
    # pour chaque fichier, si le fichier est dans themes_jeu, ajoute le fichier à flist
  else:
    flist.append((open(f'questions/{theme}.csv', encoding='utf-8'), theme+'.csv'))

  for f, fpath in flist:
    nl += len(f.readlines())
    f.seek(0)
    print((theme, nl))
    reader = csv.reader(f, delimiter=';')
    for row in reader:
      questions_list.append((row, fpath))

  random.shuffle(questions_list)

  uiClear('Canvas')
  uiTxt_welcome.set(f"Entrez le nombre de tours de la partie\n(entre 1 et {nl}) : ")

  Entry(window, width = 5, textvariable = tot_q).pack()
  Button(window, text="C'est parti !", command=uiBtnRoundsNb_Click).pack(pady=15)


def uiSetGrid(themeDict):
  uiGridList = []
  # gridSize = int(sqrt(len(themeDict)) + 0.5) # grille carrée
  gridSize = int(len(themeDict)/2 + 0.5) # grille à 2 colonnes
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