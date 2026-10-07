import csv
import io


def net_sales_cents(order):
    status = order.get("status")
    amount = order.get("amount_cents")
    refund = order.get("refund_cents")
    if status not in ("paid", "cancelled"):
        raise ValueError("订单状态必须为 paid 或 cancelled")
    if type(amount) is not int or type(refund) is not int:
        raise ValueError("金额和退款必须是整数分")
    if not 0 <= refund <= amount:
        raise ValueError("退款必须介于 0 与订单金额之间")
    return amount - refund if status == "paid" else 0


def summarize_sales(orders):
    return sum(net_sales_cents(order) for order in orders)


def export_sales_csv(orders):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["sales_cents"])
    writer.writerow([summarize_sales(orders)])
    return output.getvalue()
