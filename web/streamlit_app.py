"""Streamlit web interface for quiz processing."""
import streamlit as st
from pathlib import Path
import pandas as pd

# Add project root to Python path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from quiz_processor import QuizProcessor
from ui.score_change import ScoreChange


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    defaults = {
        'processor': None,
        'score_changes': [],
        'current_team': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def create_score_table(processor: QuizProcessor, team_data: pd.DataFrame) -> pd.DataFrame:
    """Create a table of scores for display."""
    return pd.DataFrame([
        {
            "Question": f"Question {q_num}",
            "Current Score": f"{float(team_data[f'{q_num}_Score'].iloc[0]):.1f}",
            "Maximum Score": f"{processor.raw_score_per_question:.1f}"
        }
        for q_num in processor.question_numbers
    ])


def display_team_scores(processor: QuizProcessor, team_name: str) -> None:
    """Display scores for a specific team."""
    team_data = processor.df[processor.df['Team'] == team_name]
    if team_data.empty:
        st.warning(f"No data found for team {team_name}")
        return

    st.subheader(f"Scores for {team_name}")
    st.table(create_score_table(processor, team_data))


def create_changes_table(changes: list[ScoreChange]) -> pd.DataFrame:
    """Create a table summarizing score changes."""
    if not changes:
        return None
        
    return pd.DataFrame([
        {
            "Team": change.team_name,
            "Question": f"Q{change.question_number}",
            "From": f"{change.old_score:.1f}",
            "To": f"{change.new_score:.1f}",
            "Change": f"{change.difference:+.1f}"
        }
        for change in changes
    ])


def handle_score_update(processor: QuizProcessor, team_name: str, 
                       question_number: int, new_score: float) -> None:
    """Handle updating a team's score."""
    score_col = f"{question_number}_Score"
    current_score = float(processor.df.loc[processor.df['Team'] == team_name, score_col].iloc[0])
    
    if new_score != current_score:
        change = ScoreChange(team_name, question_number, current_score, new_score)
        processor.df.loc[processor.df['Team'] == team_name, score_col] = new_score
        st.session_state.score_changes.append(change)
        st.success(f"Updated score from {current_score:.1f} to {new_score:.1f}")


def edit_team_scores(processor: QuizProcessor) -> None:
    """Edit team scores interface."""
    teams = sorted(processor.df['Team'].unique())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Select Team")
        team_idx = teams.index(st.session_state.current_team) if st.session_state.current_team in teams else 0
        team_name = st.selectbox("Choose a team:", teams, index=team_idx)
        st.session_state.current_team = team_name
        
        st.subheader("Edit Score")
        question_number = st.selectbox("Choose question number:", processor.question_numbers)
        
        current_score = float(processor.df.loc[
            processor.df['Team'] == team_name, 
            f"{question_number}_Score"
        ].iloc[0])
        
        new_score = st.number_input(
            "Enter new score:",
            min_value=0.0,
            max_value=processor.raw_score_per_question,
            value=current_score,
            step=0.5
        )
        
        if st.button("Update Score"):
            handle_score_update(processor, team_name, question_number, new_score)
    
    with col2:
        display_team_scores(processor, team_name)
        
        changes_table = create_changes_table(st.session_state.score_changes)
        if changes_table is not None:
            st.subheader("Score Changes Summary")
            st.table(changes_table)


def save_and_process_file(processor: QuizProcessor, quiz_name: str) -> Path:
    """Save and process quiz data."""
    results, question_numbers, max_raw_total = processor.process_data()
    
    st.subheader("Processing Results")
    st.write(f"Found {len(question_numbers)} questions")
    st.write(f"Raw score possible per question: {processor.raw_score_per_question} points")
    st.write(f"Maximum raw score possible: {max_raw_total} points")
    st.write(f"Total adjusted points: {processor.total_points} points")
    
    # Generate output file
    output_file = Path("outputdata") / f"{quiz_name}.xlsx"
    output_file.parent.mkdir(exist_ok=True)
    
    if st.session_state.score_changes:
        processor.record_score_changes(st.session_state.score_changes)
    
    QuizProcessor.create_output_excel(results, question_numbers, output_file, processor)
    return output_file


def process_quiz(processor: QuizProcessor, quiz_name: str) -> None:
    """Process quiz and generate output."""
    output_file = save_and_process_file(processor, quiz_name)
    
    # Provide download link
    with open(output_file, "rb") as file:
        st.download_button(
            label="Download Processed File",
            data=file,
            file_name=output_file.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


def setup_quiz_parameters() -> tuple[str, float, float]:
    """Set up quiz parameters through user input."""
    st.subheader("Quiz Parameters")
    quiz_name = st.text_input("Quiz Name", help="Enter a name for the quiz")
    raw_score = st.number_input(
        "Raw Score per Question",
        min_value=0.1,
        value=5.0,
        help="Maximum points possible for each question"
    )
    total_points = st.number_input(
        "Total Points",
        min_value=0.1,
        value=1.5,
        help="Total points for the entire quiz"
    )
    return quiz_name, raw_score, total_points


def handle_file_upload() -> tuple[Path, str]:
    """Handle file upload and saving."""
    st.subheader("Upload Quiz File")
    uploaded_file = st.file_uploader(
        "Choose Excel file",
        type="xlsx",
        help="Select the Excel file containing quiz data"
    )
    
    if uploaded_file:
        input_dir = Path("inputdata")
        input_dir.mkdir(exist_ok=True)
        input_path = input_dir / uploaded_file.name
        
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getvalue())
            
        return input_path, uploaded_file.name
    return None, None


def main() -> None:
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Quiz Score Processor",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("Quiz Score Processor")
    st.write("Process and edit quiz scores from Excel files.")
    
    initialize_session_state()
    
    # File upload and parameter setup
    upload_col, params_col = st.columns(2)
    
    with upload_col:
        input_path, _ = handle_file_upload()
    
    with params_col:
        quiz_name, raw_score, total_points = setup_quiz_parameters()
    
    # Process uploaded file
    if input_path:
        st.session_state.processor = QuizProcessor(
            input_file=input_path,
            sheet_name='Team Analysis',
            total_points=total_points,
            raw_score_per_question=raw_score
        )
        
        # Create tabs for editing and processing
        tab1, tab2 = st.tabs(["Edit Scores", "Process Quiz"])
        
        with tab1:
            edit_team_scores(st.session_state.processor)
        
        with tab2:
            if st.button("Process Quiz"):
                if not quiz_name:
                    st.error("Please enter a quiz name")
                else:
                    process_quiz(st.session_state.processor, quiz_name)


if __name__ == "__main__":
    main()