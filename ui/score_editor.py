"""Module for handling score editing operations."""
from typing import List, Tuple, Optional
import pandas as pd
from .input_validator import get_validated_input
from .menu_handler import MenuHandler
from .score_change import ScoreChange


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
                if not should_exit_without_processing:
                    # Record changes in processor before processing
                    self.processor.record_score_changes(self.score_changes)
                return not should_exit_without_processing