import sys
from pathlib import Path

here = Path(__file__).parent
sys.path[:0] = [str(here), str(here / "chapters")]
