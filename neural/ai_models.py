#Load and operate saved ML models here
import os
import time

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("summarization", model="Falconsai/text_summarization")

def generate_text(input_text, model=pipe, max_length=600, min_length=80, print_time_taken=False):
  start = time.time()
  output = model(input_text, max_length=max_length, min_length=min_length)
  end = time.time()
  print(f"Total Time Elapsed: {end - start:.2f}s")
  return ("SUMMARY: \n" + output[0]['summary_text'])


