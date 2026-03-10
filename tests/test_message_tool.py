import pytest

from nanobot.agent.tools.message import MessageTool
from nanobot.bus.events import OutboundMessage


@pytest.mark.asyncio
async def test_message_tool_returns_error_when_no_target_context() -> None:
    tool = MessageTool()
    result = await tool.execute(content="test")
    assert result == "Error: No target channel/chat specified"


@pytest.mark.asyncio
async def test_message_tool_preserves_default_metadata() -> None:
    sent: list[OutboundMessage] = []

    async def _send(msg: OutboundMessage) -> None:
        sent.append(msg)

    tool = MessageTool(send_callback=_send)
    tool.set_context(
        channel="qq",
        chat_id="group123",
        message_id="msg1",
        metadata={"chat_type": "group"},
    )

    await tool.execute(content="hello")

    assert len(sent) == 1
    assert sent[0].metadata["message_id"] == "msg1"
    assert sent[0].metadata["chat_type"] == "group"
