# Job Roaster MCP Agent Demo

The user enters a computer science or technology career, such as:

- Software Engineer
- Data Scientist
- Cybersecurity Analyst
- Machine Learning Engineer
- Cloud Engineer
- DevOps Engineer

The system then gathers information using MCP tools, creates a structured research brief, and generates a short, harmless career roast.

## Project Idea

The app follows this flow:

1. User enters a CS/tech career title.
2. Agent 1, the Research Agent, collects information from multiple MCP tools.
3. Tool outputs are combined into one structured research brief.
4. Agent 2, the Roast Agent, reads the brief.
5. Agent 2 generates a funny but safe career roast.

## Architecture

The system uses two MCP servers.

### MCP Server 1: Research Server

This server contains general research tools:

- Wikipedia definition/search
- HackerNews search
- Google News RSS search

### MCP Server 2: Reddit Server

This server contains Reddit-related tools:

- Reddit posts
- Reddit comments

Currently, the Reddit server uses fallback demo data because Reddit API/PRAW access may require approval under Reddit's Responsible Builder Policy.

## Tech Stack

- Python
- MCP Python SDK
- OpenAI API
- Wikipedia public API
- HackerNews Algolia API
- Google News RSS
- Optional PRAW Reddit API integration

## Files

- `research_server.py`  
  Contains the Research MCP Server with Wikipedia, HackerNews, and Google News tools.

- `reddit_server.py`  
  Contains the Reddit MCP Server. Currently uses fallback Reddit-style data.

- `client.py`  
  Connects to both MCP servers, collects tool outputs, sends them to the Research Agent, and then sends the research brief to the Roast Agent.

- `requirements.txt`  
  Contains the Python dependencies.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
