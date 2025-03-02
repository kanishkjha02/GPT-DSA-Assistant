import requests
from bs4 import BeautifulSoup
import re

def clean_html(html_text):
    """
    Removes HTML tags and returns clean text.
    """
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text().strip()

def extract_examples(description):
    """
    Extracts example test cases from the problem description.
    - Ensures correct separation of multiple examples.
    - Stops capturing `expected_output` at `Example X:` or `Constraints:`.
    """
    examples = []
    
    # Updated regex to properly separate multiple examples and stop at the next `Example X:`
    example_pattern = re.findall(
        r'Example (\d+):\s*Input:\s*(.*?)\s*Output:\s*(.*?)(?=\nExample \d+:|\nConstraints:|\Z)',
        description,
        re.DOTALL
    )

    for example_num, input_data, expected_output in example_pattern:
        examples.append({
            f"Example {example_num}": {
                "input": input_data.strip(),
                "expected_output": expected_output.strip()
            }
        })

    return examples if examples else [{"error": "No valid example found"}]

def fetch_leetcode_problem(leetcode_slug):
    """
    Fetches problem details from LeetCode's GraphQL API.
    - `leetcode_slug`: The problem’s slug (e.g., "two-sum").
    """
    url = "https://leetcode.com/graphql"

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://leetcode.com",
        "Referer": f"https://leetcode.com/problems/{leetcode_slug}/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        title
        content
        topicTags {
          name
        }
      }
    }
    """

    payload = {
        "operationName": "getQuestionDetail",
        "variables": {"titleSlug": leetcode_slug},
        "query": query
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()

        if "data" in data and "question" in data["data"]:
            question_data = data["data"]["question"]

            # **Extract problem details**
            problem_title = question_data["title"]
            problem_description = clean_html(question_data["content"])
            dsa_topics = [tag["name"] for tag in question_data["topicTags"]]

            # **Extract correctly formatted examples**
            formatted_examples = extract_examples(problem_description)

            return {
                "problem_title": problem_title,
                "problem_description": problem_description,
                "dsa_topics": dsa_topics,
                "examples": formatted_examples
            }

        return {"error": "Failed to fetch problem data from LeetCode API."}

    except requests.exceptions.RequestException as e:
        return {"error": f"LeetCode API request failed: {str(e)}"}

def fetch_similar_problems():
    pass
