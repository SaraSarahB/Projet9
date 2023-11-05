import requests
from flask import Flask, request, render_template

NB_USERS = 322896
REC_TYPE = ['Content-Based', 'Collaborative Filtering']
REC_TYPE_API = {'Content-Based': 'cb', 'Collaborative Filtering': 'cf'}
selected_type = REC_TYPE[0]

app = Flask(' ', template_folder='/home/SaraISTP/Projet9/templates/')

# Endpoint
@app.route('/', methods=["GET", "POST"])
def index():
    selected_id = 0

    if request.method == "POST":
        user_input = request.form.get('user')
        try:
            selected_id = int(user_input)
            if selected_id < 0:
                selected_id = 0
            elif selected_id > NB_USERS:
                selected_id = NB_USERS
        except ValueError:
            # Gérer les cas où la valeur entrée n'est pas un entier
            pass

    return render_template('form.html', sended=False, selected_id=selected_id)

# Endpoint pour recommander les articles du user sélectionné
@app.route('/recommend/', methods=["GET", "POST"])
def recommendArticles():
    selected_id = 0

    if request.method == "POST":
        user_input = request.form.get('user')
        try:
            selected_id = int(user_input)
            if selected_id < 0:
                selected_id = 0
            elif selected_id > NB_USERS:
                selected_id = NB_USERS
        except ValueError:
            # Gérer les cas où la valeur entrée n'est pas un entier
            pass

    r = requests.get(f'https://saradjeg.pythonanywhere.com/recommendation?user_id={selected_id}', verify=True)

    print(f"Request URL: {r.url}")  # Ajout d'un print pour vérifier l'URL de la requête
    print(f"Response status code: {r.status_code}")  # Ajout d'un print pour vérifier le code de statut de la réponse

    if r.status_code == 200:
        content = r.content.decode("utf-8")
        print(f"Content: {content}")  # Ajout d'un print pour vérifier le contenu de la réponse
        remove = '[ ]'
        for charac in remove:
            content = content.replace(charac, '')

        content = content.split(',')
    else:
        content = ["Erreur lors de la récupération des recommandations"]

    print(f"Prediction Text: {content}")  # Ajout d'un print pour vérifier le contenu de prediction_text
    return render_template('form.html', sended=True, selected_id=selected_id, prediction_text=content)

if __name__ == "__main__":
    app.run(debug=True)
