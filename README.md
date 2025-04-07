# Quiz Score Processing Tool

A Python tool for processing team quiz scores and generating adjusted grade reports.

## Features

- Process quiz scores from Excel files
- Calculate raw and adjusted scores for team quizzes
- Score editing capabilities:
  - Edit individual question scores
  - Select teams using numbered list
  - Track all score changes
  - View change history with difference indicators
- Generate detailed Excel reports with:
  - Team scores (raw and adjusted)
  - Individual student information
  - Question-by-question breakdown
- Rule of three based score adjustment
- User-friendly command line interface with:
  - Input validation
  - Confirmation steps
  - Exit options at any stage
  - Change tracking

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
pip install -r requirements.txt
```

## Usage

1. Place input Excel file in the `inputdata` folder
2. Run the script:
```bash
python main.py
```
3. Follow the prompts to enter:
   - Quiz name
   - Raw score per question
   - Total points for the quiz
4. Review and confirm your inputs
5. Enter score editing mode (optional):
   - Select teams by number
   - Edit question scores
   - View change history
   - Confirm or discard changes
6. Find the output Excel file in the `outputdata` folder

## Input File Format

The input Excel file should have a "Team Analysis" sheet with the following columns:
- Team: Team name
- Student Name: Student's full name
- Student ID: Student's identification number
- Email Address: Student's email
- Question scores: Columns named as "1_Score", "2_Score", etc.

## Output Format

The generated Excel file includes:
- Team information (shown once per team)
- Student details (for each student)
- Raw and adjusted scores for each question
- Total scores (both raw and adjusted)

## Features in Detail

### Score Editing
- Select teams from a numbered list
- Edit individual question scores
- View running history of all changes
- See score differences with +/- indicators
- Confirm or discard changes before processing

### Input Validation
- Validates all numeric inputs
- Ensures scores are within valid ranges
- Validates question numbers
- Confirms team existence

### Exit Options
- Exit without processing at initial input
- Exit during score editing
- Confirmation steps to prevent accidental exits
- Change summary shown before exit
