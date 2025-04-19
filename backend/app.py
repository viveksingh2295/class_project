from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

DATA_FILE = os.path.join(app.root_path, 'static', 'patient_data.csv')

@app.route('/')
def home():
    return render_template('index.html')

def generate_advice(anxiety, depression, sleep, stress):
    advice = []

    if int(anxiety) > 7:
        advice.append("Consider practicing meditation or breathing exercises to manage anxiety.")
    if int(depression) > 7:
        advice.append("Talking to a counselor or therapist could help with depression.")
    if int(sleep) < 4:
        advice.append("Improve your sleep hygiene—try reducing screen time before bed.")
    if int(stress) > 7:
        advice.append("Take regular breaks, engage in relaxing activities, or try yoga.")

    if not advice:
        advice.append("Keep up the great work maintaining your mental health!")

    return " ".join(advice)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    anxiety = request.form['anxiety']
    depression = request.form['depression']
    sleep = request.form['sleep']
    stress = request.form['stress']
    medication = request.form['medication']
    med_name = request.form['med_name'] if medication == "yes" else "N/A"

    data = [name, age, gender, anxiety, depression, sleep, stress, medication, med_name]

    with open(DATA_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

    result_data = {
        "anxiety": int(anxiety),
        "depression": int(depression),
        "sleep": int(sleep),
        "stress": int(stress)
    }

    advice = generate_advice(anxiety, depression, sleep, stress)

    return render_template("result.html", result_data=result_data, advice=advice)

@app.route('/dashboard')
def dashboard():
    entries = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            reader = csv.reader(file)
            entries.extend(reader)
    return render_template('dashboard.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
