
import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, ValidationError


# 1. Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# 2. Define the expected invoice structure
class Invoice(BaseModel):
    invoice_number: str
    vendor: str
    total: float
    currency: str = "USD"
def validate_invoice(invoice):
    if invoice.total <= 0:
        raise ValueError("Invoice total must be greater than zero.")

def extract_invoice(file_path):
    # 3. Read invoice text
    with open(file_path, "r", encoding="utf-8") as file:
        invoice_text = file.read()

    if not invoice_text.strip():
        raise ValueError("The invoice file is empty.")

    # 4. Ask Gemini to extract the information
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"""
Extract the invoice information from this text.

Return:
- invoice_number
- vendor
- total
- currency

Do not invent missing information.
Invoice text:
{invoice_text}
""",
        config={
            "response_mime_type": "application/json",
            "response_schema": Invoice,
        },
    )

    if not response.text:
        raise ValueError("The AI returned an empty response.")

    # 5. Validate the returned JSON
    invoice = Invoice.model_validate_json(response.text)

    validate_invoice(invoice)

def main():
    try:
        invoice = extract_invoice("invoice.txt")

        # 6. Save the result to a JSON file
        output_path = "invoice_output.json"

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(invoice.model_dump_json(indent=2))

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
