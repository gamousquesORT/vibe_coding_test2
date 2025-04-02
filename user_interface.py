"""Module for handling user interaction and input validation."""
from pathlib import Path


def get_quiz_name():
    """Get quiz name from user input."""
    return input("\nEnter the quiz name: ").strip()


def get_raw_score_per_question():
    """Get raw score per question from user with validation."""
    while True:
        try:
            raw_score = float(input("Enter the total raw score possible per question: ").strip())
            if raw_score <= 0:
                print("Raw score must be greater than 0. Please try again.")
                continue
            return raw_score
        except ValueError:
            print("Please enter a valid number for raw score.")


def get_total_points():
    """Get total points for the quiz from user with validation."""
    while True:
        try:
            total_points = float(input("Enter the total points for the quiz: ").strip())
            if total_points <= 0:
                print("Total points must be greater than 0. Please try again.")
                continue
            return total_points
        except ValueError:
            print("Please enter a valid number for total points.")


def get_input_file():
    """Get the most recent Excel file from the input directory."""
    input_dir = Path('inputdata')
    input_files = list(input_dir.glob('*.xlsx'))
    
    if not input_files:
        raise FileNotFoundError("No Excel files found in the input directory")
    
    return max(input_files, key=lambda x: x.stat().st_mtime)


def get_output_file(quiz_name):
    """Generate output file path and ensure output directory exists."""
    output_dir = Path('outputdata')
    output_dir.mkdir(exist_ok=True)
    return output_dir / f"{quiz_name}.xlsx"


def display_processing_start(input_file):
    """Display processing start message."""
    print("\nQuiz Score Processing Tool")
    print("-" * 30)
    print(f"\nProcessing input file: {input_file.name}")


def display_processing_results(num_questions, raw_score_per_question, max_raw_total, total_points):
    """Display processing results."""
    print(f"\nFound {num_questions} questions")
    print(f"Raw score possible per question: {raw_score_per_question} points")
    print(f"Maximum raw score possible: {max_raw_total} points")
    print(f"Total adjusted points: {total_points} points")


def display_completion(output_file):
    """Display completion message."""
    print(f"\nProcessing complete. Output saved to {output_file}")