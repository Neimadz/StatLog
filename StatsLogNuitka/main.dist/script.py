import os
import pandas as pd
import re
import sys
import matplotlib.pyplot as plt
import datetime  

# Obtenez le chemin absolu du répertoire contenant le script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Chemin pour le dossier images
images_folder = os.path.join(script_dir, 'images')

# Créer le dossier images s'il n'existe pas déjà
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# Récupérer le pseudo passé en argument en ligne de commande
if len(sys.argv) < 2:
    print("Usage: python script.py <pseudo>")
    sys.exit(1)
user_names = [sys.argv[1]]

# Fonction pour extraire les données pertinentes d'un fichier journal
def extract_game_info(log_file):
    game_info = {'Nom de mon leader': None, 'Nom de l\'adversaire': None, 'Personnage leader de l\'adversaire': None,
                 'Choix second ou first': None, 'Win': False, 'Loose': False}
    with open(log_file, 'r') as file:
        for line in file:
            match_leader = re.search(r'\[(.*?)\] Leader is ([^\[]+) \[([^>]+)', line)
            match_choice = re.search(r'\[([^\]]+)\] Chose to go (First|Second)', line)
            match_result = re.search(r'\[([^\]]+)\] (Loses|Wins|Concedes|Opponent Has Disconnected)!', line)
            if match_leader:
                username = match_leader.group(1)
                game_info['Nom de mon leader' if username in user_names else 'Nom de l\'adversaire'] = match_leader.group(1)
                game_info['Personnage leader de l\'adversaire'] = match_leader.group(2) + ' ' + match_leader.group(3)
            elif match_choice:
                username = match_choice.group(1)
                choice = match_choice.group(2)
                game_info['Choix second ou first'] = f"{username} Chose to go {choice}"
            elif match_result:
                username = match_result.group(1)
                result = match_result.group(2)
                if username in user_names:
                    game_info['Win'] = (result == 'Wins' or result == 'Opponent Has Disconnected' or result == 'Concedes')
                    game_info['Loose'] = (result == 'Loses')
                else:
                    game_info['Win'] = (result == 'Concedes')
                    game_info['Loose'] = (result == 'Wins')
                    
    return game_info

# Liste pour stocker les informations sur les parties
all_game_info = []

# Parcours de tous les fichiers dans le dossier logs
logs_folder = os.path.join(script_dir, 'logs')
for filename in os.listdir(logs_folder):
    if filename.endswith('.log'):
        log_file = os.path.join(logs_folder, filename)
        game_info = extract_game_info(log_file)
        all_game_info.append(game_info)

# Créer un DataFrame Pandas
df = pd.DataFrame(all_game_info)

# Filtrer les données pour les parties remportées par le pseudo entré
df_wins = df[(df['Win']) & ((df['Nom de mon leader'].isin(user_names)) | (df['Nom de l\'adversaire'].isin(user_names)))]

# Compter le nombre de victoires par personnage leader de l'adversaire
win_counts = df_wins['Personnage leader de l\'adversaire'].value_counts()

# Créer un camembert pour afficher le pourcentage de victoires par personnage leader de l'adversaire
plt.figure(figsize=(8, 6))
plt.title('Pourcentage de victoires par personnage leader de l\'adversaire\n')
plt.pie(win_counts, labels=win_counts.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')

# Enregistrer le camembert en image avec l'heure actuelle dans le nom de fichier
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
pie_chart_filename = os.path.join(images_folder, f"pie_chart_{current_time}.png")
plt.savefig(pie_chart_filename)

# Filtrer les données pour les parties remportées par le pseudo entré
df_wins = df[(df['Win']) & ((df['Nom de mon leader'].isin(user_names)) | (df['Nom de l\'adversaire'].isin(user_names)))]

# Filtrer les données pour les parties perdues par le pseudo entré
df_losses = df[(df['Loose']) & ((df['Nom de mon leader'].isin(user_names)) | (df['Nom de l\'adversaire'].isin(user_names)))]

# Grouper les données par le personnage leader de l'adversaire et compter le nombre de victoires et de défaites
win_counts = df_wins.groupby('Personnage leader de l\'adversaire').size()
loss_counts = df_losses.groupby('Personnage leader de l\'adversaire').size()

# Récupérer les noms des personnages leader de l'adversaire
characters = set(win_counts.index) | set(loss_counts.index)

# Créer une liste contenant le nombre de victoires et de défaites pour chaque personnage
data = [(win_counts.get(character, 0), loss_counts.get(character, 0)) for character in characters]

# Créer un diagramme en barres pour afficher le nombre de victoires et de défaites par personnage leader de l'adversaire
fig, ax = plt.subplots(figsize=(12, 8))
bar_width = 0.35
index = range(len(data))
bars1 = ax.bar(index, [item[0] for item in data], bar_width, label='Victoires', color='green')
bars2 = ax.bar(index, [item[1] for item in data], bar_width, bottom=[item[0] for item in data], label='Défaites', color='red')

# Ajouter les étiquettes des données aux barres
for i, (win, loss) in enumerate(data):
    total = win + loss
    if total != 0:
        win_percentage = win / total * 100
        loss_percentage = loss / total * 100
        ax.text(index[i], win + loss, f'{win} - {loss}\n{win_percentage:.1f}%', ha='center', va='center', color='black')

ax.set_title('Nombre de victoires et de défaites contre leader adverse')
ax.set_ylabel('Nombre de parties')
ax.set_xticks(index)
ax.set_xticklabels([character for character in characters], rotation=45)
ax.legend()

# Enregistrer l'histogramme en image avec l'heure actuelle dans le nom de fichier
histogram_filename = os.path.join(images_folder, f"histogram_{current_time}.png")
plt.savefig(histogram_filename)

# Enregistrer les données dans un fichier CSV
csv_filename = os.path.join(script_dir, 'data.csv')
df.to_csv(csv_filename, index=False)

print('Fin du script les résultat seront dans le dossier images')
