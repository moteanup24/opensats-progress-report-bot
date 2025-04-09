import os
import json
from pathlib import Path
import ollama
from datetime import datetime
import argparse
import re

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
    
    def _extract_links(self, content):
        """Extract markdown links from the content."""
        # Pattern for markdown links: [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        return links

    def _generate_summary(self, content):
        """Generate a summary using Ollama and Llama2."""
        # Extract links from the original content
        links = self._extract_links(content)
        links_context = "\n".join([f"- [{text}]({url})" for text, url in links])
        
        prompt = f"""Please summarize the following progress report by extracting and organizing the responses to these specific questions:
        1. How did the person spend their time?
        2. How did they make use of the money?
        3. What do they plan to work on next quarter?

        Here's the report:
        {content}

        Available links from the original text:
        {links_context}

        Please provide a concise summary focusing only on these three aspects. Format the response in GitHub-flavored markdown with appropriate headers and bullet points. Include relevant links from the original text where appropriate to provide context and references. Use the exact link format [text](url) when including links."""
        
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
        
        # Create output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"summary_{timestamp}.md"
        
        # Save summary to file
        with open(output_file, 'w') as f:
            f.write(f"# Progress Report Summary\n\n")
            f.write(f"*Generated from: {file_path}*\n")
            f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(summary)
        
        # Mark file as processed
        self.processed_files[file_path] = {
            'processed_at': datetime.now().isoformat(),
            'summary': summary,
            'summary_file': output_file
        }
        self._save_processed_files()
        
        return summary, output_file

def main():
    parser = argparse.ArgumentParser(description='Process a progress report markdown file and generate a summary.')
    parser.add_argument('file_path', type=str, help='Path to the markdown file to process')
    args = parser.parse_args()
    
    summarizer = ProgressSummarizer()
    
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist.")
        return
    
    print(f"\nProcessing {file_path}...")
    summary, output_file = summarizer.process_file(file_path)
    
    if summary:
        print("\nSummary:")
        print(summary)
        print(f"\nSummary saved to: {output_file}")
        print("\n" + "="*50)

if __name__ == "__main__":
    main() 