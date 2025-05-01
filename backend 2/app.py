from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

CSV_FILE = 'patient_data.csv'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assessment', methods=['POST'])
def assessment():
    # Collect patient basic details from page 1
    patient_info = {
        'name': request.form['name'],
        'mobile': request.form['mobile'],
        'age': request.form['age'],
        'gender': request.form['gender'],
        'problem': request.form['problem'],
        'doctor': request.form['doctor']
    }
    return render_template('assessment.html', **patient_info)

@app.route('/submit_assessment', methods=['POST'])
def submit_assessment():
    # Collect all data from both forms
    name = request.form['name']
    mobile = request.form['mobile']
    age = request.form['age']
    gender = request.form['gender']
    problem = request.form['problem']
    doctor = request.form['doctor']

    anxiety = request.form['anxiety']
    depression = request.form['depression']
    sleep = request.form['sleep']
    stress = request.form['stress']
    medication = request.form['medication']
    med_name = request.form.get('med_name', '')

    # Store in CSV
    row = [name, age, gender, anxiety, depression, sleep, stress, medication, med_name, mobile, problem, doctor]
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    result_data = {
        'anxiety': int(anxiety),
        'depression': int(depression),
        'sleep': int(sleep),
        'stress': int(stress)
    }

    advice = "Maintain a balanced lifestyle, sleep well, and consult a specialist if symptoms persist."

    return render_template("result.html",
                           result_data=result_data,
                           advice=advice,
                           name=name,
                           mobile=mobile,
                           problem=problem,
                           doctor=doctor)

@app.route('/dashboard')
def dashboard():
    entries = []
    try:
        with open(CSV_FILE, newline='') as f:
            reader = csv.reader(f)
            entries = list(reader)
    except FileNotFoundError:
        pass

    # Pass last patient's info (for display)
    latest = entries[-1] if entries else None
    patient_info = {}
    if latest and len(latest) >= 12:
        patient_info = {
            'name': latest[0],
            'mobile': latest[9],
            'problem': latest[10],
            'doctor': latest[11]
        }

    return render_template('dashboard.html', entries=entries, **patient_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

