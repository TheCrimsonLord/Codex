from discord.ext import commands


class RoleHierarchyError(commands.CommandError):
    pass


class PermissionFailed(commands.CommandError):
    pass
