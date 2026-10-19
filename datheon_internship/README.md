# Structured LLM Prompt Pipeline & JSON Extractor

## Overview
A Python application that uses the Google Gemini API to extract structured invoice information from unstructured text and validate the results using Pydantic.

## Features
- Extracts invoice number, vendor, total, and currency.
- Uses a reusable prompt template with few-shot examples.
- Requests structured JSON output from Gemini.
- Validates extracted data using Pydantic and custom validation rules.
- Handles missing fields, empty files, and invalid data.
- Saves validated results to a JSON file.
- Includes automated tests using pytest.

## Technologies
- Python 3
- Google Gemini API (`google-genai`)
- Pydantic
- python-dotenv
- pytest

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory:

   ```text
   GEMINI_API_KEY=your_api_key_here
   ```

   Replace the placeholder with your own Gemini API key. Never commit your actual API key to GitHub.

4. Ensure `invoice.txt` contains the invoice text to process.

## Run the Application

```bash
python main.py
```

The extracted invoice data is saved to `invoice_output.json`.

## Run Tests

```bash
python -m pytest -v
```

## Output Example

```json
{
  "invoice_number": "INV-2026-789",
  "vendor": "AMMAN OFFICE SUPPLIES",
  "total": 162.4,
  "currency": "JOD"
}
```

## Project Status
Task 1 implementation includes Gemini integration, reusable prompt templates, few-shot examples, structured JSON output, Pydantic validation, and automated tests.
