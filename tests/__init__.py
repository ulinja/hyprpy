from pathlib import Path
import logging, sys

PATH_TO_CACHE_DIR = Path(__file__).parent / ".cache"

logger = logging.getLogger('tests')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(levelname)s] %(asctime)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
