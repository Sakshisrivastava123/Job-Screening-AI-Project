<img width="960" alt="cadence" src="https://github.com/user-attachments/assets/327e15c3-4a1e-4289-a49b-6172c4ecf2d1" />﻿# JOB SCREENING AI

## Overview

The JOB SCREENING AI is a multi-agent AI application designed to streamline the recruitment process. It automates the tasks of summarizing job descriptions, extracting data from CVs, matching candidates with job requirements, shortlisting candidates, and sending interview requests.

## Features

- **Job Description Summarization**: Automatically summarizes job descriptions using an on-premises large language model (LLM) via Ollama.
- **CV Data Extraction**: Extracts relevant information from candidate CVs in PDF format.
- **Candidate Matching**: Compares candidate qualifications with job descriptions and calculates match scores.
- **Shortlisting Candidates**: Shortlists candidates based on a defined match score threshold.
- **Interview Scheduling**: Sends personalized email invitations to shortlisted candidates with interview details.
- **Web Interface**: Provides a user-friendly web interface for interaction.

## Requirements

- Python 3.x
- Ollama (for on-premises LLMs)
- SQLite (for database management)
- Flask
- pandas
- smtplib
- email
- pdfplumber (for extracting text from CV PDFs)

## Project Structure
recruitment-automation/
│
├── data/                        # Directory for data files
│   ├── job_description.csv      # CSV file containing job descriptions
│   └── cv/                     # Directory containing CV PDFs
│       ├── cv1.pdf              # Example CV file
│       └── cv2.pdf              # Another example CV file
│
├── templates/                   # Directory for HTML templates
│   └── index.html               # Main HTML file for the web interface
│
├── scripts/                     # Directory for Python scripts
│   ├── ollama_model.py          # Script to interact with Ollama 
│   ├── database_setup.py        # Script to set up the SQLite database
│   ├── job_description_summarizer.py  # Script for summarizing job descriptions
│   ├── cv_extractor.py          # Script for extracting data from CVs
│   ├── candidate_matching.py     # Script for matching candidates with job descriptions
│   ├── data_insertion.py         # Script to insert data into the database
│   └── main.py                  # Flask API to handle requests and responses
│
├── requirements.txt             # File listing required Python packages
└── README.md                    # Documentation for the project



## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd recruitment-automation

2. pip install -r requirements.txt                 #install the required packages


3. python scripts/database_setup.py                # Set up the SQLite database

4. python scripts/main.py                          #Run the Flask application

5. Open your web browser and navigate to ***link*** to access the application.
## project


<img width="393" alt="Project image" src="https://github.com/user-attachments/assets/78b311a4-b5b9-49b8-af88-79cb8ed3431e" />




