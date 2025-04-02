"""Module for processing quiz data from Excel files."""
import pandas as pd
import re
from pathlib import Path

class QuizProcessor:
    """Class for processing quiz data from Excel files."""
    
    def __init__(self, input_file: Path, sheet_name: str, total_points: float, raw_score_per_question: float):
        """Initialize the quiz processor with quiz parameters.
        
        Args:
            input_file: Path to the input Excel file
            sheet_name: Name of the sheet containing quiz data
            total_points: Total points for the adjusted quiz score
            raw_score_per_question: Raw score possible per question
        """
        self.input_file = input_file
        self.sheet_name = sheet_name
        self.total_points = total_points
        self.raw_score_per_question = raw_score_per_question
        self.df = None
        self.question_numbers = []
        self.max_possible_raw_total = 0
        self._load_data()
    
    def _load_data(self):
        """Load data from Excel file and extract question numbers."""
        self.df = pd.read_excel(self.input_file, sheet_name=self.sheet_name)
        self.question_numbers = self._extract_question_numbers()
        self.max_possible_raw_total = len(self.question_numbers) * self.raw_score_per_question
    
    def _extract_question_numbers(self) -> list:
        """Extract unique question numbers from column names."""
        question_numbers = set()
        for col in self.df.columns:
            match = re.match(r'(\d+)_score', col.lower())
            if match:
                question_numbers.add(int(match.group(1)))
        return sorted(list(question_numbers))
    
    def _get_team_scores(self, team_data) -> tuple:
        """Calculate team scores from the first student's data.
        
        Returns:
            tuple: (earned_raw_scores, team_raw_total, team_adjusted_total)
        """
        first_student = team_data.iloc[0]
        earned_raw_scores = []
        
        # Get team scores using the first student's data
        for q_num in self.question_numbers:
            score_col = f"{q_num}_Score"
            if score_col in self.df.columns:
                earned_raw_score = float(first_student[score_col])
                earned_raw_scores.append(earned_raw_score)
        
        # Calculate totals
        team_raw_total = sum(earned_raw_scores)
        team_adjusted_total = (team_raw_total * self.total_points) / self.max_possible_raw_total
        
        return earned_raw_scores, team_raw_total, team_adjusted_total
    
    def _calculate_adjusted_scores(self, earned_raw_scores: list) -> list:
        """Calculate adjusted scores for individual questions."""
        points_per_question = self.total_points / len(self.question_numbers)
        return [
            (earned_score * points_per_question) / self.raw_score_per_question 
            for earned_score in earned_raw_scores
        ]
    
    def process_data(self) -> tuple:
        """Process quiz data and calculate scores.
        
        Returns:
            tuple: (results, question_numbers, max_possible_raw_total)
        """
        results = []
        
        # Group by team
        for team_name, team_data in self.df.groupby('Team'):
            # Get team scores
            earned_raw_scores, team_raw_total, team_adjusted_total = self._get_team_scores(team_data)
            adjusted_scores = self._calculate_adjusted_scores(earned_raw_scores)
            
            # Process each student in the team
            for _, student in team_data.iterrows():
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
        
        return results, self.question_numbers, self.max_possible_raw_total
    
    @staticmethod
    def create_output_excel(results: list, question_numbers: list, output_file: Path):
        """Create the output Excel file with the processed data."""
        output_data = []
        current_team = None
        
        for result in results:
            # Show team info only for first student in team
            is_first_in_team = result['Team Name'] != current_team
            
            row = {
                'Team Name': result['Team Name'] if is_first_in_team else '',
                'Team Raw Total': result['Team Raw Total'] if is_first_in_team else '',
                'Team Adjusted Total': result['Team Adjusted Total'] if is_first_in_team else '',
                'Student ID': result['Student ID'],
                'Student Name': result['Student Name'],
                'Email Address': result['Email Address'],
                'Student Raw Total': result['Student Raw Total'],
                'Student Adjusted Total': result['Student Adjusted Total']
            }
            current_team = result['Team Name']
            
            # Add individual question scores
            for i, (raw, adjusted) in enumerate(zip(result['Raw Scores'], result['Adjusted Scores']), 1):
                row[f'Q{i} Raw Score'] = raw
                row[f'Q{i} Adjusted Score'] = adjusted
            
            output_data.append(row)
        
        # Create DataFrame and save to Excel
        df_output = pd.DataFrame(output_data)
        df_output.to_excel(output_file, index=False)