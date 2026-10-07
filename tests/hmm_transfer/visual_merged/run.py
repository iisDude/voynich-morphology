from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))
sys.argv=[sys.argv[0],"--dataset","visual_merged"]
from hmm_transfer_v0 import main
main()
