"""Module for handling user interaction and input validation."""
from pathlib import Path
from typing import Callable, List, Tuple, Optional, Any
from dataclasses import dataclass


@dataclass
class ScoreChange:
    """Class to hold score change information."""
    team_name: str
    question_number: int
    old_score: float
    new_score: float
    
    @property
    def difference(self) -> float:
        """Calculate score difference."""
        return self.new_score - self.old_score


def get_validated_input(prompt: str, validator: Callable[[str], Tuple[bool, Any]], 
                       error_message: str) -> Any:
    """Get and validate user input.
    
    Args:
        prompt: Input prompt to display
        validator: Function that validates input and returns (is_valid, value)
        error_message: Message to display on invalid input
    
    Returns:
        Validated input value
    """
    while True:
        try:
            user_input = input(prompt).strip()
            is_valid, value = validator(user_input)
            if is_valid:
                return value
            print(error_message)
        except Exception:
            print(error_message)


def validate_positive_float(value: str) -> Tuple[bool, Optional[float]]:
    """Validate input is a positive float.
    
    Args:
        value: Input string to validate
    
    Returns:
        Tuple of (is_valid, converted_value)
    """
    try:
        float_val = float(value)
        return float_val > 0, float_val
    except ValueError:
        return False, None


def handle_menu(options: List[str], prompt: str = "Enter your choice") -> int:
    """Display menu and get valid choice.
    
    Args:
        options: List of menu options to display
        prompt: Input prompt
    
    Returns:
        Selected menu index (0-based)
    """
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    
    def validate_menu_choice(value: str) -> Tuple[bool, Optional[int]]:
        try:
            choice = int(value)
            return 1 <= choice <= len(options), choice - 1
        except ValueError:
            return False, None
    
    return get_validated_input(
        f"\n{prompt} (1-{len(options)}): ",
        validate_menu_choice,
        f"Please enter a number between 1 and {len(options)}."
    )


def get_quiz_name() -> str:
    """Get quiz name from user input."""
    return input("\nEnter the quiz name: ").strip()


def get_raw_score_per_question() -> float:
    """Get raw score per question from user with validation."""
    return get_validated_input(
        "Enter the total raw score possible per question: ",
        validate_positive_float,
        "Raw score must be greater than 0. Please try again."
    )


def get_total_points() -> float:
    """Get total points for the quiz from user with validation."""
    return get_validated_input(
        "Enter the total points for the quiz: ",
        validate_positive_float,
        "Total points must be greater than 0. Please try again."
    )


def confirm_inputs(quiz_name: str, raw_score: float, total_points: float) -> tuple:
    """Allow user to confirm or modify input values.
    
    Returns:
        tuple: (quiz_name, raw_score, total_points, confirmed, should_exit)
    """
    options = [
        "Proceed with these values",
        "Change quiz name",
        "Change raw score per question", 
        "Change total points",
        "Exit without processing"
    ]
    
    while True:
        print("\nPlease confirm your inputs:")
        choice = handle_menu(options, "Enter your choice")
        
        if choice == 0:
            return quiz_name, raw_score, total_points, True, False
        elif choice == 1:
            quiz_name = get_quiz_name()
        elif choice == 2:
            raw_score = get_raw_score_per_question()
        elif choice == 3:
            total_points = get_total_points()
        elif choice == 4:
            return quiz_name, raw_score, total_points, True, True


def get_user_inputs() -> Optional[tuple]:
    """Get all user inputs with confirmation.
    
    Returns:
        Optional[tuple]: (quiz_name, raw_score_per_question, total_points) or None if user exits
    """
    quiz_name = get_quiz_name()
    raw_score = get_raw_score_per_question()
    total_points = get_total_points()
    
    confirmed = False
    while not confirmed:
        quiz_name, raw_score, total_points, confirmed, should_exit = confirm_inputs(
            quiz_name, raw_score, total_points
        )
        if should_exit:
            print("\nExiting without processing...")
            return None
    
    return quiz_name, raw_score, total_points


def get_input_file() -> Path:
    """Get the most recent Excel file from the input directory."""
    input_dir = Path('inputdata')
    input_files = list(input_dir.glob('*.xlsx'))
    
    if not input_files:
        raise FileNotFoundError("No Excel files found in the input directory")
    
    return max(input_files, key=lambda x: x.stat().st_mtime)


def get_output_file(quiz_name: str) -> Path:
    """Generate output file path and ensure output directory exists."""
    output_dir = Path('outputdata')
    output_dir.mkdir(exist_ok=True)
    return output_dir / f"{quiz_name}.xlsx"


def display_processing_start(input_file: Path) -> None:
    """Display processing start message."""
    print("\nQuiz Score Processing Tool")
    print("-" * 30)
    print(f"\nProcessing input file: {input_file.name}")


def display_processing_results(num_questions: int, raw_score_per_question: float,
                             max_raw_total: float, total_points: float) -> None:
    """Display processing results."""
    print(f"\nFound {num_questions} questions")
    print(f"Raw score possible per question: {raw_score_per_question} points")
    print(f"Maximum raw score possible: {max_raw_total} points")
    print(f"Total adjusted points: {total_points} points")


def display_completion(output_file: Path) -> None:
    """Display completion message."""
    print(f"\nProcessing complete. Output saved to {output_file}")


def get_question_number(processor) -> Optional[int]:
    """Get validated question number from user.
    
    Args:
        processor: QuizProcessor instance with question data
    
    Returns:
        Question number or None if invalid
    """
    def validate_question(value: str) -> Tuple[bool, Optional[int]]:
        try:
            q_num = int(value)
            return q_num in processor.question_numbers, q_num
        except ValueError:
            return False, None
    
    return get_validated_input(
        "Enter question number: ",
        validate_question,
        "Please enter a valid question number."
    )


def get_new_score(max_score: float, old_score: float) -> Optional[float]:
    """Get validated new score from user.
    
    Args:
        max_score: Maximum allowed score
        old_score: Current score value
    
    Returns:
        New score value or None if invalid
    """
    def validate_score(value: str) -> Tuple[bool, Optional[float]]:
        try:
            score = float(value)
            return 0 <= score <= max_score, score
        except ValueError:
            return False, None
    
    return get_validated_input(
        f"Enter new raw score (0-{max_score}): ",
        validate_score,
        f"Score must be between 0 and {max_score}."
    )


def update_team_score(processor, change: ScoreChange) -> None:
    """Update a team's score and record the change.
    
    Args:
        processor: QuizProcessor instance
        change: ScoreChange instance with change details
    """
    score_col = f"{change.question_number}_Score"
    processor.df.loc[processor.df['Team'] == change.team_name, score_col] = change.new_score
    print(f"\nUpdated score for team '{change.team_name}', question {change.question_number} "
          f"from {change.old_score:.1f} to {change.new_score:.1f}")


def process_score_edit(processor, teams: List[str], score_changes: List[ScoreChange]) -> bool:
    """Process a single score edit operation.
    
    Args:
        processor: QuizProcessor instance
        teams: List of team names
        score_changes: List to record changes
    
    Returns:
        bool: True if edit was successful
    """
    # Get team selection
    team_name = get_team_by_number(teams)
    if team_name is None:
        return False
        
    # Get question number
    q_num = get_question_number(processor)
    if q_num is None:
        return False
        
    # Get and validate new score
    score_col = f"{q_num}_Score"
    old_score = float(processor.df.loc[processor.df['Team'] == team_name, score_col].iloc[0])
    new_score = get_new_score(processor.raw_score_per_question, old_score)
    
    if new_score is not None:
        change = ScoreChange(team_name, q_num, old_score, new_score)
        update_team_score(processor, change)
        score_changes.append(change)
        return True
    return False


def handle_score_editing(processor, teams: List[str], score_changes: list) -> Tuple[bool, bool]:
    """Handle the score editing menu options.
    
    Args:
        processor: QuizProcessor instance
        teams: List of team names
        score_changes: List to record changes
    
    Returns:
        Tuple[bool, bool]: (should_exit_editing, should_exit_without_processing)
    """
    options = [
        "Edit team scores",
        "View changes", 
        "Proceed with processing",
        "Exit without processing"
    ]
    choice = handle_menu(options, "Enter your choice")
    
    if choice == 0:
        process_score_edit(processor, teams, score_changes)
        return False, False
    elif choice == 1:
        display_score_changes(score_changes)
        return False, False
    elif choice == 2:
        display_score_changes(score_changes)
        return input("\nProceed with these changes? (y/n): ").strip().lower() == 'y', False
    else:
        print("\nExiting without processing...")
        return True, True


def edit_team_scores(processor) -> bool:
    """Allow user to edit team scores before processing.
    
    Args:
        processor: QuizProcessor instance with loaded data
    
    Returns:
        bool: True if should continue processing, False to exit without processing
    """
    teams = sorted(processor.df['Team'].unique())
    score_changes = []
    
    while True:
        should_exit, should_exit_without_processing = handle_score_editing(processor, teams, score_changes)
        if should_exit:
            return not should_exit_without_processing


def display_team_list(teams: List[str]) -> None:
    """Display numbered list of teams.
    
    Args:
        teams: List of team names
    """
    print("\nAvailable Teams:")
    for idx, team in enumerate(teams, 1):
        print(f"{idx}. {team}")


def get_team_by_number(teams: List[str]) -> Optional[str]:
    """Get team name by selecting a number from the list.
    
    Args:
        teams: List of team names
    
    Returns:
        Selected team name or None if invalid selection
    """
    display_team_list(teams)
    
    def validate_team_number(value: str) -> Tuple[bool, Optional[str]]:
        try:
            choice = int(value)
            return 1 <= choice <= len(teams), teams[choice - 1] if 1 <= choice <= len(teams) else None
        except ValueError:
            return False, None
    
    return get_validated_input(
        "\nEnter team number: ",
        validate_team_number,
        f"Please enter a number between 1 and {len(teams)}."
    )


def display_score_changes(changes: List[ScoreChange]) -> None:
    """Display summary of all score changes made.
    
    Args:
        changes: List of ScoreChange objects
    """
    if not changes:
        print("\nNo score changes made.")
        return
        
    print("\nScore Changes Summary:")
    print("---------------------")
    for change in changes:
        print(f"Team {change.team_name}: Question {change.question_number} "
              f"changed from {change.old_score:.1f} to {change.new_score:.1f} "
              f"({change.difference:+.1f})")
    print("---------------------")