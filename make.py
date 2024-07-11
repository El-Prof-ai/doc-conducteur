from flask import Flask, request, jsonify
import subprocess
import os
import platform

app = Flask(__name__)

@app.route('/execute-make-html', methods=['POST'])
def execute_make_html():
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type. Expected application/json"}), 415
    
    data = request.get_json()
    branch = data.get('branch', 'main')  # Par défaut, la branche est 'main'
    
    pull_result, pull_status_code = execute_git_pull(branch)
    if pull_status_code != 200:
        return pull_result, pull_status_code

    make_result, make_status_code = execute_make()
    return make_result, make_status_code

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
        # Chemin du répertoire où se trouve le script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Détermine le système d'exploitation
        is_windows = platform.system() == 'Windows'

        # Commande pour Unix
        command = ['./make', 'html']

        # Exécution de la commande dans le bon répertoire
        result = subprocess.run(command, capture_output=True, text=True, cwd=script_dir, shell=is_windows)

        # Vérification du code de retour
        if result.returncode == 0:
            return jsonify({
                'status': 'success',
                'message': 'Exécution de make html réussie',
                'output': result.stdout
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Erreur lors de l\'exécution de make html',
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
