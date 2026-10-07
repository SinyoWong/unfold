import csv
import io


def summarize_sales(orders):
    totals = {"amount_cents": 0, "refund_cents": 0}
    for order in orders:
        status = order.get("status")
        amount_cents = order.get("amount_cents")
        refund_cents = order.get("refund_cents")
        if status not in ("paid", "cancelled"):
            raise ValueError("status 必须为 paid 或 cancelled")
        if type(amount_cents) is not int or type(refund_cents) is not int:
            raise ValueError("amount_cents 和 refund_cents 必须为整数分，不能为布尔值")
        if not 0 <= refund_cents <= amount_cents:
            raise ValueError("金额必须满足 0 <= refund_cents <= amount_cents")
        if status == "paid":
            totals["amount_cents"] += amount_cents
            totals["refund_cents"] += refund_cents
    return totals


def export_sales_csv(orders):
    totals = summarize_sales(orders)
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["amount_cents", "refund_cents"])
    writer.writerow([totals["amount_cents"], totals["refund_cents"]])
    return output.getvalue()
