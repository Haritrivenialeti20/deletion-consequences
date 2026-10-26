from pathlib import Path
import sqlite3

root = Path(__file__).resolve().parents[1]
schema = (root / 'schema.sql').read_text()
sample = (root / 'sample_data.sql').read_text()

def fresh():
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.executescript(schema)
    conn.executescript(sample)
    return conn

conn = fresh()
try:
    conn.execute('DELETE FROM customers WHERE customer_id = 1')
except sqlite3.IntegrityError as exc:
    restrict_error = str(exc)
else:
    raise AssertionError('customer with orders was deleted; RESTRICT is missing')
assert conn.execute('SELECT COUNT(*) FROM customers WHERE customer_id = 1').fetchone()[0] == 1
print('customer 1 delete: rejected by RESTRICT')

conn.execute('DELETE FROM customers WHERE customer_id = 2')
assert conn.execute('SELECT COUNT(*) FROM customers WHERE customer_id = 2').fetchone()[0] == 0
print('customer 2 delete: accepted because it has no orders')

conn = fresh()
conn.execute('DELETE FROM orders WHERE order_id = 101')
assert conn.execute('SELECT COUNT(*) FROM orders WHERE order_id = 101').fetchone()[0] == 0
assert conn.execute('SELECT COUNT(*) FROM order_items WHERE order_id = 101').fetchone()[0] == 0
assert conn.execute('SELECT COUNT(*) FROM order_items WHERE order_id = 102').fetchone()[0] == 1
print('order 101 delete: accepted; its 2 items removed by CASCADE')
print('verification passed: customer history is protected and order composition is cleaned up')
(root / 'docs/verification-output.txt').write_text(
    'customer 1 delete: rejected by RESTRICT\n'
    'customer 2 delete: accepted because it has no orders\n'
    'order 101 delete: accepted; its 2 items removed by CASCADE\n'
)
