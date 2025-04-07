"""Input validation utilities."""
from typing import Callable, Tuple, Optional, Any


def get_validated_input(prompt: str, validator: Callable[[str], Tuple[bool, Any]], 
                       error_message: str) -> Any:
    """Get and validate user input.
    
    Args:
        prompt: Input prompt to display
        validator: Function that validates input and returns (is_valid, value)
        error_message: Message to display on invalid input
    
    Returns:
        Validated input value
    """
    while True:
        try:
            user_input = input(prompt).strip()
            is_valid, value = validator(user_input)
            if is_valid:
                return value
            print(error_message)
        except Exception:
            print(error_message)


def validate_positive_float(value: str) -> Tuple[bool, Optional[float]]:
    """Validate input is a positive float.
    
    Args:
        value: Input string to validate
    
    Returns:
        Tuple of (is_valid, converted_value)
    """
    try:
        float_val = float(value)
        return float_val > 0, float_val
    except ValueError:
        return False, None