# Notion Question-Answering with LangChain

🤖Ask questions to your Notion database in natural language🤖

💪 Built with [LangChain](https://github.com/hwchase17/langchain)

## Overview

Welcome to Notion Question-Answering, a project that leverages LangChain to allow users to ask questions to their Notion database in natural language. This project is not only equipped with a powerful question-answering script but also features a FastAPI app for a user-friendly interface. Additionally, an API endpoint has been implemented using FastAPI, providing a streaming response for efficient communication.

## Environment Setup

To set up your environment, follow these steps:

1. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key:

   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

## What's Inside?

### Example Data

The project includes example data from the Blendle Employee Handbook, serving as a demonstration of its capabilities. You can replace this with your own dataset following the instructions provided.

### API Endpoint

The FastAPI implementation provides an API endpoint for search questions with a streaming response. To run the API:

```bash
uvicorn index:app --reload
```

### Asking Questions

To ask a question:
Go to the localhost link and paste in your question

## Ingesting Your Own Dataset

1. Export your dataset from Notion in Markdown & CSV format.
2. Move the exported `.zip` file into the repository.
3. Unzip the file:

   ```bash
   unzip your_exported_file.zip -d Notion_DB
   ```

4. Ingest the data:

   ```bash
   python ingest.py
   ```

## Project Structure

- **chatmodel**: Contains scripts for the LangChain model, including data and ingestion.
- **index.py**: FastAPI implementation for the API endpoint.
- **routes**: Additional FastAPI routes (e.g., note.py).
- **static**: CSS styling for the app.
- **templates**: HTML templates for the StreamLit app.

Feel free to explore, contribute, and enhance the capabilities of this Notion Question-Answering project!
