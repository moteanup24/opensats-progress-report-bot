# Progress Report Summarizer

This bot uses Ollama and the Llama2 model to automatically summarize progress reports from markdown files. It specifically looks for reports that contain responses to three key questions:
- How did you spend your time?
- How did you make use of the money?
- What do you plan to work on next quarter?

## Prerequisites

1. Install Ollama and pull the Llama2 model:
```bash
curl https://ollama.ai/install.sh | sh
ollama pull llama2
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your markdown files containing progress reports in the same directory as the script.
2. Run the script:
```bash
python progress_summarizer.py
```

The script will:
- Process all `.md` files in the current directory
- Identify which files contain progress reports
- Generate summaries for new progress reports
- Skip files that have been processed before
- Save summaries in a `processed_files.json` file

## Progress Report Format

Your progress reports should be in markdown format and should contain responses to all three key questions mentioned above. The bot will only process files that contain all three questions.

## Output

For each progress report, the bot will output:
1. A confirmation that the file is being processed
2. A summary of the responses to the three key questions
3. A record of the processed file in `processed_files.json`

Files that are not progress reports or have been processed before will be skipped. 