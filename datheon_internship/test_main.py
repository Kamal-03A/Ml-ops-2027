import pytest
from main import Invoice, validate_invoice
from main import extract_invoice

def test_valid_invoice():
    invoice = Invoice(
        invoice_number="INV-101",
        vendor="Tech Store",
        total=250.50,
        currency="JOD"
    )

    validate_invoice(invoice)


def test_zero_total_is_rejected():
    invoice = Invoice(
        invoice_number="INV-102",
        vendor="Tech Store",
        total=0,
        currency="JOD"
    )

    with pytest.raises(ValueError):
        validate_invoice(invoice)


def test_negative_total_is_rejected():
    invoice = Invoice(
        invoice_number="INV-103",
        vendor="Tech Store",
        total=-50,
        currency="JOD"
    )

    with pytest.raises(ValueError):
        validate_invoice(invoice)
def test_empty_invoice_file_is_rejected(tmp_path):
    empty_file = tmp_path / "empty_invoice.txt"
    empty_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        extract_invoice(str(empty_file))