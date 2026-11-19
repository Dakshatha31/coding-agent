from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR=Path(__file__).resolve().parent
WORKSPACE=(BASE_DIR/"workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)
MODEL=os.getenv("MODEL","gpt-4o-mini")
MAX_STEPS=int(os.getenv("MAX_STEPS","8"))
MAX_FILE_BYTES=200_000
