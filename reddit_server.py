
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Reddit MCP Server")


@mcp.tool()
def reddit_posts(job_title: str) -> str:
    """
    Return Reddit-style post data for a CS/tech career.
    This is fallback/demo data because Reddit API/PRAW access may require approval.
    """
    return f"""
Reddit-style fallback posts used.
Reason: Reddit API/PRAW credentials are not available yet.

- Is becoming a {job_title} still worth it?
- Entry-level {job_title} roles asking for 5 years of experience is insane.
- I work as a {job_title} and half my job is explaining what I actually do.
"""


@mcp.tool()
def reddit_comments(job_title: str) -> str:
    """
    Return Reddit-style comments for a CS/tech career.
    This is fallback/demo data because Reddit API/PRAW access may require approval.
    """
    return f"""
Reddit-style fallback comments used.
Reason: Reddit API/PRAW credentials are not available yet.

- "People make {job_title} sound glamorous, but the day-to-day work can be repetitive."
- "The hardest part is not just doing the work, it is explaining the work clearly."
- "Beginners underestimate how much learning is needed before becoming confident."
- "The job can be rewarding, but the expectations are usually higher than people think."
"""


if __name__ == "__main__":
    mcp.run()
