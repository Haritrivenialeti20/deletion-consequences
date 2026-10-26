# Deletion Consequences — Design Decisions

## `customers` → `orders`: `ON DELETE RESTRICT`

Orders are financial and customer-service records. Deleting a customer who has orders would remove or detach purchase history needed for accounting, refunds, audits, and support. `RESTRICT` makes the dangerous action fail before data is lost. The operational alternative is to archive or anonymize the customer after the order-retention policy allows it.

## `orders` → `order_items`: `ON DELETE CASCADE`

An order item has no independent meaning without its order. If an order is intentionally removed—for example, a test order or a cancelled transaction—its line items should disappear with it. `CASCADE` prevents orphaned items and makes the composition relationship easy to maintain.

## Verification

The valid sample contains two customers, two orders for Alice, and three order items. The verification harness demonstrates:

- deleting Alice is rejected because orders reference her;
- deleting Bob succeeds because he has no orders;
- deleting order 101 succeeds and automatically removes items 1001 and 1002 while leaving order 102 and item 1003 intact.

## General rule

Use `RESTRICT` when the child represents a record of business or legal value that must not disappear with a parent. Use `CASCADE` when the child is a component with no meaningful life outside its parent. Deletion rules should be chosen from the business meaning of the relationship, not merely developer convenience.
