import codex


class Game:
    def __init__(self, ctx: codex.CodexContext):
        self.ctx = ctx

    async def play(self):
        raise NotImplementedError()
