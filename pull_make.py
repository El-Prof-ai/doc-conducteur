import os
from flask import Flask, request, jsonify
import subprocess
import threading

import logging

app = Flask(__name__)

@app.route('/pull_make', methods=['POST'])
def pull():
    
    try:
       
        #if result.returncode == 0:
            # Si le pull est réussi, lancez la requête différée dans un thread
        threading.Thread(target=delayed_request).start()
        return jsonify({'message': 'Pull successful'}), 200
      
           # return jsonify({'message': 'Pull failed', 'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

def delayed_request():
    # Attendre une minute
    #time.sleep(60)
    # Faire la requête POST à /execute-make-html
     # Exécutez la commande Git pull
    branch = request.json.get('branch', 'main')  # Par défaut, la branche est 'main'
    
    result = subprocess.run(['git', 'pull', 'origin', branch, '--force'], capture_output=True, text=True)

    if result.returncode == 0:
    
        #try:
            #response = requests.post('http://127.0.0.1:5000/execute-make-html')
            #print(f"Request to /execute-make-html responded with: {response.status_code} {response.text}")
            
        try:
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

            
        #except Exception as e:
            #print(f"Failed to make request to /execute-make-html: {str(e)}")

@app.route('/execute-make-html', methods=['POST'])
def execute_make_html():
    # Ajoutez ici le code pour gérer cette requête
    return jsonify({'message': 'execute-make-html endpoint called'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Changer le port ici
