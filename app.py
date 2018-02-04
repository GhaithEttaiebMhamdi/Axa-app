# title           :app.py
# description     :un web service REST qui permet d’accepter, de refuser ou de mettre en attente des demandes de remboursement
# author          :Ghaith M'hamdi
# date            :04/02/2018
# version         :0.1
# usage           :python app.py
# python_version  :3.6.x
# ==============================================================================

from datetime import datetime,date
from flask import Flask,jsonify,request,make_response,abort

app = Flask(__name__)

TYPES = ['VERRE','MONTURE','LENTILLE']


#Initialiser une liste de demandes avec Un exemple

demandes = [
{
 "num_dossier": "457864",
 "num_contrat": "123456789",
 "num_professionel": "50505050",
 "date_naissance": "1988-05-12",
 "produits": [
 {"type": "VERRE", "montant": 123.5},
 {"type": "VERRE", "montant": 68.5},
 {"type": "MONTURE", "montant": 123.5}
 ]
}

]

#Initialiser une liste de Resultats Vide
results = [

]

@app.route('/')
def hello():
    return "Application : Axa-app" \
           "Pour consulter toutes les demandes : localhost:5000/demandes    en utilisant l'action GET" \
           "Pour consulter une demande specifique via le numero de dossier associé : localhost:5000/demandes/<num_dossier>  en utlisiant l'action GET" \
           "Pour consulter tous les resultats : localhost:5000/results  en utlisiant l'action GET" \
           "Pour consulter un resultat specifique : localhost:5000/resultats/<num_dossier>  en utlisiant l'action GET" \
           "Pour ajouter une demande : localhost:5000/demandes en utilisant l'action POST "


#Cette fonction a pour role de surcharger la page par defaut de l'erreur 404 et de la remplacer par error : Not Found

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


#cette fonction permet de retourner toutes les demandes via la route /demandes et l'action GET

@app.route('/demandes',methods=['GET'])
def get_demandes():
    return jsonify({'demandes' : demandes})


#cette fonction permet de retourner une demande specifique associé au numero du dossier via la route /demandes/num_dossier et l'action GET

@app.route('/demandes/<string:num_dossier>', methods=['GET'])
def get_demande(num_dossier):
    demande = [demande for demande in demandes if demande['num_dossier'] == num_dossier]
    if len(demande) == 0:
        abort(404)
    return jsonify({'demande': demande[0]})


#cette fonction permet d'ajouter une demande en format JSON via la route /demandes et l'action POST

@app.route('/demandes',methods=['POST'])
def create_demande():
    demande = {
        'num_dossier' : request.json['num_dossier'],
        'num_contrat' : request.json['num_contrat'],
        'num_professionel' : request.json['num_professionel'],
        'date_naissance' : request.json['date_naissance'],
        'produits' : request.json['produits']
    }
    demandes.append(demande)
    return jsonify({'demande' :demande})


#cette fonction permet de retourner les status des demandes via la route /results et l'action GET

@app.route('/results',methods=['GET'])
def get_results():
    global inputData
    for i in demandes:
        inputData = i
        results.append({'num_dossier' : inputData['num_dossier'], 'statut :' : check_rules()},)
    return jsonify({
        'results' : results
    })

#cette fonction permet de retourner le statut d'une demande spécifique via la route /demandes/num_dossier et l'action GET


@app.route('/results/<string:num_dossier>',methods=['GET'])
def get_result(num_dossier):
    global inputData
    inputData[0] = [demande for demande in demandes if demande['num_dossier'] == num_dossier]
    if len(inputData) == 0:
        abort(404)
    return jsonify({
        'num_dossier' : inputData['num_dossier'],
        'statut' : check_rules()
    })


#Cette fonction retourne une chaine de caractère "REFUSEE", "EN ATTENTE", "ACCEPTEE" en fonction des régles ci-dessous.
def check_rules():

    if check_error(): # retourne "REFUSEE" dans le cas où la liste des produits comporte au moins un produit de type différent de “MONTURE”,“VERRE”,“LENTILLE”
        return "REFUSEE"

    if total_amount() > 2000 : # retourne "REFUSEE" dans le cas où le montant total des produits > 2000
        return "REFUSEE"

    if lentille_rule(): # retourne "REFUSEE" dans le cas où la liste des produits comporte au moins une lentille dont le prix est > 1000
        return "REFUSEE"

    if calculate_age() < 15 and total_amount() > 1000 : # retourne "EN ATTENTE" dans le cas où l'age < 15 et montant total > 1000
        return "EN ATTENTE"

    if monture_rule(): # retourne "EN ATTENTE" dans le cas où les produits ne sont que de type “MONTURE”
        return "EN ATTENTE"

    return "ACCEPTEE" # retourne "ACCEPTEE" dans le cas où les règles mentionnées n'ont pas été vérifiées.



#Cette fonction booléenne retourne vrai si un type de produit est différent de VERRE, LENTILLE, MONTURE.
def check_error():
    for inputDataRows in inputData['produits']:
        if not any(inputDataRows['type'] in s for s in TYPES):
            return True
    return False

#Cette fonction booléenne retourne vrai si la liste des produits comporte une LENTILLE dont le prix est supérieur à 1000
def lentille_rule():
    for inputDataRows in inputData['produits']:
        if (inputDataRows['type'] == 'LENTILLE') and (inputDataRows['montant'] > 1000 ):
            return True
    return False

#Cette fonction booléenne retourne vrai si les produits ne sont que de type MONTURE
def monture_rule():
    for inputDataRows in inputData['produits']:
        if (inputDataRows['type'] != 'MONTURE'):
            return False
    return True

#Cette fonction retourne la somme des montants de la liste des produits
def total_amount():
        return sum(inputDataRows['montant'] for inputDataRows in inputData['produits'])

#Cette fonction retourne l'age actuel d'une personne calculé à partir de sa date de naissance
def calculate_age():
    born = datetime.strptime(inputData['date_naissance'], '%Y-%m-%d')
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
