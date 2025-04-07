"""Module for tracking score changes."""
from dataclasses import dataclass


@dataclass
class ScoreChange:
    """Class to hold score change information."""
    team_name: str
    question_number: int
    old_score: float
    new_score: float
    
    @property
    def difference(self) -> float:
        """Calculate score difference."""
        return self.new_score - self.old_score