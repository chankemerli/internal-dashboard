from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict')
def predict():
    try:
        projects = int(request.args.get('projects', 0))
        hours = float(request.args.get('hours', 0))
        critical = int(request.args.get('critical', 0))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input'}), 400

    # Basit kural tabanlı tahmin
    risk_score = (projects * 0.3) + (hours * 0.4) + (critical * 0.3)
    overloaded = risk_score > 10

    return jsonify({
        'overloaded': overloaded,
        'risk_score': round(risk_score / 20, 2)  # normalize 0-1 arasında
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8500)
