Procurement decision: purchase $order_units routers, paid in credits.
A supplier is eligible only when certified, able to supply all $order_units units, and able to deliver within $deadline_days days.
Landed cost = $order_units * unit price + one shipping fee - one fixed discount. There is no tax.
Among eligible suppliers choose the lowest landed cost. Ties: fewer delivery days, then alphabetically smallest name.
Quotes are independent offers; do not add offers together or split the order.
$quotes
Example JSON format only (illustrative values, not the answer):
$output_example
Calculate your actual values from the data. Return integer results, not arithmetic expressions.
Return JSON only with exactly these keys: "vendor" (winning name exactly as shown), "landed_cost" (integer credits), "eligible_vendors" (integer count), "delivery_days" (integer for the winner).
