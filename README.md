# Quiz Score Processing Tool

A Python tool for processing team quiz scores and generating adjusted grade reports.

## Features

- Process quiz scores from Excel files
- Calculate raw and adjusted scores for team quizzes
- Generate detailed Excel reports with:
  - Team scores (raw and adjusted)
  - Individual student information
  - Question-by-question breakdown
- Rule of three based score adjustment
- User-friendly command line interface

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install pandas openpyxl
```

## Usage

1. Place input Excel file in the `inputdata` folder
2. Run the script:
```bash
python process_quiz.py
```
3. Follow the prompts to enter:
   - Quiz name
   - Raw score per question
   - Total points for the quiz
4. Find the output Excel file in the `outputdata` folder

## Input File Format

The input Excel file should have a "Team Analysis" sheet with the following columns:
- Team: Team name
- Student Name: Student's full name
- Student ID: Student's identification number
- Email Address: Student's email
- Question scores: Columns named as "1_Score", "2_Score", etc.

## Output Format

The generated Excel file includes:
- Team information
- Student details
- Raw and adjusted scores for each question
- Total scores (both raw and adjusted)
