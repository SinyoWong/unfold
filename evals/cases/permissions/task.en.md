# Add a department document detail endpoint (simulated business exercise)

Existing `list_documents` limits visible documents by department and role. Add `get_document` using the same permission rule, so the new entry point cannot bypass restrictions.

## Inputs and interfaces

- `list_documents(documents, actor, department=None) -> list` returns visible documents in input order. The optional department filter may only narrow access.
- Add `get_document(documents, actor, document_id) -> dict | None`: return the requested visible document; both missing and forbidden records return `None` to avoid revealing existence.
- `documents` is a well-formed list of dictionaries containing unique string `id`, nonempty string `department`, and string `title`. Databases and malformed stored records are outside this exercise.
- `actor` is a dictionary derived from server-verified identity, with `role` and optional `department`. **Never trust a client-supplied role or department as identity.** Login is outside this exercise; a real integration must obtain `actor` from verified identity.
- `admin` reads all departments; `member` reads only their own; unknown or missing roles are denied. A member with a missing, `None`, or empty department is denied.
- The department filter and document ID come from user input and are strings (the filter can also be `None`). Unknown and empty-string filters return an empty list and cannot expand access.
- Empty documents safely return `[]` or `None`. Do not mutate documents or identity dictionaries.

Use only the Python standard library; add no framework or dependency.
