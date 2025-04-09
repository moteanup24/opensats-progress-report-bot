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

## Requirements

- Python 3.x
- Ollama (with Llama2 model)
- Required Python packages:
  - ollama
  - argparse

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

## Usage

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