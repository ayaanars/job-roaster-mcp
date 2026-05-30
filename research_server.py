
from mcp.server.fastmcp import FastMCP
import feedparser
import requests
from urllib.parse import quote


mcp = FastMCP("Research MCP Server")


@mcp.tool()
def wikipedia_definition(job_title: str) -> str:
    """
    Get a short Wikipedia definition for a CS/tech career using Wikipedia's public API.
    No fallback definition is used.
    """
    try:
        headers = {
            "User-Agent": "job-roaster-mcp-demo/1.0"
        }

        search_url = "https://en.wikipedia.org/w/api.php"

        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": job_title,
            "format": "json"
        }

        search_response = requests.get(
            search_url,
            params=search_params,
            headers=headers,
            timeout=10
        )

        search_response.raise_for_status()
        search_data = search_response.json()

        search_results = search_data.get("query", {}).get("search", [])

        if not search_results:
            return f"No Wikipedia result found for: {job_title}"

        best_title = search_results[0]["title"]

        encoded_title = quote(best_title.replace(" ", "_"))
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"

        summary_response = requests.get(
            summary_url,
            headers=headers,
            timeout=10
        )

        summary_response.raise_for_status()
        summary_data = summary_response.json()

        extract = summary_data.get("extract", "")

        if not extract:
            return f"Wikipedia page found for '{best_title}', but no summary was available."

        return f"Wikipedia page matched: {best_title}\n\n{extract}"

    except Exception as e:
        return f"Wikipedia API failed for {job_title}. Reason: {e}"


@mcp.tool()
def hackernews_search(job_title: str) -> str:
    """
    Search HackerNews for posts related to a CS/tech career.
    """
    try:
        query = job_title.replace(" ", "%20")
        url = f"https://hn.algolia.com/api/v1/search?query={query}&tags=story"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        hits = data.get("hits", [])[:5]

        if not hits:
            return f"No HackerNews posts found for {job_title}."

        results = []

        for item in hits:
            title = item.get("title", "No title")
            points = item.get("points", 0)
            comments = item.get("num_comments", 0)

            results.append(
                f"- {title} | Points: {points} | Comments: {comments}"
            )

        return "\n".join(results)

    except Exception as e:
        return f"HackerNews tool failed: {e}"


@mcp.tool()
def google_news_search(job_title: str) -> str:
    """
    Search Google News RSS for job/career-related headlines.
    """
    try:
        query = job_title.replace(" ", "+")
        url = f"https://news.google.com/rss/search?q={query}+career+technology"

        feed = feedparser.parse(url)

        headlines = []

        for entry in feed.entries[:5]:
            headlines.append(f"- {entry.title}")

        if not headlines:
            return f"No Google News headlines found for {job_title}."

        return "\n".join(headlines)

    except Exception as e:
        return f"Google News tool failed: {e}"


if __name__ == "__main__":
    mcp.run()
