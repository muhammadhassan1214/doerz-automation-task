from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


def read_csv_data(file_name: str) -> Optional[List[Dict[str, str]]]:
    """
    Read rows from a CSV file located at the project root (next to user_data.csv).

    Args:
        file_name: Name of the CSV file, e.g. 'user_data.csv'.

    Returns:
        A list of dicts keyed by the CSV headers, or None if the file is missing.
    """
    # Resolve file path relative to this file: utils/ -> project root -> file
    file_path = (Path(__file__).resolve().parent.parent / file_name).resolve()

    data: List[Dict[str, str]] = []
    try:
        with file_path.open(mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        logger.error("CSV file not found: %s", file_path)
        return None
