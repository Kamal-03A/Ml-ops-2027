# Invoice Data Extraction with Gemini AI

A Python project that extracts structured information from invoice text using Google's Gemini AI and validates the output with Pydantic.

## Features

- Extract invoice number, vendor, total amount, and currency.
- Generate structured JSON output using Gemini.
- Validate extracted data using Pydantic.
- Reject empty invoice files and non-positive invoice totals.
- Run automated tests using pytest.

## Technologies

- Python
- Google Gemini API
- Google GenAI SDK
- Pydantic
- python-dotenv
- pytest

## Project Structure

```text
datheon_internship/
├── main.py
├── test_main.py
├── invoice.txt
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Setup

1. Clone the repository and navigate to the project folder.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Create a `.env` file and add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own API key. Never commit your `.env` file or expose your API key publicly.

## Run the Project

Make sure `invoice.txt` contains the invoice text, then run:

```bash
python main.py
```

The extracted invoice data will be printed in the terminal and saved to `invoice_output.json`.

## Run Tests

```bash
python -m pytest -v
```

## Validation

The project validates the invoice structure and checks that the total amount is greater than zero. It also rejects empty invoice files.

## Future Improvements

- Support PDF and image invoices.
- Add more validation rules.
- Improve error handling and logging.
- Support additional document types.