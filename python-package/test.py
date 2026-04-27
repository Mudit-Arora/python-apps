from invoicing import generate_invoice

generate_invoice("../pdf-invoice-generator/invoices",
    "output", "product_id", "product_name",
    "amount_purchased", "price_per_unit", "total_price")