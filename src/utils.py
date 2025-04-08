import logging
import os
from pathlib import Path
import platform

def get_fastway_dir():
    if os.name == 'nt':
        # Windows
        base_dir = Path("C:/Fastway")
    else:
        # Linux / MacOS
        base_dir = Path.home() / ".fastway"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir

fastway_dir = get_fastway_dir()

log_path = fastway_dir / 'fastway.log'

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('fastway')
