from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/execute-make-html', methods=['GET'])
def pull():
    branch = request.json.get('branch', 'main')  # Par défaut, la branche est 'main'
    
    try:
        # Exécutez la commande Git pull
        result = subprocess.run(['git', 'pull', 'origin', branch, '--force'], capture_output=True, text=True)

        if result.returncode == 0:
            return jsonify({'message': 'Pull successful', 'output': result.stdout}), 200
        else:
            return jsonify({'message': 'Pull failed', 'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

def execute_make_html():
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
            return jsonify({
                'status': 'success',
                'message': 'Exécution de make.bat html réussie',
                'output': result.stdout
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Erreur lors de l\'exécution de make.bat html',
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
