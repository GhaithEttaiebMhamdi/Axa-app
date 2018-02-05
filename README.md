# Axa-app
 un web service REST qui permet d’accepter, de refuser ou de mettre en attente des demandes de remboursement

## Setup
* Installer Python 3.6
* Executer setup.sh (Linux, OS X, Cygwin) ou setup.bat (Windows)
* Executer ./app.py pour demarrer le serveur (sous Windows flask\Scripts\python app.py)
* Ouvrir http://localhost:5000 dans votre navigateur pour demarrer le client


## Utilisation
* Pour consulter toutes les demandes : **localhost:5000/demandes**    en utilisant l'action GET
* Pour consulter une demande specifique via le numero de dossier associé : **localhost:5000/demandes/<num_dossier>**  en utlisant l'action GET
* Pour consulter tous les resultats : **localhost:5000/results**  en utlisiant l'action GET
* Pour consulter un resultat specifique : **localhost:5000/resultats/<num_dossier>**  en utlisiant l'action GET
* Pour ajouter une demande : **localhost:5000/demandes** en utilisant l'action POST
