import csv
import random
#import IPython.display as display
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

themes = {
  'A' : 'culture',
  'B' : 'suisse',
  'C' : 'histoire',
  'D' : 'chimie_orga',
  'E' : 'écologie',
  'F' : 'equadiffs',
  'G' : 'genetique',
  'H' : 'hydrologie',  
  'I' : 'informatique',
  'J' : 'pedologie',
  'K' : 'géologie'
}

#from IPython.display import Image
#Image('pyrite.jpeg')


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

def theme (c) :
  choix = ""
  for key, value in themes.items() :
    if c.upper() == key :
      choix = value
  return choix

# --- Boucle qui permet la partie, une fois terminée, d'être recommencée ---
retry = True 
while retry == True :

# --- Choix du thème en début de partie ---
  print ('Thèmes :\nA | Culture\tB | Suisse\tC | Histoire\tD | Chimie organique\nE | Ecologie\tF | Equations différentielles\tG | Génétique\tH | Hydrologie\nI | Informatique\tJ | Pédologie  \tK | Géologie\n')
  c = input('Quel thème voulez-vous étudier ? ') 

# --- Ouverture du fichier ---
  f = open(f'{theme(c)}.csv', encoding='utf-8')

  nl = len(f.readlines())
  f.seek(0)

  reader = csv.reader(f, delimiter=',')

  questions_list = []
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
    a = reponses[0] # Peut-être que le code peut être optimisé
    b = reponses[1] # Il permet de mettre comme réponse a ou b ou c ou d
    c = reponses[2]
    d = reponses[3]
    
    #if row[5] == 'p':                      Faire apparaître une photo
      #img = mpimg.imread(f'row[6].jpeg')
      #imgplot = plt.imshow(img)
      #plt.show()

    print(f"{row[0]}\nA | {a}\tB | {b}\tC | {c}\tD | {d}\n")    
    user_input = str(input("Votre réponse : "))
    print(f'\nJean-Pierre Foucault ==> {bot_answer(user_input, row)} \n')
    f.seek(0)

# --- Fin de la partie ---
  print (f'La partie est terminée !\nVotre score final est de {int(nb_points/tot_q*100)} % ({nb_points} points sur {tot_q}).\n')
  recommence = str(input('Voulez-vous recommencer ? '))
  if recommence.lower() == 'oui' or recommence.lower() == 'yes' or recommence.lower() == 'o' or recommence.lower() == 'y' :
    retry = True
  else :
    print ('\nLe quiz est terminé ! A bientôt !')
    retry = False