# Code Changes Log

## April 2, 2025 2:35 PM
- Created initial `process_quiz.py` script with the following features:
  - Extracts question numbers from column names using regex
  - Processes quiz data and calculates both raw and adjusted scores
  - Groups data by teams and calculates team totals and averages
  - Generates output Excel file with all required columns
  - Command-line interface for quiz name and total points input
  - Automatic input file detection (uses most recent Excel file)
  - Creates output directory if it doesn't exist

## April 2, 2025 3:00 PM
- Updated `process_quiz.py` to use console input instead of command line arguments:
  - Added user-friendly prompts for quiz name and total points
  - Added input validation for total points (must be positive number)
  - Improved error handling and user feedback
  - Added processing status messages

## April 2, 2025 3:15 PM
- Modified quiz value calculation in `process_quiz.py`:
  - Changed user input to request points per question instead of total points
  - Added function `get_total_points` to calculate total quiz value
  - Updated score adjustment logic to use per-question value
  - Added informative messages about number of questions and total points
  - Improved calculation of adjusted scores based on question value

## April 2, 2025 3:30 PM
- Removed team average calculations from `process_quiz.py`:
  - Removed team average computation logic
  - Removed team average fields from output Excel file
  - Simplified team score processing
  - Maintained raw and adjusted totals for teams and students

## April 2, 2025 3:45 PM
- Fixed team score calculation in `process_quiz.py`:
  - Modified logic to use first student's scores as team scores
  - Updated all students in a team to have the same scores
  - Corrected team total calculations to reflect team quiz nature
  - Ensured student totals match team totals since it's a team quiz

## April 2, 2025 4:00 PM
- Fixed student and team raw total calculations in `process_quiz.py`:
  - Changed to use sum() for raw score totals instead of multiplication
  - Ensured Student Adjusted Total is calculated by summing adjusted question scores
  - Improved code organization and comments for score calculations
  - Maintained team-based scoring while fixing calculation method

## April 2, 2025 4:15 PM
- Fixed student adjusted total calculation in `process_quiz.py`:
  - Changed to use team adjusted total for student adjusted total
  - Simplified score calculation logic
  - Improved code organization to calculate team totals first
  - Ensured consistent adjusted scores across team members

## April 2, 2025 4:30 PM
- Completely redesigned score adjustment calculation in `process_quiz.py`:
  - Removed points per question approach
  - Added `calculate_adjusted_score` function implementing rule of three
  - Modified score calculations to use total quiz points directly
  - Added proper proportional scaling for both individual questions and totals
  - Updated console output to show maximum raw score and adjusted points

## April 2, 2025 4:45 PM
- Fixed adjusted total calculations in `process_quiz.py`:
  - Corrected rule of three implementation for total score adjustment
  - Added points per question calculation derived from total points
  - Updated console output to show points per question
  - Individual question scores now properly scaled based on total points
  - Improved code organization and comments for clarity

## April 2, 2025 5:00 PM
- Updated quiz score calculation in `process_quiz.py`:
  - Added raw score per question input from user
  - Modified raw score calculation to use actual raw score instead of assuming 1
  - Updated maximum possible raw total calculation (questions × raw_score_per_question)
  - Adjusted console output to show raw score per question
  - Maintained proper rule of three calculation with new raw scores

## April 2, 2025 5:15 PM
- Updated score calculation logic in `process_quiz.py`:
  - Distinguished between total raw score possible and earned score
  - Changed to store both earned percentages and earned raw scores
  - Fixed raw score calculation: earned_percentage * raw_score_per_question
  - Improved variable names for clarity
  - Updated prompts to clarify raw score input

## April 2, 2025 5:30 PM
- Fixed score calculation logic in `process_quiz.py`:
  - Now correctly using raw scores directly from Excel sheet
  - Removed incorrect percentage calculation
  - Fixed rule of three calculations for both team and individual scores
  - Updated comments to reflect correct score handling

## April 2, 2025 6:00 PM
- Refactored code into separate modules:
  - Created `quiz_processor.py` for Excel processing and score calculations
  - Created `user_interface.py` for user interaction and input handling
  - Created `main.py` as the application entry point
  - Removed original `process_quiz.py`
  - Improved code organization and maintainability
  - Added proper docstrings and comments

## April 2, 2025 6:15 PM
- Added input confirmation system:
  - Created `confirm_inputs` function for reviewing and modifying inputs
  - Added `get_user_inputs` function to handle the complete input flow
  - Updated main.py to use new input confirmation system
  - Improved user experience with clear input review options

## April 2, 2025 6:45 PM
- Modified Excel output format:
  - Changed team name display to show only on first student row
  - Maintained all other team and student data
  - Improved readability of team groupings in output
  - Added tracking of current team to handle repetition