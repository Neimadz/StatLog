import os
import subprocess

def create_folders():
    # Obtenir le chemin absolu du répertoire contenant main.exe
    exe_dir = os.path.dirname(sys.executable)
    
    # Créer un dossier pour les images s'il n'existe pas déjà
    images_folder = os.path.join(exe_dir, 'images')
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
        print(f"Dossier 'images' créé avec succès à l'emplacement : {images_folder}")
    
    # Créer un dossier pour les fichiers journaux s'il n'existe pas déjà
    logs_folder = os.path.join(exe_dir, 'logs')
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
        print(f"Dossier 'logs' créé avec succès à l'emplacement : {logs_folder}")
def main():
    create_folders()  # Créer les dossiers nécessaires
    
    # Demander le premier pseudo
    pseudo = input("Veuillez entrer votre pseudo : ")
    pseudos = [pseudo] if pseudo else []
    
    # Demander les pseudos supplémentaires
    while True:
        another_pseudo = input("Voulez-vous ajouter un autre pseudo ? (O/N) : ")
        if another_pseudo.upper() == 'O':
            pseudo = input("Veuillez entrer un autre pseudo : ")
            if pseudo:
                pseudos.append(pseudo)
            else:
                print("Pseudo vide, veuillez entrer un pseudo valide.")
        elif another_pseudo.upper() != 'N':
            print("Réponse invalide. Veuillez répondre avec 'O' pour oui ou 'N' pour non.")
        else:
            break
    
    # Continuer le script avec la liste des pseudos
    print("Liste des pseudos enregistrés :", pseudos)
    
    # Exécuter le script avec les pseudos
    print("Veuillez placer vos fichiers .log (Builds_Windows\CombatLogs) dans le dossier 'logs'.")
    input("Appuyez sur Entrée une fois que vous avez placé vos fichiers .log.")
    print("Lancement du script...")
    subprocess.run(["python", "script.py"] + pseudos, check=True)
    print("Script terminé.")

if __name__ == "__main__":
    main()
