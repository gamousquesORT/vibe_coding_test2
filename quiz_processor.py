"""Module for processing quiz data from Excel files."""
import pandas as pd
import re
from pathlib import Path

def extract_question_numbers(columns):
    """Extract unique question numbers from column names."""
    question_numbers = set()
    for col in columns:
        match = re.match(r'(\d+)_score', col.lower())
        if match:
            question_numbers.add(int(match.group(1)))
    return sorted(list(question_numbers))

def process_quiz_data(input_file, sheet_name, total_points, raw_score_per_question):
    """Process quiz data and calculate scores."""
    # Read the Excel file
    df = pd.read_excel(input_file, sheet_name=sheet_name)
    
    # Get question numbers from columns
    question_numbers = extract_question_numbers(df.columns)
    max_possible_raw_total = len(question_numbers) * raw_score_per_question
    
    # Calculate raw scores for each student and team
    results = []
    
    # Group by team
    for team_name, team_data in df.groupby('Team'):
        # Get the first student's scores as they should be the same for the whole team
        first_student = team_data.iloc[0]
        earned_raw_scores = []   # Store the raw scores from Excel
        
        # Get team scores using the first student's data
        for q_num in question_numbers:
            score_col = f"{q_num}_Score"
            if score_col in df.columns:
                # The value in Excel is already the earned score
                earned_raw_score = float(first_student[score_col])
                earned_raw_scores.append(earned_raw_score)
        
        # Calculate team raw total from earned scores
        team_raw_total = sum(earned_raw_scores)
        
        # Calculate team adjusted total using rule of three
        # If max_possible_raw_total -> total_points, then team_raw_total -> x
        team_adjusted_total = (team_raw_total * total_points) / max_possible_raw_total
        
        # Process each student in the team
        for _, student in team_data.iterrows():
            # Calculate adjusted scores for individual questions
            points_per_question = total_points / len(question_numbers)
            adjusted_scores = [
                (earned_score * points_per_question) / raw_score_per_question 
                for earned_score in earned_raw_scores
            ]
            
            # Store student data - using team scores since it's a team quiz
            results.append({
                'Team Name': team_name,
                'Student ID': student['Student ID'],
                'Student Name': student['Student Name'],
                'Email Address': student['Email Address'],
                'Raw Scores': earned_raw_scores,
                'Student Raw Total': team_raw_total,
                'Team Raw Total': team_raw_total,
                'Team Adjusted Total': team_adjusted_total,
                'Adjusted Scores': adjusted_scores,
                'Student Adjusted Total': team_adjusted_total
            })
    
    return results, question_numbers, max_possible_raw_total

def create_output_excel(results, question_numbers, output_file):
    """Create the output Excel file with the processed data."""
    output_data = []
    for result in results:
        row = {
            'Team Name': result['Team Name'],
            'Team Raw Total': result['Team Raw Total'],
            'Team Adjusted Total': result['Team Adjusted Total'],
            'Student ID': result['Student ID'],
            'Student Name': result['Student Name'],
            'Email Address': result['Email Address'],
            'Student Raw Total': result['Student Raw Total'],
            'Student Adjusted Total': result['Student Adjusted Total']
        }
        
        # Add individual question scores
        for i, (raw, adjusted) in enumerate(zip(result['Raw Scores'], result['Adjusted Scores']), 1):
            row[f'Q{i} Raw Score'] = raw
            row[f'Q{i} Adjusted Score'] = adjusted
        
        output_data.append(row)
    
    # Create DataFrame and save to Excel
    df_output = pd.DataFrame(output_data)
    df_output.to_excel(output_file, index=False)