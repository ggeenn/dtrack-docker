import git
import sys
import shutil
import time
import os
from collections import defaultdict
from datetime import datetime, timedelta

class AuthorInfo:
    def __init__(self):
        self.name = ''
        self.email = ''
        self.count = 0    

def get_authors(repo, start_date):
    authors = defaultdict(AuthorInfo)
    for c in repo.iter_commits():
        tm = datetime.fromtimestamp(c.committed_date)
        if tm > start_date:
            a = authors[c.author.email]
            a.name = c.author.name
            a.email = c.author.email
            a.count += 1

    return authors

def collect_from_repo(repo, start_date):
    result = []
    authors = get_authors(repo, start_date)
    sorted_authors = sorted(authors.values(), key=lambda x: x.count, reverse=True)
    for a in sorted_authors:
        result.append({'name':a.name, 'email':a.email, 'count':a.count})
    return result

def remove_dir(d):
        try:
            time.sleep(1)
            shutil.rmtree(d)
            return True
        except FileNotFoundError:
            return True
        except PermissionError as e:
            print(f"Failed to delete {d}: {e}")
            return False

def collect_from_url(url, start_date):
    #tmpdir = tempfile.mkdtemp()
    try:
        tmpdir = os.path.join(os.getcwd(), 'tempgit')
        if remove_dir(tmpdir):
            with git.Repo.clone_from(url, tmpdir) as repo:
                return collect_from_repo(repo, start_date)
        return []
    finally:
        remove_dir(tmpdir)

def collect(path_or_url, start_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    if path_or_url.startswith('http'):
        return collect_from_url(path_or_url, start_date)

    with git.Repo(path_or_url) as repo:
        return collect_from_repo(repo, start_date)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f'Usage: python {sys.argv[0]} <repo_path|repo_url> [start_date]')
        print("Date format : YYYY-MM-DD (2022-03-01)")
        sys.exit(1)

    path_or_url = sys.argv[1]
    start_date_str = '1900-01-01'
    if len(sys.argv) > 2:
        start_date_str = sys.argv[2]

    result = collect(path_or_url, start_date_str)
    for a in result:
        print(f'{a["name"]} : {a["email"]} : {a["count"]}')
