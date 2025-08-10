import os
import sys
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Set your local model folder path here (make sure this folder contains the saved model files)
MODEL_DIR = r"/media/jeyanth-s/DevDrive/AI_Workspace/summarizer"  # NO trailing slash

# Make absolute path (optional but recommended)
MODEL_DIR = os.path.abspath(MODEL_DIR)

def main():
    try:
        # Load tokenizer and model from local folder only (offline mode)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR, local_files_only=True)

        # Initialize the summarization pipeline
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

        # Read JSON input from stdin
        input_json = sys.stdin.read()
        data = json.loads(input_json)

        # Extract the text to summarize
        text_to_summarize = data.get("text", "")
        if not text_to_summarize:
            print(json.dumps({"error": "No text provided"}))
            sys.exit(1)

        # Generate summary (adjust max_length/min_length as needed)
        summary = summarizer(text_to_summarize, max_length=60, min_length=25, do_sample=False)

        # Output the summary as JSON
        print(json.dumps({"summary": summary[0]['summary_text']}))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
