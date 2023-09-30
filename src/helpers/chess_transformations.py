"""
This file contains dictionaries that are used to transform chess fields to indices and vice versa.
"""

FIELD_ID_TO_CHESS_INDEX = {f"{chr(97 + x)}{8 - y}": x + y * 8 for x in range(8) for y in range(8)}
CHESS_INDEX_TO_FIELD_ID = {v: k for k, v in FIELD_ID_TO_CHESS_INDEX.items()}