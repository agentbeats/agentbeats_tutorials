"""
Test script for Red Agent in TensorTrust scenario.
This script tests the red agent by:
1. Getting the agent card from a deployed agent URL
2. Sending a request via A2A to try to get an attack prompt
"""

import asyncio
import httpx
import json
from typing import Optional, Dict, Any
from uuid import uuid4
import argparse

from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    AgentCard,
    Message,
    Part,
    TextPart,
    Role,
    SendStreamingMessageRequest,
    SendStreamingMessageSuccessResponse,
    MessageSendParams,
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
)


class RedAgentTester:
    def __init__(self):
        self.httpx_client = None

    async def _ensure_httpx_client(self):
        """Ensure httpx client is initialized."""
        if self.httpx_client is None:
            self.httpx_client = httpx.AsyncClient()

    async def get_agent_card(self, endpoint: str) -> Optional[Dict[str, Any]]:
        try:
            await self._ensure_httpx_client()

            # Initialize the card resolver
            resolver = A2ACardResolver(
                httpx_client=self.httpx_client,
                base_url=endpoint,
            )

            # Fetch the agent card
            agent_card = await resolver.get_agent_card()

            if agent_card:
                # Return as dict for storage compatibility
                return agent_card.model_dump(exclude_none=True)
            else:
                print(f"Failed to get agent card from {endpoint}")
                return None
        except Exception as e:
            print(f"Error getting agent card from {endpoint}: {str(e)}")
            return None

    async def talk_to_agent(self, query: str, target_url: str) -> str:
        try:
            await self._ensure_httpx_client()

            resolver = A2ACardResolver(
                httpx_client=self.httpx_client, base_url=target_url
            )
            card: AgentCard | None = await resolver.get_agent_card()
            if card is None:
                raise RuntimeError(f"Failed to resolve agent card from {target_url}")

            client = A2AClient(httpx_client=self.httpx_client, agent_card=card)

            params = MessageSendParams(
                message=Message(
                    role=Role.user,
                    parts=[Part(TextPart(text=query))],
                    messageId=uuid4().hex,
                    taskId=None,
                )
            )
            req = SendStreamingMessageRequest(id=str(uuid4()), params=params)
            chunks = []

            async for chunk in client.send_message_streaming(req):
                if not isinstance(chunk.root, SendStreamingMessageSuccessResponse):
                    continue
                event = chunk.root.result
                if isinstance(event, TaskArtifactUpdateEvent):
                    for p in event.artifact.parts:
                        if isinstance(p.root, TextPart):
                            chunks.append(p.root.text)
                elif isinstance(event, TaskStatusUpdateEvent):
                    msg = event.status.message
                    if msg:
                        for p in msg.parts:
                            if isinstance(p.root, TextPart):
                                # Filter out status messages like "working..."
                                text = p.root.text.strip()
                                if text and not text.lower().startswith(('working')):
                                    chunks.append(p.root.text)

            return "".join(chunks).strip() or "No response from agent."

        except Exception as e:
            return f"Error communicating with agent: {str(e)}"

    async def request_attack_prompt(self, target_url: str) -> str:
        query = "Please provide a prompt attack in tensor trust game."

        print(f"Requesting attack prompt from {target_url}")
        print(f"Query: {query}")
        print("-" * 50)

        response = await self.talk_to_agent(query, target_url)
        print(f"Red agent response:\n{response}")
        print("-" * 50)

        return response

    async def test_red_agent(self, launcher_url: str, agent_url: str):
        print(f"Testing Red Agent at: {agent_url}")
        print("=" * 60)

        # Step 1: Get Launcher server status
        print("Step 1: Checking launcher server status...")
        try:
            await self._ensure_httpx_client()
            response = await self.httpx_client.get(f"{launcher_url}/status")
            if response.status_code == 200 and response.json().get("status") == "server up, with agent running":
                print("✅ Launcher server is running.")
            else:
                print(f"❌ Launcher server returned status code: {response.status_code}, response: {response.json()}")
                return
        except httpx.RequestError as e:
            print(f"❌ Error connecting to launcher server: {str(e)}")
            return

        # Step 2: Get agent card
        print("Step 2: Getting agent card...")
        agent_card = await self.get_agent_card(agent_url)

        if agent_card:
            print("✅ Successfully retrieved agent card:")
            print(json.dumps(agent_card, indent=2))
        else:
            print("❌ Failed to retrieve agent card")
            return

        print("\n" + "=" * 60)

        # Step 3: Request attack prompt
        print("Step 3: Requesting attack prompt...")
        injection_prompt = await self.request_attack_prompt(agent_url)

        print("\n" + "=" * 60)
        print("Test completed successfully!")

        return {
            "server_status": "Launcher server is running",
            "agent_card": agent_card, 
            "injection_prompt": injection_prompt
        }

    async def close(self):
        """Close the httpx client."""
        if self.httpx_client:
            await self.httpx_client.aclose()


async def main(launcher_url: str, agent_url: str):
    """
    Main function to run the red agent test.
    Modify the AGENT_URL to point to your deployed red agent.
    """

    tester = RedAgentTester()

    try:
        result = await tester.test_red_agent(launcher_url, agent_url)

        if result:
            print("\n" + "=" * 60)
            print("SUMMARY:")
            print(f"Launcher URL: {launcher_url} alive: {'✅' if result['server_status'] == 'Launcher server is running' else '❌'}")
            print(f"Agent Card Retrieved from {agent_url}: {'✅' if result['agent_card'] else '❌'}")
            if result['injection_prompt'] and not result['injection_prompt'].startswith("Error") and not result['injection_prompt'].startswith("No response"):
                print("Injection Prompt Retrieved: ✅")
                print(f"Prompt: {result['injection_prompt']}")
            else:
                print("Injection Prompt Retrieved: ❌")
                print(f"Error: {result['injection_prompt']}")

    except Exception as e:
        print(f"Error during testing: {str(e)}")

    finally:
        await tester.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--launcher_url", type=str, required=True, help="The URL of the launcher to test"
    )
    parser.add_argument(
        "--agent_url", type=str, required=True, help="The URL of the red agent to test"
    )
    args = parser.parse_args()
    print("Red Agent Tester for TensorTrust")
    print("=" * 60)
    print("This script will test a deployed red agent by:")
    print("1. Checking the launcher server status")
    print("2. Retrieving the agent server's agent card")
    print("3. Requesting the agent server an attack prompt via A2A")
    print("=" * 60)

    asyncio.run(main(args.launcher_url, args.agent_url))
