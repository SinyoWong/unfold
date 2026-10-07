import csv
import io


def summarize_sales(orders):
    return sum(order["amount_cents"] for order in orders if order["status"] == "paid")


def export_sales_csv(orders):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["sales_cents"])
    writer.writerow([summarize_sales(orders)])
    return output.getvalue()
