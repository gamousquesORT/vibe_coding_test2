"""Main entry point for the quiz processing application."""
from quiz_processor import QuizProcessor
from user_interface import (
    FileHandler,
    MenuHandler,
    QuizInputHandler,
    ScoreEditor
)


def main():
    """Main entry point for the application."""
    try:
        # Get input file
        input_file = FileHandler.get_input_file()
        if input_file is None:
            return
        MenuHandler.display_processing_start(input_file)
        
        # Get user inputs with confirmation
        inputs = QuizInputHandler.get_user_inputs()
        if inputs is None:
            return
            
        quiz_name, raw_score_per_question, total_points = inputs
        
        # Initialize processor
        processor = QuizProcessor(
            input_file=input_file,
            sheet_name='Team Analysis',
            total_points=total_points,
            raw_score_per_question=raw_score_per_question
        )

        # Allow score editing before processing
        score_editor = ScoreEditor(processor)
        if not score_editor.edit_scores():
            print("\nExiting without processing...")
            return
        
        # Process data
        results, question_numbers, max_possible_raw_total = processor.process_data()
        
        # Display results
        MenuHandler.display_processing_results(
            len(question_numbers),
            raw_score_per_question,
            max_possible_raw_total,
            total_points
        )
        
        # Generate output
        output_file = FileHandler.get_output_file(quiz_name)
        QuizProcessor.create_output_excel(results, question_numbers, output_file)
        MenuHandler.display_completion(output_file)
        
    except Exception as e:
        print(f"\nError processing quiz data: {str(e)}")
        return


if __name__ == '__main__':
    main()