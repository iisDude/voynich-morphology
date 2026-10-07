from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))
sys.argv=[sys.argv[0],"hmm","--dataset","visual_v11_merged"]
from run_tracked_tests_v1 import main
main()
