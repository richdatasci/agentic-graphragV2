class DataAccessPolicy:
    def filter_documents(self, documents: list[dict], user_roles: list[str]) -> list[dict]:
        allowed = []
        for document in documents:
            roles = document.get("allowed_roles", ["admin"])
            if set(roles) & set(user_roles):
                allowed.append(document)
        return allowed
