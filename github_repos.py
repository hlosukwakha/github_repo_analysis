import requests

def get_top_github_repos(language="", num_repos=10):
    """
    Fetches the top GitHub repositories based on stars for a given language.

    Args:
        language (str): The programming language to filter by (e.g., "python", "javascript").
                        Leave empty to search all languages.
        num_repos (int): The number of top repositories to retrieve.

    Returns:
        list: A list of dictionaries, each representing a repository with 'rank',
              'repository_name', and 'stars'.
    """
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"stars:>10000{' language:' + language if language else ''}",
        "sort": "stars",
        "order": "desc",
        "per_page": num_repos
    }
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        repositories = []
        for i, item in enumerate(data.get("items", [])):
            repo_name = item["full_name"]
            stars = item["stargazers_count"]
            repositories.append({
                "rank": i + 1,
                "repository_name": repo_name,
                "stars": stars
            })
        return repositories

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")
        return []

def print_report(title, repositories):
    """
    Prints a formatted report of GitHub repositories.
    """
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)
    print("\n" + "-" * 40 + " Top Repositories " + "-" * 40 + "\n")
    print(f"{'Rank':<5} {'Repository':<60} {'Stars':>10}")
    print(f"{'-'*5:<5} {'-'*60:<60} {'-'*10:>10}")

    for repo in repositories:
        print(f"{repo['rank']:<5} {repo['repository_name']:<60} {repo['stars']:>10,}")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    print("Fetching top 10 GitHub repositories globally...")
    all_repos = get_top_github_repos(num_repos=10)
    if all_repos:
        print_report("GitHub Top Repositories (All Languages)", all_repos)
    else:
        print("Could not retrieve repositories.")

    print("\nFetching top 10 GitHub repositories for Python...")
    python_repos = get_top_github_repos(language="python", num_repos=10)
    if python_repos:
        print_report("GitHub Top Repositories by Language (Python)", python_repos)
    else:
        print("Could not retrieve Python repositories.")