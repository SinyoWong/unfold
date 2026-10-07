def can_read(document, actor):
    if actor.get("role") == "admin":
        return True
    return (
        actor.get("role") == "member"
        and bool(actor.get("department"))
        and document["department"] == actor["department"]
    )


def list_documents(documents, actor, department=None):
    return [
        document
        for document in documents
        if can_read(document, actor)
        and (department is None or document["department"] == department)
    ]


def get_document(documents, actor, document_id):
    for document in documents:
        if document["id"] == document_id and can_read(document, actor):
            return document
    return None
