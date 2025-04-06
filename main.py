from flask import Flask, request, jsonify, render_template
import pandas as pd
from job_description_summarizer import summarize_job_description  # Import the summarization function
from candidate_matching import match_candidate, load_job_descriptions  # Import the matching and loading functions
from datetime import datetime, timedelta

# Specify the full path to the templates directory
template_dir = r'C:\Users\lenovo\Desktop\recruitment-automation\templates'

app = Flask(__name__, template_folder=template_dir)

# Store job descriptions and scheduled interviews in memory
job_descriptions = None
scheduled_interviews = []

@app.route('/')
def index():
    """Render the main index page."""
    return render_template('index.html', scheduled_interviews=scheduled_interviews)

@app.route('/upload_job_descriptions', methods=['POST'])
def upload_job_descriptions():
    """Handle the upload of job descriptions and return summaries."""
    global job_descriptions  # Use the global variable to store job descriptions

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Read job titles and descriptions from the uploaded CSV file
    try:
        job_descriptions = load_job_descriptions(file)
    except Exception as e:
        return jsonify({'error': f'Error reading job descriptions: {str(e)}'}), 400

    if job_descriptions is None or job_descriptions.empty:
        return jsonify({'error': 'No job descriptions found in the uploaded file.'}), 400

    summaries = []
    for index, job in job_descriptions.iterrows():
        summary = summarize_job_description(job['Job Description'])
        summaries.append({'Job Title': job['Job Title'], 'Summary': summary})

    return jsonify({'summaries': summaries})

@app.route('/match_candidates', methods=['POST'])
def match_candidates():
    """Match candidates' CVs against job descriptions and return matching scores."""
    global job_descriptions  # Use the global variable to access job descriptions

    if job_descriptions is None:
        return jsonify({'error': 'No job descriptions uploaded. Please upload job descriptions first.'}), 400

    if 'cv_files' not in request.files:
        return jsonify({'error': 'No CV files uploaded'}), 400

    cv_files = request.files.getlist('cv_files')

    if not cv_files:
        return jsonify({'error': 'No CV files uploaded'}), 400

    results = []
    shortlisted_candidates = []  # List to store candidates with matching scores > 50
    for index, job in job_descriptions.iterrows():
        job_title = job['Job Title']  # Adjust this based on your CSV structure
        
        for cv_file in cv_files:
            if cv_file.filename.endswith('.pdf'):
                matching_score = match_candidate(cv_file, job)  # Pass the CV file and job
                
                candidate_name = cv_file.filename[:-4]  # Assuming the file name is the candidate's name
                
                # Append the result only if the matching score is greater than 0
                if matching_score > 0:
                    results.append({
                        'Candidate Name': candidate_name,
                        'Job Title': job_title,
                        'Matching Score': matching_score
                    })
                    
                    # Check if the matching score is greater than 50
                    if matching_score > 50:
                        shortlisted_candidates.append({
                            'Candidate Name': candidate_name,
                            'Job Title': job_title
                        })

    return jsonify({'results': results, 'shortlisted_candidates': shortlisted_candidates})

INTERVIEW_INTERVAL = timedelta(minutes=30)  # Change to timedelta(hours=1) for 1-hour intervals

@app.route('/schedule_interviews', methods=['POST'])
def schedule_interviews_route():
    """Schedule interviews for candidates based on matching scores."""
    global job_descriptions  # Use the global variable to access job descriptions

    if job_descriptions is None:
        return jsonify({'error': 'No job descriptions uploaded. Please upload job descriptions first.'}), 400

    if 'cv_files' not in request.files:
        return jsonify({'error': 'No CV files uploaded'}), 400

    cv_files = request.files.getlist('cv_files')
    threshold = 50  # Set your threshold for scheduling interviews
    global scheduled_interviews
    scheduled_interviews = []  # Reset scheduled interviews

    # Start scheduling from the current time
    current_time = datetime.now()

    for index, job in job_descriptions.iterrows():
        job_title = job['Job Title']  # Adjust this based on your CSV structure
        
        for cv_file in cv_files:
            if cv_file.filename.endswith('.pdf'):
                matching_score = match_candidate(cv_file, job)  # Calculate matching score
                
                candidate_name = cv_file.filename[:-4]  # Assuming the file name is the candidate's name
                
                # Schedule interview if matching score is greater than the threshold
                if matching_score > threshold:
                    scheduled_interviews.append({
                        'candidate_name': candidate_name,
                        'job_title': job_title,
                        'matching_score': matching_score,
                        'interview_time': current_time.strftime("%Y-%m-%d %H:%M:%S")  # Format the date and time
                    })
                    print(f"Scheduled interview for {candidate_name} for job '{job_title}' with score: {matching_score} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Increment the current time by the defined interval for the next interview
                    current_time += INTERVIEW_INTERVAL

    # Check if no candidates were scheduled for interviews
    if not scheduled_interviews:
        return jsonify({'message': 'No CVs have been shortlisted for interviews.'})

    return jsonify({'scheduled_interviews': scheduled_interviews})

if __name__ == '__main__':
    app.run(debug=True)