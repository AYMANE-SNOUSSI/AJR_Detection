from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import re

app = Flask(__name__)

# Charger les modèles et les features sélectionnées
model = joblib.load('trained_model.pkl')
selected_features = joblib.load('selected_features.pkl')
explanation_model = joblib.load('explanation_model.pkl')

# Décrire chaque feature avec des explications brèves et détaillées
descriptions_brief = {
    'logged_in': 'Indique si l\'utilisateur est connecté (1) ou non (0).',
    'serror_rate': 'Le taux d\'erreurs SYN dans les connexions du réseau.',
    'srv_serror_rate': 'Le taux d\'erreurs SYN dans les connexions des services.',
    'same_srv_rate': 'Le taux de connexions au même service.',
    'dst_host_srv_count': 'Le nombre de connexions au même service à l\'hôte de destination.',
    'dst_host_same_srv_rate': 'Le taux de connexions au même service à l\'hôte de destination.',
    'dst_host_serror_rate': 'Le taux d\'erreurs SYN pour l\'hôte de destination.',
    'dst_host_srv_serror_rate': 'Le taux d\'erreurs SYN pour les services à l\'hôte de destination.',
    'flag_S0': 'Indicateur binaire si le flag de la connexion est S0 (1) ou non (0).',
    'flag_SF': 'Indicateur binaire si le flag de la connexion est SF (1) ou non (0).'
}

descriptions_detailed = {
    'logged_in': 'Ce paramètre est crucial pour comprendre le comportement de l\'utilisateur et peut aider à distinguer les actions normales des activités malveillantes. Les utilisateurs non connectés peuvent être plus susceptibles de représenter des menaces potentiellement non authentifiées.',
    'serror_rate': 'Un taux élevé d\'erreurs SYN peut indiquer une attaque SYN flood. Une attaque SYN flood (attaque semi-ouverte) est un type d’attaque par déni de service (DDoS) qui vise à rendre un serveur indisponible pour le trafic légitime en consommant toutes les ressources serveur disponibles. En envoyant à plusieurs reprises des paquets de demande de connexion initiale (SYN), le pirate est en mesure de submerger tous les ports disponibles sur une machine serveur ciblée, ce qui oblige l’appareil ciblé à répondre lentement au trafic légitime, ou l’empêche totalement de répondre.',
    'srv_serror_rate': 'Semblable au serror_rate, ce paramètre mesure les erreurs SYN mais spécifiquement pour les services individuels. Un taux élevé peut également signaler des attaques visant des services particuliers.',
    'same_srv_rate': 'Ce paramètre mesure la proportion de connexions dirigées vers le même service. Un taux anormalement élevé peut indiquer une tentative de surcharge ou d\'attaque sur un service spécifique.',
    'dst_host_srv_count': 'Ce paramètre compte combien de connexions ont été établies vers un service particulier sur l\'hôte de destination. Un nombre élevé peut être le signe d\'une attaque par déni de service visant à surcharger un service spécifique.',
    'dst_host_same_srv_rate': 'Mesure la proportion des connexions qui ciblent le même service sur un hôte de destination. Des valeurs élevées peuvent indiquer une focalisation anormale sur un service unique, potentiellement en raison d\'une attaque.',
    'dst_host_serror_rate': 'Un taux élevé d\'erreurs SYN à l\'hôte de destination peut également indiquer une attaque SYN flood dirigée spécifiquement contre cet hôte, rendant les ressources de ce dernier indisponibles pour le trafic légitime.',
    'dst_host_srv_serror_rate': 'Similaire au dst_host_serror_rate, ce paramètre se concentre sur les erreurs SYN pour des services spécifiques sur l\'hôte de destination. Un taux élevé peut indiquer des attaques ciblant des services particuliers sur cet hôte.',
    'flag_S0': 'Le flag S0 indique que la connexion est "syn sent", ce qui signifie qu\'une demande de connexion a été envoyée mais qu\'aucune réponse n\'a été reçue. Un grand nombre de connexions avec ce flag peut signaler des tentatives de connexion infructueuses, souvent associées à des scans de port ou à des tentatives de déni de service.',
    'flag_SF': 'Le flag SF indique que la connexion a été établie et terminée correctement. C\'est typique des connexions normales, mais une analyse de la fréquence et du contexte des connexions SF peut encore être utile pour identifier des schémas anormaux dans le trafic réseau.'
}
@app.route('/')
def home():
    return render_template('index.html', features=selected_features, descriptions=descriptions_brief)

@app.route('/details')
def details():
    return render_template('details.html', descriptions=descriptions_detailed)

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

# Fonction pour lire les fichiers de logs
def read_log_file(file):
    try:
        # Lire le fichier comme un texte brut
        log_data = file.read().decode('utf-8')
        return log_data
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture du fichier log : {str(e)}")

# Fonction pour extraire les features des logs
def extract_features(log_data):
    try:
        # Simuler l'extraction des features à partir du fichier log
        # Adapter cette extraction à la structure de ton fichier de log réel

        # Exemple : Utiliser des regex pour extraire certaines informations spécifiques
        # Ici, tu devras analyser comment les logs sont structurés pour adapter les regex

        # Exemple de regex pour extraire une valeur si elle existe
        logged_in = re.search(r'logged_in=(\d+)', log_data)
        serror_rate = re.search(r'serror_rate=([\d.]+)', log_data)
        srv_serror_rate = re.search(r'srv_serror_rate=([\d.]+)', log_data)
        same_srv_rate = re.search(r'same_srv_rate=([\d.]+)', log_data)
        dst_host_srv_count = re.search(r'dst_host_srv_count=(\d+)', log_data)
        dst_host_same_srv_rate = re.search(r'dst_host_same_srv_rate=([\d.]+)', log_data)
        dst_host_serror_rate = re.search(r'dst_host_serror_rate=([\d.]+)', log_data)
        dst_host_srv_serror_rate = re.search(r'dst_host_srv_serror_rate=([\d.]+)', log_data)
        flag_S0 = re.search(r'flag_S0=(\d+)', log_data)
        flag_SF = re.search(r'flag_SF=(\d+)', log_data)

        # Mettre les valeurs à défaut si elles ne sont pas trouvées dans le log
        features_dict = {
            'logged_in': int(logged_in.group(1)) if logged_in else 0,
            'serror_rate': float(serror_rate.group(1)) if serror_rate else 0.0,
            'srv_serror_rate': float(srv_serror_rate.group(1)) if srv_serror_rate else 0.0,
            'same_srv_rate': float(same_srv_rate.group(1)) if same_srv_rate else 0.0,
            'dst_host_srv_count': int(dst_host_srv_count.group(1)) if dst_host_srv_count else 0,
            'dst_host_same_srv_rate': float(dst_host_same_srv_rate.group(1)) if dst_host_same_srv_rate else 0.0,
            'dst_host_serror_rate': float(dst_host_serror_rate.group(1)) if dst_host_serror_rate else 0.0,
            'dst_host_srv_serror_rate': float(dst_host_srv_serror_rate.group(1)) if dst_host_srv_serror_rate else 0.0,
            'flag_S0': int(flag_S0.group(1)) if flag_S0 else 0,
            'flag_SF': int(flag_SF.group(1)) if flag_SF else 0
        }

        # Créer un dataframe avec les features extraites
        return pd.DataFrame([features_dict])
    except Exception as e:
        raise ValueError(f"Erreur lors de l'extraction des features : {str(e)}")
# Vérifier les features attendues par le modèle
@app.route('/check_features', methods=['GET'])
def check_features():
    try:
        expected_features = selected_features  # Les features avec lesquelles le modèle a été entraîné
        return jsonify({'expected_features': expected_features})
    except Exception as e:
        return jsonify({'error': str(e)})


# Route pour charger un fichier et faire une prédiction

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier envoyé.'})

        file = request.files['file']
        file_type = request.form.get('file_type')  # csv ou log

        if file_type == "csv":
            # Lire le fichier CSV
            data = pd.read_csv(file)
        elif file_type == "log":
            # Logique pour traiter les fichiers log
            data = read_log_file(file)  # à implémenter si nécessaire
        else:
            return jsonify({'error': 'Type de fichier non supporté.'})

        # Vérifier les colonnes manquantes
        missing_features = [feature for feature in selected_features if feature not in data.columns]

        # Ajouter les colonnes manquantes avec des valeurs par défaut (par exemple 0)
        for feature in missing_features:
            data[feature] = 0  # Vous pouvez aussi utiliser d'autres valeurs par défaut

        # S'assurer que seules les features nécessaires sont présentes
        features = data[selected_features]

        # Faire une prédiction
        predictions = model.predict(features)
        features['prediction'] = predictions

        # Explication des anomalies
        explanations = explanation_model.predict(features)

        return jsonify({
            'features': features.to_dict(),
            'predictions': list(predictions),
            'explanations': list(explanations)
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# Route pour les prédictions à partir des formulaires
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données du formulaire
        data = request.form.to_dict()
        data_df = pd.DataFrame([data])

        # Convertir les données en types appropriés
        for feature in selected_features:
            data_df[feature] = data_df[feature].astype(float)

        # S'assurer que les colonnes sont dans le bon ordre
        data_df = data_df[selected_features]

        # Faire une prédiction
        prediction = model.predict(data_df)[0]

        if prediction == "normal":
            explanation = "État : Normal"
        else:
            # Utiliser le modèle d'explication pour analyser les anomalies
            explanation = explanation_model.predict(data_df)[0]

        return jsonify({
            'prediction': prediction,
            'explanation': explanation
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)