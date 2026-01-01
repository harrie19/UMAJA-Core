import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import (
    ANSWER_TO_LIFE_THE_UNIVERSE_AND_EVERYTHING,
    answer_to_life_the_universe_and_everything,
)


def test_answer_constant_is_42():
    assert ANSWER_TO_LIFE_THE_UNIVERSE_AND_EVERYTHING == 42


def test_answer_function_returns_42():
    assert answer_to_life_the_universe_and_everything() == 42
