import argparse
import os
from pathlib import Path
import requests
from datetime import datetime
import re

class GitHubCommenter:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def _read_summary(self, summary_file):
        """Read the contents of the summary file."""
        with open(summary_file, 'r') as f:
            return f.read()
    
    def _parse_github_url(self, url):
        """Extract owner, repo, and issue number from a GitHub issue URL."""
        # Pattern for GitHub issue URLs
        pattern = r'https://github.com/([^/]+)/([^/]+)/issues/(\d+)'
        match = re.match(pattern, url)
        
        if not match:
            raise ValueError("Invalid GitHub issue URL. Expected format: https://github.com/owner/repo/issues/number")
        
        return match.groups()
    
    def post_comment(self, issue_url, summary_file):
        """Post the summary as a comment to a GitHub issue."""
        # Extract repository details from URL
        try:
            owner, repo, issue_number = self._parse_github_url(issue_url)
        except ValueError as e:
            print(f"Error: {str(e)}")
            return False
        
        # Read the summary content
        summary_content = self._read_summary(summary_file)
        
        # Prepare the API URL
        url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments'
        
        # Prepare the comment body
        comment_body = {
            'body': summary_content
        }
        
        # Make the API request
        response = requests.post(url, headers=self.headers, json=comment_body)
        
        if response.status_code == 201:
            print(f"Successfully posted comment to {owner}/{repo} issue #{issue_number}")
            return True
        else:
            print(f"Failed to post comment. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Post a progress report summary as a GitHub comment.')
    parser.add_argument('--token', required=True, help='GitHub access token')
    parser.add_argument('issue_url', help='GitHub issue URL (e.g., https://github.com/owner/repo/issues/123)')
    parser.add_argument('summary_file', help='Path to the summary markdown file')
    
    args = parser.parse_args()
    
    # Validate the summary file exists
    if not os.path.exists(args.summary_file):
        print(f"Error: Summary file {args.summary_file} does not exist.")
        return
    
    # Initialize the commenter and post the comment
    commenter = GitHubCommenter(args.token)
    commenter.post_comment(args.issue_url, args.summary_file)

if __name__ == "__main__":
    main() 