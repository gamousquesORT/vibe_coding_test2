"""Main entry point for the quiz processing application."""
from quiz_processor import process_quiz_data, create_output_excel
from user_interface import (
    get_quiz_name,
    get_raw_score_per_question,
    get_total_points,
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
        
        # Get user inputs
        quiz_name = get_quiz_name()
        raw_score_per_question = get_raw_score_per_question()
        total_points = get_total_points()
        
        # Process data
        results, question_numbers, max_possible_raw_total = process_quiz_data(
            input_file,
            sheet_name='Team Analysis',
            total_points=total_points,
            raw_score_per_question=raw_score_per_question
        )
        
        # Display results
        display_processing_results(
            len(question_numbers),
            raw_score_per_question,
            max_possible_raw_total,
            total_points
        )
        
        # Generate output
        output_file = get_output_file(quiz_name)
        create_output_excel(results, question_numbers, output_file)
        display_completion(output_file)
        
    except Exception as e:
        print(f"\nError processing quiz data: {str(e)}")
        return


if __name__ == '__main__':
    main()