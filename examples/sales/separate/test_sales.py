"""运行 python test_sales.py，检查汇总、CSV 和输入校验。"""

import copy
import csv
import io

from app import export_sales_csv, summarize_sales


def check_total(orders, amount_cents, refund_cents):
    original = copy.deepcopy(orders)
    expected = {"amount_cents": amount_cents, "refund_cents": refund_cents}
    total = summarize_sales(orders)
    assert type(total) is dict and total == expected, (orders, total, expected)
    assert all(type(value) is int for value in total.values()), total
    assert orders == original, "汇总修改了输入"
    rows = list(csv.reader(io.StringIO(export_sales_csv(orders), newline="")))
    assert rows == [
        ["amount_cents", "refund_cents"],
        [str(amount_cents), str(refund_cents)],
    ], rows
    assert orders == original, "导出修改了输入"


def check_rejected(orders):
    original = copy.deepcopy(orders)
    for entry in (summarize_sales, export_sales_csv):
        try:
            entry(orders)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{entry.__name__} 未拒绝非法订单：{orders!r}")
        assert orders == original, f"{entry.__name__} 修改了输入"


def run_checks():
    paid = {"status": "paid", "amount_cents": 10000, "refund_cents": 2000}
    second = {"status": "paid", "amount_cents": 5000, "refund_cents": 0}
    cancelled = {"status": "cancelled", "amount_cents": 9000, "refund_cents": 3000}
    check_total([], 0, 0)
    check_total([paid, second], 15000, 2000)
    check_total([paid, second, cancelled], 15000, 2000)
    check_total([paid, dict(second, refund_cents=1000)], 15000, 3000)
    check_total([cancelled], 0, 0)
    check_total([dict(cancelled, refund_cents=9000)], 0, 0)
    check_total([dict(cancelled, amount_cents=0, refund_cents=0)], 0, 0)
    check_total([dict(paid, refund_cents=10000)], 10000, 10000)
    check_total([dict(paid, amount_cents=0, refund_cents=0)], 0, 0)
    check_total([dict(paid, amount_cents=10**30, refund_cents=1)], 10**30, 1)

    invalid_orders = []
    for status in ("paid", "cancelled"):
        valid = dict(paid, status=status)
        for field in ("status", "amount_cents", "refund_cents"):
            missing = valid.copy()
            del missing[field]
            invalid_orders.append(missing)
        for field in ("amount_cents", "refund_cents"):
            for value in (True, False, 1.5, 100.0, "100", None, -1):
                invalid_orders.append(dict(valid, **{field: value}))
        invalid_orders.append(dict(valid, refund_cents=10001))
    for status in ("pending", "", None, True, 1, []):
        invalid_orders.append(dict(paid, status=status))
    for invalid in invalid_orders:
        check_rejected([invalid])
        check_rejected([paid, invalid])
        check_rejected([invalid, paid])
    print("通过：汇总与 CSV 金额、退款边界、非法输入拒绝和输入保持不变。")


if __name__ == "__main__":
    run_checks()
