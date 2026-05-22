ROLE_PERMISSIONS = {
    "admin": {"read", "write", "evaluate", "manage"},
    "analyst": {"read", "evaluate"},
    "viewer": {"read"},
}


class Rbac:
    def has_permission(self, role: str, permission: str) -> bool:
        return permission in ROLE_PERMISSIONS.get(role, set())
