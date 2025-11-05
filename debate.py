from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage, ModelFamily
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
import asyncio
import httpx
import os

load_dotenv()
base_url=os.getenv("BASE_URL")
API_KEY=os.getenv("API_KEY")

async def team_config(topic):
    custom_http_client = httpx.AsyncClient(verify=False)
    model = OpenAIChatCompletionClient(
        model="meta/llama-3.3-70b-instruct",
        base_url=base_url,
        api_key=API_KEY,
        http_client=custom_http_client,
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": ModelFamily.LLAMA_3_3_70B,
            "structured_output": True,
        },
    )

    # One Host agent and Two debate agents John(for) and Alice(against)
    host_agen = AssistantAgent(
        name="Jane",
        model_client=model,
        model_client_stream=True,
        system_message=(
            'You are Jane, the host of a bebate between John(for), a support agent'
            'and Alice(against), a critic agent. You will be moderate the debate.'
            f'The debate topic is {topic}.'
            'At the beginning of each round, announce the round number.'
            'At the beginning of third round, declare that it will be'
            'the last round. After the last round, thank the audience and exactly'
            'say "TERMINATE" to end the debate.'
        )
    )
    for_agent = AssistantAgent(
        name="John",
        model_client=model,
        model_client_stream=True,
        system_message=f"You are an profissional debater. You will argue for the given topic {topic} in supports of the motion. You will be debating Alice.",
    )
    against_agent = AssistantAgent(
        name="Alice",
        model_client=model,
        model_client_stream=True,
        system_message=f"You are an profissional debater. You will argue against the given topic {topic} in opposes of the motion. You will be debating John.",
    )

    team = RoundRobinGroupChat(
        [host_agen, for_agent, against_agent],
        max_turns=20,
        termination_condition=TextMentionTermination("TERMINATE")
    )

    return team

async def debate(team):
    async for stream in team.run_stream(task="Start the debate!"):
            if isinstance(stream, TaskResult):
                msg = f"Stopping Reason: {stream.stop_reason}"
                yield msg
            elif hasattr(stream, 'type') and stream.type == 'ModelClientStreamingChunkEvent':  # Only yield chunks
                msg = f"{stream.source}: {stream.content}"
                yield msg
    
async def main():
    topic = "Shall US goverment ban TikTok?"
    team = await team_config(topic)
    async for msg in debate(team):
        print('-'*20)
        print(msg)

if __name__ == "__main__":
    asyncio.run(main())