from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/execute-make-html', methods=['POST'])
def execute_make_html():
    branch = request.json.get('branch', 'main')  # Par défaut, la branche est 'main'
    
    pull_result = execute_git_pull(branch)
    if pull_result.status_code != 200:
        return pull_result

    make_result = execute_make()
    return make_result

def execute_git_pull(branch):
    try:
        # Exécutez la commande Git pull
        result = subprocess.run(['git', 'pull', 'origin', branch, '--force'], capture_output=True, text=True)

        if result.returncode == 0:
            return jsonify({'message': 'Pull successful', 'output': result.stdout}), 200
        else:
            return jsonify({'message': 'Pull failed', 'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

def execute_make():
    try:
        # Exécution de la commande './make html' dans le répertoire courant
        result = subprocess.run(['./make', 'html'], 
                                capture_output=True, 
                                text=True, 
                                shell=True)
        
        # Vérification du code de retour
        if result.returncode == 0:
            return jsonify({
                'status': 'success',
                'message': 'Exécution de ./make html réussie',
                'output': result.stdout
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Erreur lors de l\'exécution de ./make html',
                'error': result.stderr
            }), 500
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Une erreur est survenue',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
