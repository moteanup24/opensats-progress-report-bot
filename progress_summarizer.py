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
        self.key_questions = [
            "how did you spend your time",
            "how did you make use of the money",
            "what do you plan to work on next quarter"
        ]
        
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
        content_lower = content.lower()
        # Check for both versions of each question (with and without question mark)
        for question in self.key_questions:
            if question not in content_lower and f"{question}?" not in content_lower:
                return False
        return True
    
    def _extract_links(self, content):
        """Extract markdown links and raw URLs from the content."""
        # Pattern for markdown links: [text](url)
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        # Pattern for raw URLs
        raw_urls = re.findall(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', content)
        
        # Combine and deduplicate links
        links = {}
        for text, url in markdown_links:
            links[url] = text
        for url in raw_urls:
            if url not in links:
                links[url] = url
        
        return links
    
    def _validate_summary(self, summary):
        """Validate that the summary includes all three key questions."""
        summary_lower = summary.lower()
        missing_questions = []
        
        for question in self.key_questions:
            # Check for variations of the question in the summary
            if (question not in summary_lower and 
                f"time spent" not in summary_lower and 
                f"money utilization" not in summary_lower and 
                f"next quarter" not in summary_lower):
                missing_questions.append(question)
        
        return len(missing_questions) == 0, missing_questions
    
    def _generate_summary(self, content):
        """Generate a summary using Ollama and Llama2."""
        # Extract links from the original content
        links = self._extract_links(content)
        links_context = "\n".join([f"- [{text}]({url})" for url, text in links.items()])
        
        prompt = f"""Please summarize the following progress report by extracting and organizing the responses to these specific questions:
        1. How did the person spend their time?
        2. How did they make use of the money?
        3. What do they plan to work on next quarter?

        Here's the report:
        {content}

        Available links from the original text:
        {links_context}

        Please provide a concise summary that MUST include all three sections:
        1. Time Spent
        2. Money Used
        3. Next Quarter Plans

        IMPORTANT: Follow this exact format and style:
        - Use bullet points with asterisks (*) for main items
        - Use plus signs (+) for sub-items
        - Use dashes (-) for sub-sub-items
        - Preserve ALL relevant links from the original text
        - Include links in their original context
        - Use the exact format [text](url) for links
        - Keep the same level of detail as the original
        - Maintain the hierarchical structure of the original report

        For each section, focus on summarizing the direct responses to the questions:

        For the Time Spent section:
        - Group related activities under clear headers
        - Include all relevant project names and collaborators
        - Preserve all technical details and progress
        - Include all relevant links to PRs, issues, and documentation
        - Focus on summarizing what was actually done, not just planned

        For the Money Used section:
        - Provide a general summary of fund usage (e.g., "living expenses and travel costs")
        - Keep this section concise and high-level
        - Only include specific details if they are particularly relevant
        - Focus on the main categories of expenses

        For the Next Quarter Plans section:
        - List primary focus areas first
        - Include specific goals and milestones
        - Preserve all relevant links to project plans and issues
        - Maintain the same level of detail as the original
        - Focus on summarizing concrete plans and next steps

        Format the response in GitHub-flavored markdown with appropriate headers and bullet points. 
        Ensure each section is clearly labeled and contains relevant information from the report, including all pertinent links."""
        
        max_attempts = 3
        for attempt in range(max_attempts):
            response = ollama.generate(
                model='llama2',
                prompt=prompt
            )
            
            summary = response['response']
            is_valid, missing_questions = self._validate_summary(summary)
            
            if is_valid:
                return summary
            
            if attempt < max_attempts - 1:
                print(f"Summary missing sections: {', '.join(missing_questions)}. Retrying...")
                prompt += f"\n\nPrevious attempt was missing these sections: {', '.join(missing_questions)}. Please ensure all sections are included."
            else:
                print("Warning: Generated summary is missing some sections after multiple attempts.")
                return summary
    
    def process_file(self, file_path):
        """Process a markdown file and generate a summary if it's a progress report."""
        file_path = str(file_path)
        
        # Check if file has been processed
        if file_path in self.processed_files:
            print(f"File {file_path} has already been processed.")
            return None, None
        
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if it's a progress report
        if not self._is_progress_report(content):
            print(f"File {file_path} is not a progress report.")
            return None, None
        
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
