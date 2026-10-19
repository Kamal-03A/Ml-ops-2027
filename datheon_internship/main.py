
import os
import json

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, ValidationError, Field


# 1. Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# 2. Define the expected invoice structure
class Invoice(BaseModel):
    invoice_number: str | None = None
    vendor: str | None = None
    total: float | None = None
    currency: str | None = None


# 3. Validate extracted invoice data
def validate_invoice(invoice: Invoice) -> None:
    if not invoice.invoice_number:
        raise ValueError("Invoice number is missing.")

    if not invoice.vendor:
        raise ValueError("Vendor is missing.")

    if invoice.total is None:
        raise ValueError("Invoice total is missing.")

    if invoice.total <= 0:
        raise ValueError("Invoice total must be greater than zero.")

    if not invoice.currency:
        raise ValueError("Invoice currency is missing.")


# 4. Build a reusable prompt template with few-shot examples
def build_invoice_prompt(invoice_text: str) -> str:
    return f"""
You are an information extraction assistant.
Extract invoice data accurately from the supplied text.

Return these fields:
- invoice_number
- vendor
- total
- currency

Rules:
- Use only information explicitly supported by the invoice.
- Never invent or guess missing information.
- Return null for missing fields.
- Preserve the currency stated in the invoice.
- The total must be a number, without currency symbols.

Example 1:
Input:
Invoice Number: INV-100
Vendor: ABC Store
Total: 50.00 USD

Expected JSON:
{{
  "invoice_number": "INV-100",
  "vendor": "ABC Store",
  "total": 50.0,
  "currency": "USD"
}}

Example 2:
Input:
Invoice Number: INV-200
Vendor: XYZ Company
Total: 125.50 JOD

Expected JSON:
{{
  "invoice_number": "INV-200",
  "vendor": "XYZ Company",
  "total": 125.5,
  "currency": "JOD"
}}

Now extract the information from this invoice:

{invoice_text}
"""


# 5. Extract invoice information using Gemini
def extract_invoice(file_path: str) -> Invoice:
    # Read invoice text
    with open(file_path, "r", encoding="utf-8") as file:
        invoice_text = file.read()

    if not invoice_text.strip():
        raise ValueError("The invoice file is empty.")

    # Build the prompt
    prompt = build_invoice_prompt(invoice_text)

    # Request structured output from Gemini
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Invoice,
        },
    )

    if not response.text:
        raise ValueError("The AI returned an empty response.")

    # Parse and validate the JSON structure
    invoice = Invoice.model_validate_json(response.text)

    # Validate business rules
    validate_invoice(invoice)

    return invoice


# 6. Save the extracted invoice as JSON
def save_invoice(invoice: Invoice, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(invoice.model_dump_json(indent=2))


# 7. Run the program
def main() -> None:
    try:
        invoice = extract_invoice("invoice.txt")

        output_path = "invoice_output.json"
        save_invoice(invoice, output_path)

        print("Invoice extracted successfully!")
        print(invoice.model_dump_json(indent=2))
        print(f"\nSaved result to: {output_path}")

    except FileNotFoundError:
        print("Error: invoice.txt was not found.")

    except (ValidationError, ValueError) as error:
        print(f"Validation error: {error}")

    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()
