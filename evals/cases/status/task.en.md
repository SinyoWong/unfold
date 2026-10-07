# Status label (simulated business exercise)

Request: change the order-list label “Pending” to “待处理”. Change only this display label; keep the internal status `pending`.

The entry point in `app.py` is `display_status(status) -> str`; input is a string. Keep `Paid` for `paid`, `Cancelled` for `cancelled`, and return unknown states and the empty string unchanged. Keep the interface and add no dependencies.

Keep the command-line entry point: `python app.py pending` must print one line containing “待处理”; other statuses follow the same rules above. Arguments still use internal status strings; do not replace the internal `pending` value with Chinese.
