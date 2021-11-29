import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


themes_jeu = {
  'A' : 'culture',
  'B' : 'suisse',
  'C' : 'histoire',
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

  
# --- Effaçage du contenu du fichier progression ---
e = open ('progression.csv', 'w') # Permet d'avoir un fichier avec seulement les scores de cette partie
e.close()                         

# --- Accueil dans le quiz ---
print ('Bienvenue dans le quiz : La Colle', '\U0001F9D0\n\nPrêt.e à répondre aux questions ?\n ')


# --- Boucle qui permet la partie, une fois terminée, d'être recommencée ---
retry = True 
nb_partie = 1
while retry == True :
  
# --- Choix du type de partie ---
  type = input ('\nQue voulez-vous faire ?\nA | Jouer\tB | Réviser\n\n')
  

# --- Choix du thème en début de partie ---
  if type == 'a' :
    print ('\nThèmes :\nA | Culture\tB | Suisse\tC | Histoire\n')
    c = input('Quel thème voulez-vous étudier ? ') 
  else :
    print ('\nThèmes :\nA | Géologie\tB | Ecologie\tC | Equations différentielles\nD | Génétique\tE | Hydrologie\tF | Chimie organique \nG | Pédologie  \tH | Informatique\n')
    c = input('Quel thème voulez-vous étudier ? ')


# --- Ouverture du fichier ---
  f = open(f'{theme(c)}.csv', encoding='utf-8')

  nl = len(f.readlines())
  f.seek(0)

  reader = csv.reader(f, delimiter=',')

  questions_list = [] # Permet d'éviter la répétition des questions
  for row in reader:
    questions_list.append(row)
  random.shuffle(questions_list)

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
    print(f'\nJean-Pierre Foucault ==> {bot_answer(user_input, row)} \n')
    f.seek(0)


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
  plt.plot(x,y)
  plt.show ()
  print (f'Vous avez obtenu {sum(p)} points sur {sum(s)}.\n'f'La moyenne est de {round(sum(p)/sum(s)*100,2)}%\n')
  print ('\nLe quiz est terminé ! A bientôt !')  
else :
  print ('\nLe quiz est terminé ! A bientôt !')
    
