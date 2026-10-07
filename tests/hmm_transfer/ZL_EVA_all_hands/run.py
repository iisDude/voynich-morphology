from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))
sys.argv=[sys.argv[0],"--dataset","ZL_EVA_all_hands"]
from hmm_transfer_all_hands_v1 import main
main()
