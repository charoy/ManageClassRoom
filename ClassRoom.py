from types import NoneType
from datetime import datetime
from yaml import load,dump,YAMLError
from github import Github

class ClassRoom(object):

    def __init__(self,oauth,repo_name):
        self.repo_name=repo_name
        self.g = Github(oauth)

    def get_github_classroom_repos(self):
        result = list()
        for org in self.g.get_user().get_orgs():
            for repo in org.get_repos():
                print repo.name
                if self.repo_name in repo.name:
                    result.append(repo.html_url)
        return result




stream = open("props.yml", 'r')
try:
    props=load(stream)
    c=ClassRoom(props['github']['oauth'],'designpattern')
    r=c.get_github_classroom_repos()
    print r
except YAMLError as exc:
    print(exc)


