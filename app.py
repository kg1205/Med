import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Path to the Excel files
MEDICINE_DATA_FILE = os.path.join('data', 'medicines.xlsx')
TEST_DATA_FILE = os.path.join('data', 'Blood And Scan.xlsx')

HOSPITAL_DOCTOR_FILE = os.path.join('data', 'Hospital And Doctor.xlsx')

# Load data from Excel file
df_hospital_doctor = pd.read_excel(HOSPITAL_DOCTOR_FILE)

# Load data from Excel files
df_medicine = pd.read_excel(MEDICINE_DATA_FILE)
df_tests = pd.read_excel(TEST_DATA_FILE)

print(df_medicine.columns)
print(df_tests.columns)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/medicine_data', methods=['GET', 'POST'])
def medicine_data():
    if request.method == 'POST':
        selected_medicine = request.form.get('option').strip()
        print(f"Selected Medicine: {selected_medicine}")

        if 'MedicineName' not in df_medicine.columns:
            return "Error: 'MedicineName' column not found in DataFrame."

        if selected_medicine in df_medicine['MedicineName'].values:
            medicine_row = df_medicine[df_medicine['MedicineName'] == selected_medicine].iloc[0]
            dosage = medicine_row['Dosage']
            time = medicine_row['Time Of Acceptance']
            instructions = medicine_row['Instructions']
            medication = medicine_row['Medication']
            uses = medicine_row['Uses']
            commonsideeffects = medicine_row['Common Side Effects']
            raresideeffects = medicine_row['Rare Side Effects']

            return render_template('medicine_data.html',
                                   show_results=True,
                                   medicine={'name': selected_medicine},
                                   dosage=dosage,
                                   instructions=instructions,
                                   time=time,
                                   medication=medication,
                                   uses=uses,
                                   commonsideeffects=commonsideeffects,
                                   raresideeffects=raresideeffects)
        else:
            return "Error: Selected medicine not found."
    else:
        medicines = df_medicine['MedicineName'].tolist()
        return render_template('medicine_data.html',
                               show_results=False,
                               medicines=medicines)



@app.route('/Tests_And_Scanes', methods=['GET', 'POST'])
def Tests_And_Scanes():
    if request.method == 'POST':
        test_category = request.form.get('test_category').strip()
        diagnostic_test = request.form.get('diagnostic_test').strip()

        print(f"Test category: {test_category}, Diagnostic test: {diagnostic_test}")

        if 'Test category' not in df_tests.columns or 'Diagnostic test' not in df_tests.columns:
            return "Error: Required columns not found in DataFrame."

        if test_category in df_tests['Test category'].values:
            test_row = df_tests[df_tests['Test category'] == test_category]
            print(f"Available diagnostic tests for {test_category}: {test_row['Diagnostic test'].unique()}")

            if diagnostic_test:
                test_row = test_row[test_row['Diagnostic test'].str.strip() == diagnostic_test]
                print(f"Filtered test rows: {test_row}")

            if not test_row.empty:
                test_row = test_row.iloc[0]
                specimen_type = test_row['Specimen type']
                equipment_used = test_row['Equipment used']
                sample_collection = test_row['Sample Collection']

                return render_template('test_results.html',
                                       show_results=True,
                                       test_category=test_category,
                                       diagnostic_test=diagnostic_test,
                                       specimen_type=specimen_type,
                                       equipment_used=equipment_used,
                                       sample_collection=sample_collection)
            else:
                return "Error: Test not found."
        else:
            return "Error: Test category not found."
    else:
        test_categories = df_tests['Test category'].unique().tolist()

        # Clean and remove duplicates
        diagnostic_tests = (df_tests.groupby('Test category')['Diagnostic test']
                            .apply(lambda x: list(set(x.dropna().str.strip())))
                            .to_dict())

        return render_template('Tests_And_Scanes.html',
                               test_categories=test_categories,
                               diagnostic_tests=diagnostic_tests)



@app.route('/test_results')
def test_results():
    # This route handles the results page
   def Test_Results():
    test_category = request.args.get('test_category')
    diagnostic_test = request.args.get('diagnostic_test')
    specimen_type = request.args.get('specimen_type')
    equipment_used = request.args.get('equipment_used')
    sample_collection = request.args.get('sample_collection')

    return render_template('test_results.html',
                           show_results=True,
                           test_category=test_category,
                           diagnostic_test=diagnostic_test,
                           specimen_type=specimen_type,
                           equipment_used=equipment_used,
                           sample_collection=sample_collection)

@app.route('/doctors_availability', methods=['GET', 'POST'])
def doctors_availability():
    # Get unique locations
    locations = sorted(df_hospital_doctor['Location'].unique())

    if request.method == 'POST':
        location = request.form.get('location')
        hospital = request.form.get('hospital')

        if not location:
            return render_template('doctors_availability.html', locations=locations, error="Please select a location")

        # Redirect to the doctor_results page with query parameters
        return redirect(url_for('doctor_results', location=location, hospital=hospital))

    # For GET request, render the form
    return render_template('doctors_availability.html', locations=locations)

@app.route('/doctor_results')
def doctor_results():
    location = request.args.get('location')
    hospital = request.args.get('hospital')

    if not location:
        return redirect(url_for('doctors_availability'))

    # Filter data based on user selection
    if hospital:
        filtered_data = df_hospital_doctor[(df_hospital_doctor['Location'] == location) & 
                                           (df_hospital_doctor['Hospital Names'] == hospital)]
    else:
        filtered_data = df_hospital_doctor[df_hospital_doctor['Location'] == location]

    # Convert filtered data to a list of dictionaries for easy rendering in template
    results = filtered_data.to_dict('records')

    return render_template('doctor_results.html', results=results, location=location, hospital=hospital)

@app.route('/get_hospitals/<location>')
def get_hospitals(location):
    hospitals = sorted(df_hospital_doctor[df_hospital_doctor['Location'] == location]['Hospital Names'].unique())
    return {'hospitals': hospitals}


@app.route('/prescription')
def prescription():
    # Render the prescription page
    return render_template('prescription.html')

@app.route('/diet_control')
def diet_control():
    # Render the diet control page
    return render_template('diet_control.html')

@app.route('/fee_structure')
def fee_structure():
    # Render the fee structure page
    return render_template('fee_structure.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Placeholder for real authentication
        if username != 'admin' or password != 'secret':
            error = 'Invalid credentials'
        # else:
        #     return redirect(url_for('index'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
