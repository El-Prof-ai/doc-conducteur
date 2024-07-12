import os
from flask import Flask, request, jsonify
import subprocess
import threading
import logging
import time

app = Flask(__name__)

@app.route('/pull_make', methods=['POST'])
def pull():
    branch = request.json.get('branch', 'main')  # Par défaut, la branche est 'main'
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Exécutez la commande Git pull
        result = subprocess.run(['git', 'pull', 'origin', branch, '--force'], capture_output=True, text=True, cwd=script_dir, shell=True)

        if result.returncode == 0:
            # Si le pull est réussi, lancez la requête différée dans un thread
            logging.info('Pull successful. Starting make process...')
            threading.Thread(target=make).start()
            return jsonify({'message': 'Pull successful', 'output': result.stdout}), 200
        else:
            logging.error(f'Pull failed: {result.stderr}')
            return jsonify({'message': 'Pull failed', 'error': result.stderr}), 500
    except Exception as e:
        logging.error(f'An error occurred during pull: {str(e)}')
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

def make():
    try:
        # Vérification de la fin du pull en vérifiant le status de git
        status_line = get_git_status()
        while status_line != "Your branch is up to date with 'origin/main'":
            logging.info('Waiting for git pull to complete...')
            time.sleep(3)
            status_line = get_git_status()

        # Obtenir le chemin du répertoire du script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Exécution de la commande 'make.bat html' dans le répertoire du script
        logging.info('Running make.bat html...')
        result = subprocess.run(['make.bat', 'html'], capture_output=True, text=True, cwd=script_dir, shell=True)
        
        # Vérification du code de retour
        if result.returncode == 0:
            logging.info('Exécution de make.bat html réussie: %s', result.stdout)
        else:
            logging.error('Erreur lors de l\'exécution de make.bat html: %s', result.stdout)
        
    except Exception as e:
        logging.error('Une erreur est survenue: %s', str(e))

def get_git_status():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Exécute la commande `git status`
    result = subprocess.run(['git', 'status'], capture_output=True, text=True, cwd=script_dir, shell=True)
    
    # Vérifie si la commande s'est exécutée avec succès
    if result.returncode != 0:
        logging.error(f"Erreur lors de l'exécution de git status: {result.stderr}")
        return "None"
    
    # Parcourt chaque ligne de la sortie pour trouver celle qui nous intéresse
    for line in result.stdout.split('\n'):
        if 'Your branch is up to date with' in line:
            return line.strip()
    
    return "None"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, port=8000)  # Changer le port ici
