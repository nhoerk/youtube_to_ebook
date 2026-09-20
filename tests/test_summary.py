# test_summary.py

from src.ai_processing.save_summary import process_chunk

file = process_chunk(
    "data/transcript_chunks/EyrdaHFpvOA_clean_part_1.txt"
)

print(file)