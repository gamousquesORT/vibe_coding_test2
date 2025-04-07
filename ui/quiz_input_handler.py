"""Module for handling quiz parameter inputs."""
from typing import Optional, Tuple
from .input_validator import get_validated_input, validate_positive_float
from .menu_handler import MenuHandler


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
    def get_user_inputs(cls) -> Optional[Tuple[str, float, float]]:
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