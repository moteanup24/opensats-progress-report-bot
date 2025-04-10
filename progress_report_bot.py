import argparse
import os
from pathlib import Path
import json
from datetime import datetime
from progress_summarizer import ProgressSummarizer
from github_commenter import GitHubCommenter

class ProgressReportBot:
    def __init__(self, token=None):
        self.summarizer = ProgressSummarizer()
        self.github = GitHubCommenter(token) if token else None
        self.tracking_file = "github_posts.json"
        self.posted_issues = self._load_posted_issues()
    
    def _load_posted_issues(self):
        """Load the list of previously posted issues."""
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_posted_issues(self):
        """Save the list of posted issues."""
        with open(self.tracking_file, 'w') as f:
            json.dump(self.posted_issues, f, indent=2)
    
    def _get_report_id(self, report_path):
        """Generate a unique ID for the report based on its content."""
        with open(report_path, 'r') as f:
            content = f.read()
        # Use a combination of file path and first few lines as ID
        return f"{report_path}:{content[:100]}"
    
    def process_and_post(self, report_path, issue_url):
        """Process a progress report and post it to GitHub if not already posted."""
        # Generate summary
        summary, summary_file = self.summarizer.process_file(report_path)
        if not summary:
            print("No summary generated. The file might not be a progress report or has already been processed.")
            return False
        
        # Check if we've already posted this report to this issue
        report_id = self._get_report_id(report_path)
        if issue_url in self.posted_issues and report_id in self.posted_issues[issue_url]:
            print(f"This report has already been posted to {issue_url}")
            return False
        
        if not self.github:
            print("GitHub token not provided. Summary generated but not posted.")
            return True
        
        # Post to GitHub
        success = self.github.post_comment(issue_url, summary_file)
        
        if success:
            # Update tracking
            if issue_url not in self.posted_issues:
                self.posted_issues[issue_url] = []
            self.posted_issues[issue_url].append(report_id)
            self._save_posted_issues()
        
        return success

def main():
    parser = argparse.ArgumentParser(description='Process a progress report and post it to GitHub.')
    parser.add_argument('--token', help='GitHub access token (optional)')
    parser.add_argument('report_path', help='Path to the progress report markdown file')
    parser.add_argument('issue_url', help='GitHub issue URL to post the summary to')
    
    args = parser.parse_args()
    
    # Validate the report file exists
    if not os.path.exists(args.report_path):
        print(f"Error: Report file {args.report_path} does not exist.")
        return
    
    # Initialize and run the bot
    bot = ProgressReportBot(args.token)
    bot.process_and_post(args.report_path, args.issue_url)

if __name__ == "__main__":
    main() 