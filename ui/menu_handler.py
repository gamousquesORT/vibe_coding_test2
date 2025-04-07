"""Module for handling menu operations and display."""
from pathlib import Path
from typing import List
from .input_validator import get_validated_input
from .score_change import ScoreChange


class MenuHandler:
    """Class for handling menu operations and display."""
    
    @staticmethod
    def handle_menu(options: List[str], prompt: str = "Enter your choice") -> int:
        """Display menu and get valid choice."""
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
        
        def validate_menu_choice(value: str):
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