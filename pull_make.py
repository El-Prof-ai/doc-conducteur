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
        time.sleep(40)
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
        if result.returncode == 0:
            logging.info('Exécution de make.bat html réussie: %s', result.stdout)
        else:
            logging.error('Erreur lors de l\'exécution de make.bat html: %s', result.stdout)
        
    except Exception as e:
        logging.error('Une erreur est survenue: %s', str(e))

#fdf


if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Changer le port ici
