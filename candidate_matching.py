import pandas as pd
import pdfplumber
import re
import os

def load_job_descriptions(csv_path):
    """
    Loads job descriptions from a CSV file.
    
    Args:
        csv_path (str): The path to the job description CSV file.
    
    Returns:
        DataFrame: A pandas DataFrame containing job descriptions.
    """
    return pd.read_csv(csv_path, encoding='ISO-8859-1')  # Change encoding as needed

def extract_text_from_cv(cv_file):
    """
    Extracts text from a CV (PDF file).
    
    Args:
        cv_file (str): The CV file name.
    
    Returns:
        str: The extracted text from the CV.
    """
    extracted_text = ""
    try:
        with pdfplumber.open(cv_file) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from CV {cv_file}: {e}")
    
    return extracted_text.strip()

def extract_job_description_from_cv(cv_text):
    """
    Extracts the job description from the CV text.
    
    Args:
        cv_text (str): The full text extracted from the CV.
    
    Returns:
        str: The extracted job description.
    """
    # Assuming the job description in the CV is marked with a specific keyword
    job_description_match = re.search(r'Work Experience\s*(.*?)(?=Skills:|Certifications:|Achievements:|$)', cv_text, re.DOTALL)
    
    if job_description_match:
        return job_description_match.group(1).strip()
    return ""

def extract_job_title_from_cv(cv_text):
    """
    Extracts the job title from the CV text.
    
    Args:
        cv_text (str): The full text extracted from the CV.
    
    Returns:
        str: The extracted job title.
    """
    # Adjusted regex to capture job title directly
    job_title_match = re.search(r'Work Experience\s*(.*?)\s+at', cv_text, re.DOTALL)
    if job_title_match:
        return job_title_match.group(1).strip()
    return ""

def match_candidate(cv_file, job):
    """
    Calculates the matching score for a candidate's CV against a job description.
    
    Args:
        cv_file (str): The CV file name.
        job (Series): A row from the job descriptions DataFrame.
    
    Returns:
        int: The matching score.
    """
    # Extract text from the CV
    cv_text = extract_text_from_cv(cv_file)

    # Extract job title from the CV
    job_title_from_cv = extract_job_title_from_cv(cv_text)

    # Check if the job title matches the job description
    if job_title_from_cv.lower() != job['Job Title'].lower():
        return 0  # No match if job titles do not match

    # Extract job description from the CV
    job_description_from_cv = extract_job_description_from_cv(cv_text)

    # Use the job description from the CV for matching
    job_description = job['Job Description'].lower()  # Assuming 'Job Description' is the column name
    cv_text_lower = job_description_from_cv.lower()

    # Calculate the matching score based on the number of keywords found in the CV
    keywords = re.findall(r'\b\w+\b', job_description)  # Extract words as keywords
    score = sum(1 for keyword in keywords if keyword in cv_text_lower)

    return score

# Example usage
if __name__ == "__main__":
    job_description_path = r"C:\Users\lenovo\Desktop\recruitment-automation\data\job_description.csv"
    job_descriptions = load_job_descriptions(job_description_path)

    cv_directory = r"C:\Users\lenovo\Desktop\recruitment-automation\data\cv"

    for index, job in job_descriptions.iterrows():
        job_title = job['Job Title']
        
        for cv_file in os.listdir(cv_directory):
            if cv_file.endswith('.pdf'):
                cv_path = os.path.join(cv_directory, cv_file)
                matching_score = match_candidate(cv_path, job)  # Pass the CV path and job
                
                candidate_name = cv_file[:-4]  # Assuming the file name is the candidate's name
                
                # Only print if the matching score is greater than 0
                if matching_score > 0:
                    print(f"Candidate: {candidate_name} | Job Title: {job_title} | Matching Score: {matching_score}")