"""Module for handling file operations."""
from pathlib import Path
from typing import Optional


class FileHandler:
    """Class for handling file operations."""

    @staticmethod
    def get_input_file() -> Optional[Path]:
        """Get the most recent Excel file from the input directory.
        Creates input directory if it doesn't exist.
        """
        input_dir = Path('inputdata')
        input_dir.mkdir(exist_ok=True)
        
        input_files = list(input_dir.glob('*.xlsx'))
        if not input_files:
            print("\nNo Excel files found in the input directory.")
            print(f"Please place your Excel files in: {input_dir.absolute()}")
            return None
        
        return max(input_files, key=lambda x: x.stat().st_mtime)

    @staticmethod
    def get_output_file(quiz_name: str) -> Path:
        """Generate output file path and ensure output directory exists."""
        output_dir = Path('outputdata')
        output_dir.mkdir(exist_ok=True)
        return output_dir / f"{quiz_name}.xlsx"