import git
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timedelta

class AuthorInfo:
    def __init__(self):
        self.name = ''
        self.email = ''
        self.count = 0    

def clone_repo(repo_url, local_dir):
    # Clone the repository
    try:
        repo = git.Repo.clone_from(repo_url, local_dir)
    except Exception as e:
        print(f"Error cloning repository: {e}")
        return
    
def get_authors(repo, start_date):
    authors = defaultdict(AuthorInfo)
    for c in repo.iter_commits():
        tm = datetime.utcfromtimestamp(c.committed_date)
        if tm > start_date:
            a = authors[c.author.email]
            a.name = c.author.name
            a.email = c.author.email
            a.count += 1
    return authors

def collect(path_or_url, start_date_str):
    result = []
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    with tempfile.TemporaryDirectory() as tmpdir:
        if path_or_url.startswith('http'):
            repo = git.Repo.clone_from(path_or_url, tmpdir)
        else:
            repo = git.Repo(path_or_url)
        authors = get_authors(repo, start_date)
        sorted_authors = sorted(authors.values(), key=lambda x: x.count, reverse=True)
        for a in sorted_authors:
            result.append({'name':a.name, 'email':a.email, 'count':a.count})

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <repository_path|repo_url> [startDate]")
        print("Date format : YYYY-MM-DD (2022-03-01)")
        sys.exit(1)

    path_or_url = sys.argv[1]
    start_date_str = '1900-01-01'
    if len(sys.argv) > 2:
        start_date_str = sys.argv[2]

    result = collect(path_or_url, start_date_str)
    for a in result:
        print(f'{a["name"]} : {a["email"]} : {a["count"]}')
