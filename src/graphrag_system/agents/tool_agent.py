class ToolAgent:
    def __init__(self, tools: dict | None = None) -> None:
        self.tools = tools or {}

    def call(self, tool_name: str, **kwargs):
        tool = self.tools.get(tool_name)
        if not tool:
            raise ValueError(f"Unknown tool: {tool_name}")
        return tool.run(**kwargs)
