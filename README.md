# Progress Report Summarizer

A Python tool that analyzes progress report markdown files and generates concise summaries using Ollama and Llama2. The tool identifies key sections of progress reports, extracts relevant information, and produces formatted summaries with preserved hyperlinks.

## Features

- Analyzes markdown files for progress report content
- Extracts and summarizes three key aspects:
  - Time spent
  - Money utilization
  - Future plans
- Preserves and includes relevant hyperlinks from the original text
- Generates GitHub-flavored markdown summaries
- Saves summaries to timestamped markdown files
- Tracks processed files to avoid duplicate processing
- Posts summaries as GitHub comments (optional)

## Requirements

- Python 3.x
- Ollama (with Llama2 model)
- Required Python packages:
  - ollama
  - argparse
  - requests (for GitHub integration)

## Installation

1. Ensure you have Ollama installed and the Llama2 model downloaded:
   ```bash
   ollama pull llama2
   ```

2. Clone this repository:
   ```bash
   git clone <repository-url>
   cd opensats-progress-report-bot
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Generating Summaries

Run the script by providing the path to a markdown file:

```bash
python progress_summarizer.py path/to/your/report.md
```

The script will:
1. Process the input markdown file
2. Generate a formatted summary
3. Save the summary to a new file (e.g., `summary_20240315_143022.md`)
4. Display the summary in the console
5. Track the processed file in `processed_files.json`

### Posting to GitHub

To post a summary as a GitHub comment:

```bash
python github_commenter.py --token YOUR_GITHUB_TOKEN \
                          https://github.com/owner/repo/issues/123 \
                          path/to/summary.md
```

Replace:
- `YOUR_GITHUB_TOKEN` with your GitHub personal access token
- `https://github.com/owner/repo/issues/123` with the full URL of the GitHub issue
- `path/to/summary.md` with the path to your generated summary file

### Combined Processing and Posting

For a complete workflow that both summarizes and posts to GitHub, use the combined bot:

```bash
python progress_report_bot.py --token YOUR_GITHUB_TOKEN \
                             path/to/your/report.md \
                             https://github.com/owner/repo/issues/123
```

The bot will:
1. Process the progress report and generate a summary
2. Check if this report has already been posted to the specified issue
3. Post the summary as a comment if it hasn't been posted before
4. Track posted reports in `github_posts.json` to avoid duplicates

The GitHub token is optional. If not provided, the bot will still generate the summary but won't post it to GitHub.

## Output

The generated summary file includes:
- A title header
- Source file information
- Generation timestamp
- Formatted summary with:
  - Headers for each section
  - Bullet points for key points
  - Preserved hyperlinks from the original text

## Example

Input markdown file:
```markdown
# Q1 2024 Progress Report

## Time Spent
- Worked on [Project A](https://github.com/example/project-a)
- Contributed to [Documentation](https://docs.example.com)

## Money Utilization
- Purchased licenses for [Tool X](https://toolx.com)
- Funded [Conference Attendance](https://conference.example.com)

## Next Quarter Plans
- Continue work on [Project A](https://github.com/example/project-a)
- Start new initiative [Project B](https://github.com/example/project-b)
```

Generated summary:
```markdown
# Progress Report Summary

*Generated from: path/to/your/report.md*
*Generated on: 2024-03-15 14:30:22*

## Time Spent
- Worked on [Project A](https://github.com/example/project-a)
- Contributed to documentation efforts

## Money Utilization
- Purchased licenses for [Tool X](https://toolx.com)
- Funded conference attendance

## Next Quarter Plans
- Continue development of [Project A](https://github.com/example/project-a)
- Begin work on [Project B](https://github.com/example/project-b)
```

## Notes

- The tool uses Ollama's Llama2 model for text analysis and summarization
- Processed files are tracked in `processed_files.json` to avoid duplicate processing
- Each summary is saved with a unique timestamp to prevent overwriting
- The tool preserves relevant hyperlinks from the original text in the summary
- For GitHub integration, you'll need a personal access token with `repo` scope 