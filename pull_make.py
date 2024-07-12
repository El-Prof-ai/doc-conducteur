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
        # Exécutez la commande Git pull
        result = subprocess.run(['git', 'pull', 'origin', branch, '--force'], capture_output=True, text=True)

        if result.returncode == 0:
            # Si le pull est réussi, lancez la requête différée dans un thread
            threading.Thread(target=make).start()
            print('REPONDRE')
            return jsonify({'message': 'Pull successful', 'output': result.stdout}), 200
        else:
            return jsonify({'message': 'Pull failed', 'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

def make():
    
    try:
        print('make()')
        status_line = get_git_status()
        while(status_line != 'Your branch is up to date with'):
            time.sleep(3)
            status_line = get_git_status()
        print('start make()........')
        # Obtenir le chemin du répertoire du script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Exécution de la commande 'make.bat html' dans le répertoire du script
        result = subprocess.run(['make.bat', 'html'], 
                                capture_output=True, 
                                text=True, 
                                cwd=script_dir,
                                shell=True)
        
        # Vérification du code de retour
        print('end make()........')
        if result.returncode == 0:
            logging.info('Exécution de make.bat html réussie: %s', result.stdout)
        else:
            logging.error('Erreur lors de l\'exécution de make.bat html: %s', result.stdout)
        
    except Exception as e:
        logging.error('Une erreur est survenue: %s', str(e))

def get_git_status():
    # Exécute la commande `git status`
    result = subprocess.run(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Vérifie si la commande s'est exécutée avec succès
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution de git status: {result.stderr}")
        return 'None'
    
    # Parcourt chaque ligne de la sortie pour trouver celle qui nous intéresse
    for line in result.stdout.split('\n'):
        if 'Your branch is up to date with' in line:
            return 'Your branch is up to date with'
    
    return 'None'

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Changer le port ici
