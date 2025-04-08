"""Module for handling user interaction and input validation."""
from pathlib import Path
from typing import Optional, Tuple
from ui.file_handler import FileHandler
from ui.menu_handler import MenuHandler
from ui.quiz_input_handler import QuizInputHandler
from ui.score_editor import ScoreEditor


def get_quiz_name() -> str:
    """Get quiz name from user input."""
    return QuizInputHandler.get_quiz_name()


def get_raw_score_per_question() -> float:
    """Get raw score per question from user with validation."""
    return QuizInputHandler.get_raw_score_per_question()


def get_total_points() -> float:
    """Get total points for the quiz from user with validation."""
    return QuizInputHandler.get_total_points()


def confirm_inputs(quiz_name: str, raw_score: float, total_points: float) -> tuple:
    """Allow user to confirm or modify input values."""
    return QuizInputHandler.confirm_inputs(quiz_name, raw_score, total_points)


def get_user_inputs() -> Optional[Tuple[str, float, float]]:
    """Get all user inputs with confirmation."""
    return QuizInputHandler.get_user_inputs()


def get_input_file() -> Path:
    """Get the most recent Excel file from the input directory."""
    file = FileHandler.get_input_file()
    if file is None:
        raise FileNotFoundError("No Excel files found in the input directory")
    return file


def get_output_file(quiz_name: str) -> Path:
    """Generate output file path and ensure output directory exists."""
    return FileHandler.get_output_file(quiz_name)


def display_processing_start(input_file: Path) -> None:
    """Display processing start message."""
    MenuHandler.display_processing_start(input_file)


def display_processing_results(num_questions: int, raw_score_per_question: float,
                             max_raw_total: float, total_points: float) -> None:
    """Display processing results."""
    MenuHandler.display_processing_results(
        num_questions, raw_score_per_question, max_raw_total, total_points
    )


def display_completion(output_file: Path) -> None:
    """Display completion message."""
    MenuHandler.display_completion(output_file)


def edit_team_scores(processor) -> bool:
    """Allow user to edit team scores before processing."""
    editor = ScoreEditor(processor)
    return editor.edit_scores()