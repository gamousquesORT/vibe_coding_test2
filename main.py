"""Main entry point for the quiz processing application."""
from quiz_processor import QuizProcessor
from user_interface import (
    get_user_inputs,
    get_input_file,
    get_output_file,
    display_processing_start,
    display_processing_results,
    display_completion
)


def main():
    """Main entry point for the application."""
    try:
        # Get input file
        input_file = get_input_file()
        display_processing_start(input_file)
        
        # Get user inputs with confirmation
        quiz_name, raw_score_per_question, total_points = get_user_inputs()
        
        # Initialize and process data
        processor = QuizProcessor(
            input_file=input_file,
            sheet_name='Team Analysis',
            total_points=total_points,
            raw_score_per_question=raw_score_per_question
        )
        
        results, question_numbers, max_possible_raw_total = processor.process_data()
        
        # Display results
        display_processing_results(
            len(question_numbers),
            raw_score_per_question,
            max_possible_raw_total,
            total_points
        )
        
        # Generate output
        output_file = get_output_file(quiz_name)
        QuizProcessor.create_output_excel(results, question_numbers, output_file)
        display_completion(output_file)
        
    except Exception as e:
        print(f"\nError processing quiz data: {str(e)}")
        return


if __name__ == '__main__':
    main()