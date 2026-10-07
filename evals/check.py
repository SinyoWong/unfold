"""Independent acceptance checks. Run: python evals/check.py --selftest."""

import argparse
import copy
import csv
import importlib
import io
from pathlib import Path
import random
import subprocess
import sys
import tempfile


sys.dont_write_bytecode = True  # Reading a review target must not create __pycache__.
CASES = Path(__file__).resolve().parent / "cases"
FIXTURES = (
    ("status", "starter", "AssertionError: display_status('pending')"),
    ("status", "reference", None),
    ("sales", "starter", "AssertionError: sales summary sample 1"),
    ("sales", "reference", None),
    ("sales", "review-bad", "AssertionError: sales CSV sample 1"),
    ("permissions", "starter", "AttributeError: module 'app' has no attribute 'get_document'"),
    ("permissions", "reference", None),
    ("permissions", "review-bad", "AssertionError: detail actor="),
)


def equal(actual, expected, note):
    if actual != expected:
        raise AssertionError(f"{note}: expected {expected!r}, got {actual!r}")


def load_app(workspace):
    workspace = workspace.resolve()
    if not (workspace / "app.py").is_file():
        raise FileNotFoundError(workspace / "app.py")
    # Each --case runs in a fresh process, including every selftest sample.
    sys.path.insert(0, str(workspace))
    return importlib.import_module("app")


def check_status(app):
    for status, label in (
        ("pending", "待处理"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
        ("unknown", "unknown"),
        ("pending-review", "pending-review"),
        ("PENDING", "PENDING"),
        ("", ""),
    ):
        equal(app.display_status(status), label, f"display_status({status!r})")
        result = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", app.__file__, status],
            capture_output=True, text=True, encoding="utf-8", timeout=10,
        )
        equal(result.returncode, 0, f"status CLI exit code for {status!r}")
        equal(result.stdout, label + "\n", f"status CLI output for {status!r}")
        equal(result.stderr, "", f"status CLI stderr for {status!r}")


def sales_inputs():
    yield []
    yield [
        {"status": "paid", "amount_cents": 10000, "refund_cents": 2000},
        {"status": "paid", "amount_cents": 5000, "refund_cents": 0},
        {"status": "cancelled", "amount_cents": 90000, "refund_cents": 1000},
    ]
    yield [{"status": "paid", "amount_cents": 73, "refund_cents": 73}]
    yield [{"status": "paid", "amount_cents": 0, "refund_cents": 0}]
    yield [{"status": "cancelled", "amount_cents": 55, "refund_cents": 0}]
    yield [{"status": "paid", "amount_cents": 10**18 + 3, "refund_cents": 2}]
    rng = random.Random(20261007)
    for size in range(1, 31):
        orders = []
        for _ in range(size):
            amount = rng.randrange(0, 100000)
            orders.append({
                "status": rng.choice(("paid", "cancelled")),
                "amount_cents": amount,
                "refund_cents": rng.randrange(amount + 1),
            })
        yield orders


def check_sales(app, handoff=False):
    for index, orders in enumerate(sales_inputs()):
        original = copy.deepcopy(orders)
        paid = [order for order in orders if order["status"] == "paid"]
        amount = sum(order["amount_cents"] for order in paid)
        refund = sum(order["refund_cents"] for order in paid)
        if handoff:
            expected = {"amount_cents": amount, "refund_cents": refund}
            rows = [["amount_cents", "refund_cents"], [str(amount), str(refund)]]
        else:
            expected = amount - refund
            rows = [["sales_cents"], [str(expected)]]
        actual = app.summarize_sales(orders)
        equal(actual, expected, f"sales summary sample {index}")
        if handoff:
            equal(type(actual), dict, "handoff summary type")
            for value in actual.values():
                equal(type(value), int, "handoff cents type")
        else:
            equal(type(actual), int, "summary cents type")
        equal(orders, original, "summary must not mutate orders")
        exported = app.export_sales_csv(orders)
        equal(type(exported), str, "CSV return type")
        equal(list(csv.reader(io.StringIO(exported))), rows, f"sales CSV sample {index}")
        equal(orders, original, "CSV must not mutate orders")

    base = {"status": "paid", "amount_cents": 100, "refund_cents": 10}
    invalid = [
        {**base, "refund_cents": -1},
        {**base, "refund_cents": 101},
        {**base, "amount_cents": -1},
        {**base, "amount_cents": 100.0},
        {**base, "amount_cents": "100"},
        {**base, "amount_cents": True},
        {**base, "refund_cents": 10.0},
        {**base, "refund_cents": "10"},
        {**base, "refund_cents": False},
        {**base, "status": "pending"},
        {**base, "status": None},
        {**base, "status": "cancelled", "refund_cents": 101},
        {key: value for key, value in base.items() if key != "status"},
        {key: value for key, value in base.items() if key != "amount_cents"},
        {key: value for key, value in base.items() if key != "refund_cents"},
    ]
    for bad in invalid:
        for function in (app.summarize_sales, app.export_sales_csv):
            orders = [base.copy(), bad.copy()]
            original = copy.deepcopy(orders)
            try:
                function(orders)
            except ValueError:
                pass
            else:
                raise AssertionError(f"{function.__name__} accepted invalid order {bad!r}")
            equal(orders, original, "rejected input must not be mutated")


def check_permissions(app):
    documents = [
        {"id": "s-1", "department": "sales", "title": "销售 1"},
        {"id": "h-1", "department": "support", "title": "支持 1"},
        {"id": "s-2", "department": "sales", "title": "销售 2"},
        {"id": "o-1", "department": "ops", "title": "运营 1"},
    ]
    actors = [
        ({"role": "admin"}, {"s-1", "h-1", "s-2", "o-1"}),
        ({"role": "admin", "department": "sales"}, {"s-1", "h-1", "s-2", "o-1"}),
        ({"role": "member", "department": "sales"}, {"s-1", "s-2"}),
        ({"role": "member", "department": "support"}, {"h-1"}),
        ({"role": "member", "department": "ops"}, {"o-1"}),
        ({"role": "member", "department": "missing"}, set()),
        ({"role": "member", "department": None}, set()),
        ({"role": "member", "department": ""}, set()),
        ({"role": "member"}, set()),
        ({"role": "guest", "department": "sales"}, set()),
        ({"role": "ADMIN", "department": "sales"}, set()),
        ({"department": "sales"}, set()),
        ({}, set()),
    ]
    for collection in (documents, list(reversed(documents)), []):
        for actor, visible in actors:
            original = copy.deepcopy((collection, actor))
            for department in (None, "sales", "support", "ops", "missing", ""):
                expected = [
                    document for document in collection
                    if document["id"] in visible
                    and (department is None or document["department"] == department)
                ]
                equal(
                    app.list_documents(collection, actor, department), expected,
                    f"list actor={actor!r}, filter={department!r}",
                )
                equal((collection, actor), original, "list must not mutate inputs")
            equal(
                app.list_documents(collection, actor),
                [document for document in collection if document["id"] in visible],
                "list default department filter",
            )
            for document_id in ("s-1", "s-2", "h-1", "o-1", "absent", ""):
                expected = next(
                    (document for document in collection
                     if document["id"] == document_id and document_id in visible),
                    None,
                )
                equal(
                    app.get_document(collection, actor, document_id), expected,
                    f"detail actor={actor!r}, id={document_id!r}",
                )
                equal((collection, actor), original, "detail must not mutate inputs")


def check(case, workspace):
    app = load_app(workspace)
    if case == "status":
        check_status(app)
    elif case == "permissions":
        check_permissions(app)
    else:
        check_sales(app, handoff=case == "sales-handoff")


def require_fixtures(cases):
    for case, variant, _ in FIXTURES:
        path = cases / case / variant / "app.py"
        if not path.is_file():
            raise FileNotFoundError(f"required fixture is missing: {path}")


def run_case(case, workspace):
    return subprocess.run(
        [sys.executable, "-B", "-X", "utf8", str(Path(__file__).resolve()),
         "--case", case, "--workspace", str(workspace.resolve())],
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )


def check_runner_regressions():
    with tempfile.TemporaryDirectory(prefix="unfold-check-") as temporary:
        root = Path(temporary).resolve()
        try:
            require_fixtures(root)
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("missing fixtures were accepted")
        print("PASS runner: missing fixtures are rejected")

        for marker in ("first", "second"):
            workspace = root / marker
            workspace.mkdir()
            (workspace / "helper.py").write_text(
                f"MARKER = {marker!r}\n"
                "LABELS = {'pending': '\u5f85\u5904\u7406', 'paid': 'Paid', 'cancelled': 'Cancelled'}\n",
                encoding="utf-8",
            )
            (workspace / "app.py").write_text(
                "from helper import MARKER, LABELS\n"
                f"assert MARKER == {marker!r}\n"
                "def display_status(status):\n    return LABELS.get(status, status)\n"
                "if __name__ == '__main__':\n    import sys\n    print(display_status(sys.argv[1]))\n",
                encoding="utf-8",
            )
            result = run_case("status", workspace)
            equal(result.returncode, 0, f"sibling import ({marker}): {result.stderr.strip()}")
        print("PASS runner: sibling imports work without cross-workspace module caching")


def selftest():
    require_fixtures(CASES)
    for case, variant, expected_failure in FIXTURES:
        result = run_case(case, CASES / case / variant)
        output = (result.stdout + result.stderr).strip()
        if expected_failure is None:
            equal(result.returncode, 0, f"{case}/{variant}: {output}")
            print(f"PASS {case}/{variant}: all acceptance checks passed")
        else:
            equal(result.returncode, 1, f"{case}/{variant}: expected failure exit code; {output}")
            if expected_failure not in output:
                raise AssertionError(f"{case}/{variant}: unexpected failure: {output}")
            print(f"PASS {case}/{variant}: expected failure detected: {output}")
    check_runner_regressions()
    print(f"PASS selftest: {len(FIXTURES)} fixture outcomes verified")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--case", choices=("status", "sales", "permissions", "sales-handoff"))
    parser.add_argument("--workspace", type=Path, help="Directory containing the candidate app.py")
    args = parser.parse_args()
    if args.selftest:
        if args.case or args.workspace:
            parser.error("--selftest cannot be combined with --case or --workspace")
    elif not args.case or not args.workspace:
        parser.error("provide --selftest, or both --case and --workspace")
    try:
        if args.selftest:
            selftest()
        else:
            check(args.case, args.workspace)
            print(f"PASS {args.case}: all acceptance checks passed")
    except Exception as error:
        print(f"FAIL {args.case or 'selftest'}: {type(error).__name__}: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
