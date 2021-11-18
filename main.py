import csv
import random

nb_points = 0

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

f = open('questions.csv', encoding='utf-8')

nl = len(f.readlines())
f.seek(0)

reader = csv.reader(f, delimiter=',')

q = 0 
while q < 3 : # Alterne entre question du bot, entrée de l'utilisateur et réponse du bot
  q +=1       # Limite le nombre de questions à trois
  rand_nb = random.randint(0, nl-1)
  current_row = []
  for i, row in enumerate(reader):
    if i == rand_nb:
      current_row = row
  
  print (f'Question {q}/3\n')
  print(f"{current_row[0]}\n{current_row[1]}\t{current_row[2]}\t{current_row[3]}\t{current_row[4]}\n")    
# peut être que faut relire le fichier depuis le début ? # bien vu haha # C'est Rémi (l'assistant) qui a remarqué :) 
  user_input = str(input("Votre réponse : "))
  print(f'\nJean-Pierre Foucault ==> {bot_answer(user_input)} \n')
  f.seek(0)

print (f'La partie est terminée !\nVotre score final est de {nb_points} points !')

