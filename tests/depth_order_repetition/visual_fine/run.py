from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))
sys.argv=[sys.argv[0],"--dataset","visual_fine"]
from finish_depth_order_repetition_v1 import main
main()
