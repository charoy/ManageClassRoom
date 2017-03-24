from types import NoneType
from datetime import datetime
from yaml import load,dump,YAMLError
from github import Github

class ClassRoom(object):

    def __init__(self,oauth,repo_name):
        self.repo_name=repo_name
        self.g = Github(oauth)

    def getRepos(self):
        result = list()
        for org in self.g.get_user().get_orgs():
            for repo in org.get_repos():
                if self.repo_name in repo.name:
                    result.append(repo)
        return result

    def getCommits(self,repo):
        commits = repo.get_commits()
        return commits

    def setTeachers(self,teachers):
        self.teachers=teachers

    def workDistribution(self,commits):
        authors=set()
        count=0
        for c in commits:
            if type(c.author) != NoneType and c.author.login not in self.teachers:
                    authors.add(c.author.login)
                    count=count+1
        return list([authors,count])

stream = open("props.yml", 'r')
try:
    props=load(stream)
    c=ClassRoom(props['github']['oauth'],'designpattern')
    c.setTeachers([u'oster', u'charoy'])
    repos=c.getRepos()
    for r in repos:
        w=c.getCommits(r)
        print(c.workDistribution(w))

except YAMLError as exc:
    print(exc)


