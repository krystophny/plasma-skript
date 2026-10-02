import sys
from pathlib import Path

here = Path(__file__).parent
sys.path[:0] = [str(here), str(here / "chapters")]

# Section references resolve through the script outline; build it once, first.
import notebook  # noqa: E402

notebook.ensure_outline()
