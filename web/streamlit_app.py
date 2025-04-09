"""Streamlit web interface for quiz processing."""
import streamlit as st
from pathlib import Path
import pandas as pd
import os
import sys

# Add project root to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from quiz_processor import QuizProcessor
from ui.score_change import ScoreChange


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'processor' not in st.session_state:
        st.session_state.processor = None
    if 'score_changes' not in st.session_state:
        st.session_state.score_changes = []
    if 'current_team' not in st.session_state:
        st.session_state.current_team = None


def display_team_scores(processor: QuizProcessor, team_name: str) -> None:
    """Display scores for a specific team."""
    team_data = processor.df[processor.df['Team'] == team_name]
    if team_data.empty:
        st.warning(f"No data found for team {team_name}")
        return

    st.subheader(f"Scores for {team_name}")
    
    # Create score table
    scores_data = []
    for q_num in processor.question_numbers:
        score_col = f"{q_num}_Score"
        score = float(team_data[score_col].iloc[0])
        scores_data.append({
            "Question": f"Question {q_num}",
            "Current Score": f"{score:.1f}",
            "Maximum Score": f"{processor.raw_score_per_question:.1f}"
        })
    
    st.table(pd.DataFrame(scores_data))


def edit_team_scores(processor: QuizProcessor):
    """Edit team scores interface."""
    teams = sorted(processor.df['Team'].unique())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Select Team")
        team_name = st.selectbox(
            "Choose a team:",
            teams,
            index=teams.index(st.session_state.current_team) if st.session_state.current_team in teams else 0
        )
        st.session_state.current_team = team_name
        
        st.subheader("Edit Score")
        question_number = st.selectbox(
            "Choose question number:",
            processor.question_numbers
        )
        
        score_col = f"{question_number}_Score"
        current_score = float(processor.df.loc[processor.df['Team'] == team_name, score_col].iloc[0])
        
        new_score = st.number_input(
            "Enter new score:",
            min_value=0.0,
            max_value=processor.raw_score_per_question,
            value=current_score,
            step=0.5
        )
        
        if st.button("Update Score"):
            if new_score != current_score:
                change = ScoreChange(team_name, question_number, current_score, new_score)
                processor.df.loc[processor.df['Team'] == team_name, score_col] = new_score
                st.session_state.score_changes.append(change)
                st.success(f"Updated score from {current_score:.1f} to {new_score:.1f}")
    
    with col2:
        display_team_scores(processor, team_name)
        
        if st.session_state.score_changes:
            st.subheader("Score Changes Summary")
            changes_data = []
            for change in st.session_state.score_changes:
                changes_data.append({
                    "Team": change.team_name,
                    "Question": f"Q{change.question_number}",
                    "From": f"{change.old_score:.1f}",
                    "To": f"{change.new_score:.1f}",
                    "Change": f"{change.difference:+.1f}"
                })
            st.table(pd.DataFrame(changes_data))


def process_quiz(processor: QuizProcessor, quiz_name: str):
    """Process quiz and generate output."""
    results, question_numbers, max_raw_total = processor.process_data()
    
    st.subheader("Processing Results")
    st.write(f"Found {len(question_numbers)} questions")
    st.write(f"Raw score possible per question: {processor.raw_score_per_question} points")
    st.write(f"Maximum raw score possible: {max_raw_total} points")
    st.write(f"Total adjusted points: {processor.total_points} points")
    
    # Generate output file
    output_file = Path("outputdata") / f"{quiz_name}.xlsx"
    output_file.parent.mkdir(exist_ok=True)
    
    # Record changes in processor if any exist
    if st.session_state.score_changes:
        processor.record_score_changes(st.session_state.score_changes)
    
    QuizProcessor.create_output_excel(results, question_numbers, output_file, processor)
    
    # Provide download link
    with open(output_file, "rb") as file:
        st.download_button(
            label="Download Processed File",
            data=file,
            file_name=output_file.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Quiz Score Processor",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("Quiz Score Processor")
    st.write("Process and edit quiz scores from Excel files.")
    
    initialize_session_state()
    
    # File upload and initial setup
    upload_col, params_col = st.columns(2)
    
    with upload_col:
        st.subheader("Upload Quiz File")
        uploaded_file = st.file_uploader(
            "Choose Excel file",
            type="xlsx",
            help="Select the Excel file containing quiz data"
        )
    
    with params_col:
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
    
    # Process uploaded file
    if uploaded_file:
        # Save uploaded file
        input_dir = Path("inputdata")
        input_dir.mkdir(exist_ok=True)
        input_path = input_dir / uploaded_file.name
        
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Initialize processor
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