class RoleGuard:
    @staticmethod
    def has_role(user, allowed_roles: list):
        return user.role.value in allowed_roles