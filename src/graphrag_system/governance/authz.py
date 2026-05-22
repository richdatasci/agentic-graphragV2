class Authorizer:
    def can_access(self, user_roles: list[str], allowed_roles: list[str]) -> bool:
        return bool(set(user_roles) & set(allowed_roles))
