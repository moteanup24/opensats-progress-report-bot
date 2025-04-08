import os
import json
from pathlib import Path
import ollama
from datetime import datetime

class ProgressSummarizer:
    def __init__(self, processed_files_path="processed_files.json"):
        self.processed_files_path = processed_files_path
        self.processed_files = self._load_processed_files()
        
    def _load_processed_files(self):
        """Load the list of previously processed files."""
        if os.path.exists(self.processed_files_path):
            with open(self.processed_files_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_processed_files(self):
        """Save the list of processed files."""
        with open(self.processed_files_path, 'w') as f:
            json.dump(self.processed_files, f)
    
    def _is_progress_report(self, content):
        """Check if the content is a progress report by looking for key questions."""
        key_questions = [
            "how did you spend your time",
            "how did you make use of the money",
            "what do you plan to work on next quarter"
        ]
        
        content_lower = content.lower()
        # Check for both versions of each question (with and without question mark)
        for question in key_questions:
            if question not in content_lower and f"{question}?" not in content_lower:
                return False
        return True
    
    def _generate_summary(self, content):
        """Generate a summary using Ollama and Llama2."""
        prompt = f"""Please summarize the following progress report by extracting and organizing the responses to these specific questions:
        1. How did the person spend their time?
        2. How did they make use of the money?
        3. What do they plan to work on next quarter?

        Here's the report:
        {content}

        Please provide a concise summary focusing only on these three aspects."""
        
        response = ollama.generate(
            model='llama2',
            prompt=prompt
        )
        
        return response['response']
    
    def process_file(self, file_path):
        """Process a markdown file and generate a summary if it's a progress report."""
        file_path = str(file_path)
        
        # Check if file has been processed
        if file_path in self.processed_files:
            print(f"File {file_path} has already been processed.")
            return None
        
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if it's a progress report
        if not self._is_progress_report(content):
            print(f"File {file_path} is not a progress report.")
            return None
        
        # Generate summary
        summary = self._generate_summary(content)
        
        # Mark file as processed
        self.processed_files[file_path] = {
            'processed_at': datetime.now().isoformat(),
            'summary': summary
        }
        self._save_processed_files()
        
        return summary

def main():
    summarizer = ProgressSummarizer()
    
    # Get all markdown files in the current directory
    md_files = Path('.').glob('*.md')
    
    for file_path in md_files:
        print(f"\nProcessing {file_path}...")
        summary = summarizer.process_file(file_path)
        
        if summary:
            print("\nSummary:")
            print(summary)
            print("\n" + "="*50)

if __name__ == "__main__":
    main() 