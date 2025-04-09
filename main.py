"""Main entry point for the quiz processing application."""
import streamlit.web as stw
from pathlib import Path


def main():
    """Main entry point for the application."""
    web_app = Path(__file__).parent / "web" / "streamlit_app.py"
    stw.bootstrap.run(web_app, "", [], [])


if __name__ == '__main__':
    main()