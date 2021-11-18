import csv
import random

def bot_answer(user_input): # Evalue la réponse
  nb_points = 0
  global current_row
  if user_input == current_row[1] :
    nb_points += 1
    message = ['Vrai', 'Bien joué', 'Super', 'Génial', 'Bravo', 'Juste']
    a = random.choice(message)
    return f'{a} ! Vous avez {nb_points} points !'
  else :
    message = ['Oh non !', 'Elle est où la culture ?', 'Zut !', 'Loupé !', 'Bien tenté !']
    a = random.choice(message)
    return f'{a}\nLa réponse correcte est {current_row[1]} !'

f = open('questions.csv', encoding='utf-8')

nl = len(f.readlines())
f.seek(0)

reader = csv.reader(f, delimiter=',')

while True: # Alterne entre entrée de l'utilisateur et réponse du bot
  rand_nb = random.randint(0, nl)
  current_row = []
  for i, row in enumerate(reader):
    if i == rand_nb:
      current_row = row
  
  print(f"{current_row[0]}\n{current_row[1]}\t{current_row[2]}\t{current_row[3]}\t{current_row[4]}\n")    
# peut être que faut relire le fichier depuis le début ? 
  user_input = str(input("Votre réponse : "))
  print(f'\nJean-Pierre Foucault ==> {bot_answer(user_input)} \n')
  

 