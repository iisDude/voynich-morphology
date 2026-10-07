from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))
from positional_dependence_and_boundaries_v0 import main
main()
