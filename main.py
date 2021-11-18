import csv
import random

# --- Fonction : Évalue la réponse ---
def bot_answer(user_input): # Evalue la réponse
  global nb_points 
  global current_row
  if user_input.lower() == current_row[1].lower() :
    nb_points += 1
    message = ['Vrai', 'Bien joué', 'Super', 'Génial', 'Bravo', 'Juste']
    a = random.choice(message) 
    g = (f'{a} ! Vous avez {nb_points} points !')
  else :
    message = ['Oh non !', 'Elle est où la culture ?', 'Zut !', 'Loupé !', 'Bien tenté !']
    a = random.choice(message)
    g = f'{a}\nLa réponse correcte est {current_row[1]} !'
  return g


# --- Ouverture du fichier ---
f = open('questions.csv', encoding='utf-8')

nl = len(f.readlines())
f.seek(0)

reader = csv.reader(f, delimiter=',')

# --- Choix du nombre de questions en début de partie ---
repeat = True
while repeat == True:
  nb_q = int(input("Entrez le nombre de tours de la partie : "))
  if nb_q > nl: # S'il n'y a pas assez de questions dans le csv, redemande d'entrer un autre nombre
    print("Il n'y a pas assez de questions disponibles !")
    repeat = True
  else: repeat = False

# --- Alterne entre question du bot, entrée de l'utilisateur et réponse du bot ---
nb_points = 0

for q in range(1, nb_q+1):
  rand_nb = random.randint(0, nl-1)
  current_row = []
  for i, row in enumerate(reader):
    if i == rand_nb:
      current_row = row
  
  print (f'Question {q}/{nb_q}\n')
  print(f"{current_row[0]}\n{current_row[1]}\t{current_row[2]}\t{current_row[3]}\t{current_row[4]}\n")    
  user_input = str(input("Votre réponse : "))
  print(f'\nJean-Pierre Foucault ==> {bot_answer(user_input)} \n')
  f.seek(0)

# --- Fin de la partie ---
print (f'La partie est terminée !\nVotre score final est de {nb_points} points.')
