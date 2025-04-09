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

## April 2, 2025 7:00 PM
- Enhanced Excel output format:
  - Modified team totals to show only on first student row
  - Team Raw Total and Team Adjusted Total now appear once per team
  - Improved readability by eliminating duplicate values
  - Consistent handling of all team-specific information

[2025-04-07 14:00] Tested code execution
- Ran main.py successfully
- Processed input file with 12 questions
- Generated output file q1.xlsx
- Confirmed correct calculation of raw scores and scaling

[2025-04-07 14:30] Added score editing functionality
- Added edit_team_scores function to user_interface.py
- Added score editing step in main.py before processing
- Implemented score validation and error handling
- Added user interface for team score modifications

[2025-04-07 14:45] Added team number selection
- Added display_team_list function to show numbered team list
- Added get_team_by_number function for team selection by number
- Updated edit_team_scores to use numbered team selection
- Improved user experience with clearer team selection interface

[2025-04-07 15:00] Added score change tracking
- Added display_score_changes function to show summary of changes
- Enhanced edit_team_scores with change tracking
- Added view changes option in editing menu
- Added confirmation step with changes summary
- Added score difference indicators (+/-) in summary

[2025-04-07 15:30] Added exit options to all user input loops
- Added "Exit without processing" option to initial input confirmation
- Added exit option to score editing menu
- Updated return types to handle early exits
- Added clean exit paths throughout the application
- Added change summary display before exiting from editing

[2025-04-07 15:45] Updated README documentation
- Added score editing capabilities section
- Added detailed feature descriptions
- Updated usage instructions with new steps
- Added input validation details
- Added exit options documentation
- Updated setup instructions to use requirements.txt

[2025-04-07 16:00] Added team score visualization
- Added display_team_scores function to show current scores
- Added process_view_scores function to handle team selection
- Updated score editing menu with "View team scores" option
- Added score display showing current/maximum score for each question
- Enhanced user interface with clear score presentation

[2025-04-07 16:15] Improved folder handling
- Modified get_input_file to create input directory if missing
- Added user-friendly message when no Excel files found
- Changed error handling to return None instead of throwing exception
- Updated main.py to gracefully handle missing input files
- Added absolute path display in user message for clarity

[2025-04-07 16:30] Test run verification
- Successfully ran program with live data
- Verified input file processing
- Tested menu navigation and user input handling
- Confirmed score editing interface works
- Validated output file generation

[2025-04-07 16:45] Standardized menu options
- Moved "Proceed with processing" to first position in score editing menu
- Updated handle_score_editing function to match new menu order
- Maintained all existing functionality while improving consistency
- Verified changes with error checking

[2025-04-07 17:00] Test run with standardized menus
- Verified consistent menu option placement
- Successfully processed new quiz with test data
- Confirmed proper menu flow and navigation
- Generated output file r1.xlsx correctly
- Validated all user input handling

[2025-04-07 17:15] Committed changes
- Created commit on feat_visualize_teams_scores branch
- Included team score visualization feature
- Added menu standardization changes
- Updated input/output folder handling
- Added documentation updates
- Verified all changes with successful test runs

[2025-04-07 17:30] Major code refactoring
- Extracted FileHandler class for file operations
- Created MenuHandler class for menu and display logic
- Added QuizInputHandler class for quiz parameter management
- Implemented ScoreEditor class for score editing operations
- Updated main.py to use new class structure
- Removed duplicate standalone functions
- Verified no errors in refactored code

[2025-04-07 17:45] Separated UI modules
- Created ui package with separate modules for each class
- Moved input validation to input_validator.py
- Created score_change.py for ScoreChange dataclass
- Moved file operations to file_handler.py
- Created menu_handler.py for menu operations
- Moved quiz input handling to quiz_input_handler.py
- Created score_editor.py for score editing operations
- Verified all functionality working with test run

[2025-04-08 14:00] Refactored UI code into modular structure
- Moved duplicated code from user_interface.py to specialized UI modules
- Organized UI code into focused modules:
  - file_handler.py: File operations
  - input_validator.py: Input validation
  - menu_handler.py: Menu displays and navigation
  - quiz_input_handler.py: Quiz parameter input
  - score_change.py: Score change tracking
  - score_editor.py: Score editing operations
- Added new view scores feature
- Updated user_interface.py to use new modules
- Improved code organization and reduced duplication

[2025-04-08 14:30] Added score highlighting in output Excel
- Added score change tracking in QuizProcessor
- Modified Excel output to highlight changed scores
- Added yellow highlighting for modified raw and adjusted scores
- Updated score editor to record changes in processor
- Improved Excel writer to handle cell formatting

[2025-04-08 15:00] Added score highlighting in Excel output
- Added highlighting for changed scores in output Excel
- Refactored QuizProcessor for better code organization
- Split Excel output logic into focused methods
- Added proper type hints throughout
- Updated dependencies in requirements.txt
- Improved error handling in file operations
- Tested functionality with sample quiz data

[2025-04-08 15:30] Fixed score highlighting for team members
- Modified _highlight_changed_scores to track current team
- Ensured highlighting applies to all team members
- Fixed team name tracking for empty rows
- Removed unnecessary parameter from save_to_excel
- Tested with multiple teams and verified highlighting

[2025-04-09 11:00] Fixed syntax errors in quiz_processor.py
- Fixed method indentation
- Added missing import for ScoreChange class
- Verified proper type hints for all methods
- Confirmed no remaining syntax errors

[2025-04-09 11:30] Refactored to Web Interface
- Migrated from terminal to Streamlit web interface
- Added streamlit_app.py with interactive features
- Removed duplicated code from user_interface.py
- Updated requirements.txt with web dependencies
- Improved code organization in QuizProcessor
- Added proper type hints throughout codebase
- Verified web interface functionality