
import pytest
from pydantic import ValidationError

from main import Invoice, validate_invoice, build_invoice_prompt


def test_valid_invoice():
    invoice = Invoice(
        invoice_number="INV-101",
        vendor="Tech Store",
        total=250.50,
        currency="JOD",
    )
    validate_invoice(invoice)


def test_zero_total_is_rejected():
    invoice = Invoice(
        invoice_number="INV-102",
        vendor="Tech Store",
        total=0,
        currency="JOD",
    )
    with pytest.raises(ValueError, match="greater than zero"):
        validate_invoice(invoice)


def test_negative_total_is_rejected():
    invoice = Invoice(
        invoice_number="INV-103",
        vendor="Tech Store",
        total=-50,
        currency="JOD",
    )
    with pytest.raises(ValueError, match="greater than zero"):
        validate_invoice(invoice)


def test_missing_invoice_number_is_rejected():
    invoice = Invoice(
        vendor="Tech Store",
        total=100,
        currency="JOD",
    )
    with pytest.raises(ValueError, match="Invoice number is missing"):
        validate_invoice(invoice)


def test_missing_currency_is_rejected():
    invoice = Invoice(
        invoice_number="INV-104",
        vendor="Tech Store",
        total=100,
    )
    with pytest.raises(ValueError, match="Invoice currency is missing"):
        validate_invoice(invoice)


def test_prompt_contains_invoice_text():
    prompt = build_invoice_prompt("Invoice Number: INV-500")
    assert "INV-500" in prompt
    assert "Never invent or guess missing information" in prompt


def test_invalid_json_is_rejected():
    with pytest.raises(ValidationError):
        Invoice.model_validate_json("this is not JSON")
