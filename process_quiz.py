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

def calculate_adjusted_score(raw_score, max_raw_score, total_points):
    """Calculate adjusted score using rule of three."""
    # Rule of three: if max_raw_score -> total_points, then raw_score -> x
    if max_raw_score == 0:
        return 0
    return (raw_score * total_points) / max_raw_score

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
            # For each question: if raw_score_per_question -> (total_points/num_questions), then earned_raw_score -> x
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
                'Raw Scores': earned_raw_scores,  # Store raw scores from Excel
                'Student Raw Total': team_raw_total,  # Use team total for student
                'Team Raw Total': team_raw_total,
                'Team Adjusted Total': team_adjusted_total,
                'Adjusted Scores': adjusted_scores,
                'Student Adjusted Total': team_adjusted_total  # Same as team adjusted total
            })
    
    return results, question_numbers, max_possible_raw_total

def create_output_excel(results, question_numbers, output_file):
    """Create the output Excel file with the processed data."""
    # Prepare data for DataFrame
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

def main():
    print("\nQuiz Score Processing Tool")
    print("-" * 30)
    
    # Get quiz information from user
    quiz_name = input("\nEnter the quiz name: ").strip()
    
    while True:
        try:
            raw_score_per_question = float(input("Enter the total raw score possible per question: ").strip())
            if raw_score_per_question <= 0:
                print("Raw score must be greater than 0. Please try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for raw score.")
    
    while True:
        try:
            total_points = float(input("Enter the total points for the quiz: ").strip())
            if total_points <= 0:
                print("Total points must be greater than 0. Please try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for total points.")
    
    # Setup paths
    input_dir = Path('inputdata')
    output_dir = Path('outputdata')
    output_dir.mkdir(exist_ok=True)
    
    # Find the most recent Excel file in the input directory
    input_files = list(input_dir.glob('*.xlsx'))
    if not input_files:
        print("Error: No Excel files found in the input directory")
        return
    
    input_file = max(input_files, key=lambda x: x.stat().st_mtime)
    print(f"\nProcessing input file: {input_file.name}")
    
    output_file = output_dir / f"{quiz_name}.xlsx"
    
    try:
        # Process the data
        results, question_numbers, max_possible_raw_total = process_quiz_data(
            input_file,
            sheet_name='Team Analysis',
            total_points=total_points,
            raw_score_per_question=raw_score_per_question
        )
        
        print(f"\nFound {len(question_numbers)} questions")
        print(f"Raw score possible per question: {raw_score_per_question} points")
        print(f"Maximum raw score possible: {max_possible_raw_total} points")
        print(f"Total adjusted points: {total_points} points")
        
        # Generate output
        create_output_excel(results, question_numbers, output_file)
        print(f"\nProcessing complete. Output saved to {output_file}")
        
    except Exception as e:
        print(f"\nError processing quiz data: {str(e)}")
        return

if __name__ == '__main__':
    main()