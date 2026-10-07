from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))
from verify_candidate_partitions_v1 import main
main()
