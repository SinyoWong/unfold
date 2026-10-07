def list_documents(documents, actor, department=None):
    result = []
    for document in documents:
        if actor.get("role") == "admin":
            allowed = True
        elif actor.get("role") == "member" and actor.get("department"):
            allowed = document["department"] == actor["department"]
        else:
            allowed = False
        if allowed and (department is None or document["department"] == department):
            result.append(document)
    return result
