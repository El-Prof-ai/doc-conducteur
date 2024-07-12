from flask import Flask, request, jsonify
import subprocess
import threading
import time
import requests

app = Flask(__name__)

@app.route('/pull', methods=['POST'])
def pull():
    branch = request.json.get('branch', 'main')  # Par défaut, la branche est 'main'
    
    try:
        # Exécutez la commande Git pull
        result = subprocess.run(['git', 'pull', 'origin', branch, '--force'], capture_output=True, text=True)

        if result.returncode == 0:
            # Si le pull est réussi, lancez la requête différée dans un thread
            threading.Thread(target=delayed_request).start()
            return jsonify({'message': 'Pull successful', 'output': result.stdout}), 200
        else:
            return jsonify({'message': 'Pull failed', 'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

def delayed_request():
    # Attendre une minute
    time.sleep(60)
    # Faire la requête POST à /execute-make-html
    try:
        response = requests.post('http://127.0.0.1:5000/execute-make-html')
        print(f"Request to /execute-make-html responded with: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Failed to make request to /execute-make-html: {str(e)}")

@app.route('/execute-make-html', methods=['POST'])
def execute_make_html():
    # Ajoutez ici le code pour gérer cette requête
    return jsonify({'message': 'execute-make-html endpoint called'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Changer le port ici
