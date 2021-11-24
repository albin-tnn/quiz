import csv
import random


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
  'k' : 'géologie'
}


# --- Fonction : Évalue la réponse ---
def bot_answer(user_input):
  global nb_points 
  global current_row
  global reponses
  global liste
  answer = liste.index(user_input.lower())
  answer_2 = reponses[answer]
  if answer_2 == current_row[1] :
    nb_points += 1
    message = ['Vrai', 'Bien joué', 'Super', 'Génial', 'Bravo', 'Juste']
    a = random.choice(message) 
    g = (f'{a} ! Vous avez {nb_points} points !')
  else :
    message = ['Oh non !', 'Elle est où la culture ?', 'Zut !', 'Loupé !', 'Bien tenté !']
    a = random.choice(message)
    g = f'{a}\nLa réponse correcte est {current_row[1]} !'
  return g


# --- Boucle qui permet la partie, une fois terminée, d'être recommencée ---
retry = True 
while retry == True :

# --- Choix du thème en début de partie ---
  print ('Thèmes :\nA | Culture\tB | Suisse\tC | Histoire\tD | Chimie organique\nE | Ecologie\tF | Equations différentielles\tG | Génétique\tH | Hydrologie\nI | Informatique\tJ | Pédologie  \tK | Géologie\n')
  c = input('Quel thème voulez-vous étudier ? ') 
  def theme (c) :
    for key, value in themes.items() :
      if c.upper() in key :
        choix = value
    return choix


# --- Ouverture du fichier ---
  f = open(f'{theme(c)}.csv', encoding='utf-8')

  nl = len(f.readlines())
  f.seek(0)

  reader = csv.reader(f, delimiter=',')


# --- Choix du nombre de questions en début de partie ---
  repeat = True
  while repeat == True:
    nb_q = int(input("Entrez le nombre de tours de la partie : "))
    if nb_q > nl: # S'il n'y a pas assez de questions dans le csv, redemande d'entrer un autre nombre
      print(f"Il n'y a pas assez de questions disponibles ! Le nombre doit être compris entre 1 et {nl}.")
      repeat = True
    elif nb_q < 1:
      print(f"Le nombre doit être compris entre 1 et {nl}.")
    else: repeat = False

# --- Alterne entre question du bot, entrée de l'utilisateur et réponse du bot ---
  nb_points = 0

  for q in range(1, nb_q+1):
    rand_nb = random.randint(0, nl-1)
    current_row = []
    for i, row in enumerate(reader):
      if i == rand_nb:
        current_row = row
  
    print (f'\nQuestion {q}/{nb_q}\n')
    reponses = [current_row[1], current_row[2], current_row[3], current_row[4]]
    reponses.sort() # réponses dans un ordre aléatoire
    a = reponses[0] # Peut-être que le code peut être optimisé
    b = reponses[1] # Il permet de mettre comme réponse a ou b ou c ou d
    c = reponses[2]
    d = reponses[3]
    liste = ['a', 'b', 'c', 'd']
    print(f"{current_row[0]}\nA | {a}\tB | {b}\tC | {c}\tD | {d}\n")    
    user_input = str(input("Votre réponse : "))
    print(f'\nJean-Pierre Foucault ==> {bot_answer(user_input)} \n')
    f.seek(0)

# --- Fin de la partie ---
  print (f'La partie est terminée !\nVotre score final est de {nb_points} points.\n')
  recommence = str(input('Voulez-vous recommencer ? '))
  if recommence.lower() == 'oui' :
    retry = True
  else :
    print ('\nLe quiz est terminé ! A bientôt !')
    retry = False