# Deletion Consequences — E-commerce Foreign-Key Rules

This submission implements the required deletion behavior for an e-commerce system with `customers`, `orders`, and `order_items`.

## Rules

- `orders.customer_id → customers.customer_id`: `ON DELETE RESTRICT`. Customer history is financial and must not be removed accidentally.
- `order_items.order_id → orders.order_id`: `ON DELETE CASCADE`. Line items are components of an order and have no meaning without it.

## Deliverables

- `schema.sql` — PostgreSQL-compatible schema with primary keys, foreign keys, deletion rules, checks, uniqueness, and indexes.
- `sample_data.sql` — representative customers, orders, and order items.
- `ERD/corrected_erd.png` and `ERD/corrected_erd.mmd` — corrected relationship diagram.
- `Changes.md` — business reasoning for RESTRICT and CASCADE.
- `scripts/verify_deletions.py` — reproducible deletion behavior tests.
- `docs/verification-output.txt` — captured verification results.
- `docs/submission-pages/` — five PNG submission pages showing the final schema and deletion evidence.

## Verify

```bash
python3 scripts/verify_deletions.py
```

Expected behavior: deleting customer 1 is rejected, deleting customer 2 succeeds, and deleting order 101 removes its two line items automatically.

## Pull-request verification

The five PNG pages in `docs/submission-pages/` are the upload-ready visual proof requested by Challenge 6. The archive is available at `docs/deletion-consequences-five-page-pngs.zip`.
