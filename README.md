Plateforme de Détection d’Anomalies Réseau – AJR

Ce projet a été réalisé dans le cadre d’un stage à l’Agence Judiciaire du Royaume (AJR).
Il s’agit d’une plateforme intelligente permettant de détecter automatiquement des anomalies réseau (intrusions, machines potentiellement infectées ou comportements suspects) à partir de données issues des logs Kaspersky.

L’application combine Machine Learning, explicabilité, et une interface web Flask simple pour aider les administrateurs réseau dans la prise de décision.

🎯 Objectif du projet

L’objectif est de créer un système capable de :

Analyser les données réseau extraites des logs

Prédire si une machine est infectée ou non

Expliquer les causes probables d’une anomalie

Offrir une interface web ergonomique basée sur Flask

Visualiser les principaux graphiques produits lors de l’analyse

🧠 Modèles utilisés
1️⃣ Modèle principal : Détection d'infection

Algorithme : Random Forest Classifier

Données d’entrée : 10 features sélectionnées via SelectKBest

Sortie : infecté / non infecté

2️⃣ Modèle secondaire : Explication

Objectif : expliquer une anomalie détectée

Techniques : modèle explicatif + SHAP

Sortie : feature la plus responsable de la prédiction

🏗️ Architecture du projet
Data → Prétraitement → Sélection de Features → Entraînement du modèle ML →  Déploiement Flask  →   Interface Web + Visualisations

🌐 Fonctionnement de l’application

L’utilisateur peut :

✔️ 1. Fournir les valeurs des 10 caractéristiques nécessaires

L’application charge automatiquement le modèle et réalise la prédiction.

✔️ 2. Visualiser le résultat

→ Infecté / Non infecté

✔️ 3. Obtenir une explication

→ Indication de la feature la plus influente
→ Graphiques analytiques

✔️ 4. Consulter les graphiques générés

Heatmap de corrélation

Distribution de la classe

Boxplots

Scatter 3D

Graphique d’importance des features

📊 Exemples de visualisations produites

Les images ci-dessous sont générées automatiquement dans le dossier static/ :

correlation_heatmap.png

target_distribution.png

Lollipop_chart.png

3d_scatter.png

boxplot_grouped.png

🔧 Lancer l’application

pip install -r requirements.txt

python plat.py


Accéder via :
👉 http://127.0.0.1:5000/

🔮 Points à améliorer & Perspectives

📌 1. Amélioration de l’explication fournie à l’utilisateur

Actuellement, le modèle explicatif donne une réponse simple ("la feature X est responsable").
➡️ À améliorer :

Ajouter une explication plus riche (graphique SHAP détaillé, contribution des features, valeurs exactes).

Afficher un résumé des raisons de la décision.

📌 2. Amélioration de l’étape de prétraitement des logs

Actuellement, le modèle travaille sur des données déjà nettoyées.
➡️ À améliorer :

Automatiser l’extraction et le nettoyage des logs bruts (EVTX, CSV…).

Créer un module qui :

lit les logs réels des serveurs

extrait les features nécessaires

les transforme au bon format pour le modèle

📌 3. Déploiement du modèle

Le modèle est actuellement déployé localement via Flask.
➡️ À améliorer :

Déploiement sur serveur AJR sécurisé

Intégration avec Nginx + Gunicorn

Intégration Docker pour simplifier la maintenance

Accès authentifié pour les administrateurs

📌 4. Gestion de données en temps réel

➡️ À implémenter :

Collecte en continu via agent IoT

Analyse temps réel (MQTT, Kafka)

Alertes instantanées en cas d’anomalie détectée

📌 5. Interface utilisateur

➡️ À améliorer :

Rendre l’interface plus moderne

Ajouter un tableau des prédictions

Ajouter un historique (logs + prédictions + explications)

🏁 Conclusion

Ce projet pose les bases d’un outil d’analyse réseau intelligent capable de détecter les anomalies et de les expliquer.
Les perspectives d’amélioration le transformeront en un véritable IDS intelligent intégré aux systèmes de l’AJR.
