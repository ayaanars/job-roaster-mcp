
import asyncio
import os
import sys
from openai import OpenAI

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def call_tool(server_script: str, tool_name: str, arguments: dict) -> str:
    """
    Starts an MCP server through stdio, connects to it,
    calls one tool, then returns the result.
    """

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
    )

    # Colab fix:
    # MCP stdio can fail with "fileno" in notebook environments.
    # This sends MCP server logs to a real file instead.
    with open("mcp_error_log.txt", "a") as log_file:
        async with stdio_client(server_params, errlog=log_file) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(tool_name, arguments)

                output_parts = []

                for item in result.content:
                    if hasattr(item, "text"):
                        output_parts.append(item.text)
                    else:
                        output_parts.append(str(item))

                return "\n".join(output_parts)


async def collect_research(job_title: str) -> dict:
    """
    Calls tools from both MCP servers.
    """

    tool_calls = {
        "Wikipedia": call_tool(
            "research_server.py",
            "wikipedia_definition",
            {"job_title": job_title}
        ),
        "HackerNews": call_tool(
            "research_server.py",
            "hackernews_search",
            {"job_title": job_title}
        ),
        "Google News": call_tool(
            "research_server.py",
            "google_news_search",
            {"job_title": job_title}
        ),
        "Reddit Posts": call_tool(
            "reddit_server.py",
            "reddit_posts",
            {"job_title": job_title}
        ),
        "Reddit Comments": call_tool(
            "reddit_server.py",
            "reddit_comments",
            {"job_title": job_title}
        ),
    }

    results = {}

    for name, call in tool_calls.items():
        try:
            results[name] = await call
        except Exception as e:
            results[name] = f"{name} failed: {e}"

    return results


def research_agent(job_title: str, tool_outputs: dict) -> str:
    """
    Agent 1:
    Takes raw MCP tool outputs and asks GPT to create a structured research brief.
    """

    prompt = f"""
You are Agent 1: Research Agent.

The user entered this CS/technology career:
{job_title}

You received information from two MCP servers.

MCP Server 1: Research Server

Wikipedia:
{tool_outputs["Wikipedia"]}

HackerNews:
{tool_outputs["HackerNews"]}

Google News:
{tool_outputs["Google News"]}

MCP Server 2: Reddit Server

Reddit Posts:
{tool_outputs["Reddit Posts"]}

Reddit Comments:
{tool_outputs["Reddit Comments"]}

Create a structured research brief with this format:

# Research Brief: {job_title}

## 1. Official Definition
Explain what this career is.

## 2. Current Market / News Signals
Summarize the news and online discussion.

## 3. Community Opinions
Summarize what people online seem to say.

## 4. Common Struggles
List common struggles.

## 5. Overall Summary
Give a short useful summary.

Keep it clear, simple, and suitable for a university workshop demo.
"""

    response = openai_client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


def roast_agent(job_title: str, research_brief: str) -> str:
    """
    Agent 2:
    Takes Agent 1's research brief and asks GPT to create the final roast.
    """

    prompt = f"""
You are Agent 2: Roast Agent.

You received this research brief about the CS/technology career:
{job_title}

Research brief:
{research_brief}

Write a funny but harmless career roast.

Rules:
- Keep it under 150 words.
- Make it sarcastic and entertaining.
- Do not insult real people.
- Do not use offensive stereotypes.
- Make it suitable for a university workshop demo.
"""

    response = openai_client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


async def main():
    job_title = input("Enter a CS/tech career, e.g. software engineer, data scientist: ")

    print("\n==============================")
    print("CALLING BOTH MCP SERVERS")
    print("==============================\n")

    tool_outputs = await collect_research(job_title)

    for tool_name, output in tool_outputs.items():
        print(f"\n===== {tool_name} OUTPUT =====")
        print(output)

    print("\n==============================")
    print("RUNNING AGENT 1: RESEARCH AGENT")
    print("==============================\n")

    research_brief = research_agent(job_title, tool_outputs)

    print("\n===== COMPILED RESEARCH BRIEF =====\n")
    print(research_brief)

    print("\n==============================")
    print("RUNNING AGENT 2: ROAST AGENT")
    print("==============================\n")

    roast = roast_agent(job_title, research_brief)

    print("\n===== FINAL CAREER ROAST =====\n")
    print(roast)


if __name__ == "__main__":
    asyncio.run(main())
