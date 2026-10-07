def display_status(status):
    labels = {"pending": "Pending", "paid": "Paid", "cancelled": "Cancelled"}
    return labels.get(status, status)


if __name__ == "__main__":
    import sys

    print(display_status(sys.argv[1]))
