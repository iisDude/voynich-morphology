from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))
sys.argv=[sys.argv[0],"--dataset","Turkish"]
from context_assays_v0 import main
main()
