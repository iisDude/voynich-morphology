from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))
sys.argv=[sys.argv[0],"--dataset","ZL_EVA"]
from run_structural_tests_v2 import main
main()
