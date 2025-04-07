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


class MenuHandler:
    """Class for handling menu operations and display."""
    
    @staticmethod
    def handle_menu(options: List[str], prompt: str = "Enter your choice") -> int:
        """Display menu and get valid choice."""
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
    
    @staticmethod
    def display_processing_start(input_file: Path) -> None:
        """Display processing start message."""
        print("\nQuiz Score Processing Tool")
        print("-" * 30)
        print(f"\nProcessing input file: {input_file.name}")

    @staticmethod
    def display_processing_results(num_questions: int, raw_score_per_question: float,
                                 max_raw_total: float, total_points: float) -> None:
        """Display processing results."""
        print(f"\nFound {num_questions} questions")
        print(f"Raw score possible per question: {raw_score_per_question} points")
        print(f"Maximum raw score possible: {max_raw_total} points")
        print(f"Total adjusted points: {total_points} points")

    @staticmethod
    def display_completion(output_file: Path) -> None:
        """Display completion message."""
        print(f"\nProcessing complete. Output saved to {output_file}")

    @staticmethod
    def display_team_list(teams: List[str]) -> None:
        """Display numbered list of teams."""
        print("\nAvailable Teams:")
        for idx, team in enumerate(teams, 1):
            print(f"{idx}. {team}")

    @staticmethod
    def display_score_changes(changes: List[ScoreChange]) -> None:
        """Display summary of all score changes made."""
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


class QuizInputHandler:
    """Class for handling quiz parameter inputs."""

    @staticmethod
    def get_quiz_name() -> str:
        """Get quiz name from user input."""
        return input("\nEnter the quiz name: ").strip()

    @staticmethod
    def get_raw_score_per_question() -> float:
        """Get raw score per question from user with validation."""
        return get_validated_input(
            "Enter the total raw score possible per question: ",
            validate_positive_float,
            "Raw score must be greater than 0. Please try again."
        )

    @staticmethod
    def get_total_points() -> float:
        """Get total points for the quiz from user with validation."""
        return get_validated_input(
            "Enter the total points for the quiz: ",
            validate_positive_float,
            "Total points must be greater than 0. Please try again."
        )

    @staticmethod
    def confirm_inputs(quiz_name: str, raw_score: float, total_points: float) -> tuple:
        """Allow user to confirm or modify input values."""
        options = [
            "Proceed with these values",
            "Change quiz name",
            "Change raw score per question", 
            "Change total points",
            "Exit without processing"
        ]
        
        while True:
            print("\nPlease confirm your inputs:")
            choice = MenuHandler.handle_menu(options, "Enter your choice")
            
            if choice == 0:
                return quiz_name, raw_score, total_points, True, False
            elif choice == 1:
                quiz_name = QuizInputHandler.get_quiz_name()
            elif choice == 2:
                raw_score = QuizInputHandler.get_raw_score_per_question()
            elif choice == 3:
                total_points = QuizInputHandler.get_total_points()
            elif choice == 4:
                return quiz_name, raw_score, total_points, True, True

    @classmethod
    def get_user_inputs(cls) -> Optional[tuple]:
        """Get all user inputs with confirmation."""
        quiz_name = cls.get_quiz_name()
        raw_score = cls.get_raw_score_per_question()
        total_points = cls.get_total_points()
        
        confirmed = False
        while not confirmed:
            quiz_name, raw_score, total_points, confirmed, should_exit = cls.confirm_inputs(
                quiz_name, raw_score, total_points
            )
            if should_exit:
                print("\nExiting without processing...")
                return None
        
        return quiz_name, raw_score, total_points


class FileHandler:
    """Class for handling file operations."""

    @staticmethod
    def get_input_file() -> Optional[Path]:
        """Get the most recent Excel file from the input directory.
        Creates input directory if it doesn't exist.
        """
        input_dir = Path('inputdata')
        input_dir.mkdir(exist_ok=True)
        
        input_files = list(input_dir.glob('*.xlsx'))
        if not input_files:
            print("\nNo Excel files found in the input directory.")
            print(f"Please place your Excel files in: {input_dir.absolute()}")
            return None
        
        return max(input_files, key=lambda x: x.stat().st_mtime)

    @staticmethod
    def get_output_file(quiz_name: str) -> Path:
        """Generate output file path and ensure output directory exists."""
        output_dir = Path('outputdata')
        output_dir.mkdir(exist_ok=True)
        return output_dir / f"{quiz_name}.xlsx"


def display_processing_start(input_file: Path) -> None:
    """Display processing start message."""
    MenuHandler.display_processing_start(input_file)


def display_processing_results(num_questions: int, raw_score_per_question: float,
                             max_raw_total: float, total_points: float) -> None:
    """Display processing results."""
    MenuHandler.display_processing_results(num_questions, raw_score_per_question, max_raw_total, total_points)


def display_completion(output_file: Path) -> None:
    """Display completion message."""
    MenuHandler.display_completion(output_file)


class ScoreEditor:
    """Class for handling score editing operations."""

    def __init__(self, processor):
        """Initialize score editor with quiz processor."""
        self.processor = processor
        self.teams = sorted(processor.df['Team'].unique())
        self.score_changes = []

    def get_question_number(self) -> Optional[int]:
        """Get validated question number from user."""
        def validate_question(value: str) -> Tuple[bool, Optional[int]]:
            try:
                q_num = int(value)
                return q_num in self.processor.question_numbers, q_num
            except ValueError:
                return False, None
        
        return get_validated_input(
            "Enter question number: ",
            validate_question,
            "Please enter a valid question number."
        )

    def get_new_score(self, max_score: float, old_score: float) -> Optional[float]:
        """Get validated new score from user."""
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

    def get_team_by_number(self) -> Optional[str]:
        """Get team name by selecting a number from the list."""
        MenuHandler.display_team_list(self.teams)
        
        def validate_team_number(value: str) -> Tuple[bool, Optional[str]]:
            try:
                choice = int(value)
                return 1 <= choice <= len(self.teams), self.teams[choice - 1] if 1 <= choice <= len(self.teams) else None
            except ValueError:
                return False, None
        
        return get_validated_input(
            "\nEnter team number: ",
            validate_team_number,
            f"Please enter a number between 1 and {len(self.teams)}."
        )

    def update_team_score(self, change: ScoreChange) -> None:
        """Update a team's score and record the change."""
        score_col = f"{change.question_number}_Score"
        self.processor.df.loc[self.processor.df['Team'] == change.team_name, score_col] = change.new_score
        print(f"\nUpdated score for team '{change.team_name}', question {change.question_number} "
              f"from {change.old_score:.1f} to {change.new_score:.1f}")

    def process_score_edit(self) -> bool:
        """Process a single score edit operation."""
        team_name = self.get_team_by_number()
        if team_name is None:
            return False
            
        q_num = self.get_question_number()
        if q_num is None:
            return False
            
        score_col = f"{q_num}_Score"
        old_score = float(self.processor.df.loc[self.processor.df['Team'] == team_name, score_col].iloc[0])
        new_score = self.get_new_score(self.processor.raw_score_per_question, old_score)
        
        if new_score is not None:
            change = ScoreChange(team_name, q_num, old_score, new_score)
            self.update_team_score(change)
            self.score_changes.append(change)
            return True
        return False

    def display_team_scores(self, team_name: str) -> None:
        """Display all scores for a specific team."""
        team_data = self.processor.df[self.processor.df['Team'] == team_name]
        if team_data.empty:
            print(f"\nNo data found for team {team_name}")
            return
            
        print(f"\nScores for team {team_name}:")
        print("-" * 40)
        
        for q_num in self.processor.question_numbers:
            score_col = f"{q_num}_Score"
            score = float(team_data[score_col].iloc[0])
            print(f"Question {q_num}: {score:.1f}/{self.processor.raw_score_per_question:.1f}")
        print("-" * 40)

    def process_view_scores(self) -> None:
        """Process the view scores operation."""
        team_name = self.get_team_by_number()
        if team_name is not None:
            self.display_team_scores(team_name)

    def handle_score_editing(self) -> Tuple[bool, bool]:
        """Handle the score editing menu options."""
        options = [
            "Proceed with processing",
            "Edit team scores",
            "View team scores",
            "View changes", 
            "Exit without processing"
        ]
        choice = MenuHandler.handle_menu(options, "Enter your choice")
        
        if choice == 0:
            MenuHandler.display_score_changes(self.score_changes)
            return input("\nProceed with these changes? (y/n): ").strip().lower() == 'y', False
        elif choice == 1:
            self.process_score_edit()
            return False, False
        elif choice == 2:
            self.process_view_scores()
            return False, False
        elif choice == 3:
            MenuHandler.display_score_changes(self.score_changes)
            return False, False
        else:
            print("\nExiting without processing...")
            return True, True

    def edit_scores(self) -> bool:
        """Main entry point for score editing."""
        while True:
            should_exit, should_exit_without_processing = self.handle_score_editing()
            if should_exit:
                return not should_exit_without_processing


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
        "View team scores",
        "View changes", 
        "Proceed with processing",
        "Exit without processing"
    ]
    choice = MenuHandler.handle_menu(options, "Enter your choice")
    
    if choice == 0:
        process_score_edit(processor, teams, score_changes)
        return False, False
    elif choice == 1:
        process_view_scores(processor, teams)
        return False, False
    elif choice == 2:
        MenuHandler.display_score_changes(score_changes)
        return False, False
    elif choice == 3:
        MenuHandler.display_score_changes(score_changes)
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
    MenuHandler.display_team_list(teams)


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
    MenuHandler.display_score_changes(changes)


def display_team_scores(processor, team_name: str) -> None:
    """Display all scores for a specific team.
    
    Args:
        processor: QuizProcessor instance
        team_name: Name of the team to display scores for
    """
    team_data = processor.df[processor.df['Team'] == team_name]
    if team_data.empty:
        print(f"\nNo data found for team {team_name}")
        return
        
    print(f"\nScores for team {team_name}:")
    print("-" * 40)
    
    for q_num in processor.question_numbers:
        score_col = f"{q_num}_Score"
        score = float(team_data[score_col].iloc[0])
        print(f"Question {q_num}: {score:.1f}/{processor.raw_score_per_question:.1f}")
    print("-" * 40)


def process_view_scores(processor, teams: List[str]) -> None:
    """Process the view scores operation.
    
    Args:
        processor: QuizProcessor instance
        teams: List of team names
    """
    team_name = get_team_by_number(teams)
    if team_name is not None:
        display_team_scores(processor, team_name)