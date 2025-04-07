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


def confirm_inputs(quiz_name: str, raw_score: float, total_points: float) -> tuple:
    """Allow user to confirm or modify input values.
    
    Returns:
        tuple: (quiz_name, raw_score, total_points, confirmed)
    """
    while True:
        print("\nPlease confirm your inputs:")
        print(f"1. Quiz name: {quiz_name}")
        print(f"2. Raw score per question: {raw_score}")
        print(f"3. Total points: {total_points}")
        print("\nWould you like to:")
        print("1. Proceed with these values")
        print("2. Change quiz name")
        print("3. Change raw score per question")
        print("4. Change total points")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            return quiz_name, raw_score, total_points, True
        elif choice == "2":
            quiz_name = get_quiz_name()
        elif choice == "3":
            raw_score = get_raw_score_per_question()
        elif choice == "4":
            total_points = get_total_points()
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def get_user_inputs() -> tuple:
    """Get all user inputs with confirmation.
    
    Returns:
        tuple: (quiz_name, raw_score_per_question, total_points)
    """
    quiz_name = get_quiz_name()
    raw_score = get_raw_score_per_question()
    total_points = get_total_points()
    
    confirmed = False
    while not confirmed:
        quiz_name, raw_score, total_points, confirmed = confirm_inputs(
            quiz_name, raw_score, total_points
        )
    
    return quiz_name, raw_score, total_points


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


def display_team_list(teams):
    """Display numbered list of teams.
    
    Args:
        teams: List of team names
    """
    print("\nAvailable Teams:")
    for idx, team in enumerate(teams, 1):
        print(f"{idx}. {team}")


def get_team_by_number(teams):
    """Get team name by selecting a number from the list.
    
    Args:
        teams: List of team names
    
    Returns:
        str: Selected team name or None if invalid selection
    """
    display_team_list(teams)
    
    try:
        choice = int(input("\nEnter team number: ").strip())
        if 1 <= choice <= len(teams):
            return teams[choice - 1]
        print(f"Please enter a number between 1 and {len(teams)}.")
    except ValueError:
        print("Please enter a valid number.")
    return None


def edit_team_scores(processor):
    """Allow user to edit team scores before processing.
    
    Args:
        processor: QuizProcessor instance with loaded data
    """
    teams = sorted(processor.df['Team'].unique())
    
    while True:
        print("\nScore Editing Mode")
        print("-----------------")
        print("1. Edit team scores")
        print("2. Proceed with processing")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "2":
            break
        elif choice == "1":
            # Get team by number
            team_name = get_team_by_number(teams)
            if team_name is None:
                continue
            
            # Get question number
            try:
                q_num = int(input("Enter question number: ").strip())
                if q_num not in processor.question_numbers:
                    print(f"Question {q_num} not found.")
                    continue
            except ValueError:
                print("Please enter a valid question number.")
                continue
            
            # Get new score
            try:
                new_score = float(input(f"Enter new raw score (0-{processor.raw_score_per_question}): ").strip())
                if not 0 <= new_score <= processor.raw_score_per_question:
                    print(f"Score must be between 0 and {processor.raw_score_per_question}.")
                    continue
            except ValueError:
                print("Please enter a valid score.")
                continue
            
            # Update score in dataframe
            score_col = f"{q_num}_Score"
            processor.df.loc[processor.df['Team'] == team_name, score_col] = new_score
            print(f"\nUpdated score for team '{team_name}', question {q_num} to {new_score}")
        else:
            print("Invalid choice. Please enter 1 or 2.")