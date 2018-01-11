import os
import re

from dateutil import parser
from github import Github
from github import GithubException
from yaml import load, YAMLError

API_REPO = 'https://api.github.com/user/repos'
PREFIX='software-architecture-2017'

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
        print(commits)
        if commits:
            for c in commits:
                if type(c.author) is not None and c.author.login not in self.teachers:
                        authors.add(c.author.login)
                        count=count+1
            return list([authors,count])

    def committers(self, commits):
        committers = set()
        thedates=list()
        count = 0
        try:
            for c in commits:
                print(c.raw_headers)
                print(c.last_modified)
                d = parser.parse(c.last_modified)
                print(d)
                thedates.append(d)
                count = count + 1
                if type(c.committer) is not None and c.committer.login not in self.teachers:
                    #print c.committer
                    committers.add(c.committer.login)
                    print(c.raw_headers)
                    print(c.last_modified)
                    d=parser.parse(c.last_modified)
                    print(d)
                    thedates.append(d)
                    count = count + 1
            return list([committers, count,thedates])
        except GithubException:
            return list([0,0,0])

    def checktags(self,repo,required_tags):
        found=set()
        count=0
        tags=repo.get_tags()
        for t in tags:
            if type(t) != NoneType and t.name  in required_tags:
                    found.add(t.name)
                    count+=1
        return list([found, count])

    def clone(self,repo,dir):
        stream = open("props.yml", 'r')
        try:
            props = load(stream)
            url = '%s?access_token=%s' % (API_REPO, props['github']['oauth'])
            print(repo.clone_url)
            line=re.sub('//','//8d511495b21e701c7f2e7238a79061844eb0aa4d@',repo.clone_url)
            os.system("git clone "+line)
        except YAMLError as exc:
            print(exc)


stream = open("props.yml", 'r')
try:
    props=load(stream)
    c=ClassRoom(props['github']['oauth'],PREFIX)
    c.setTeachers([u'oster', u'charoy'])
    repos=c.getRepos()
    commitfile=PREFIX+'.csv'
    f=open(commitfile,"w+")
    for r in repos:
        w=c.getCommits(r)
        u=c.committers(w)
        print(u[0])
        print(u[1])
        print(u[2])
        f.write(r.html_url+";"+str(u[1]))
        if u[2] != 0:
            for d in u[2]:
                f.write(";"+str(d))
        f.write("\n")
        print(r.git_url)
        clonedir=PREFIX+'repos/'
 #       c.clone(r,clonedir)
    f.close()

#        print(c.workDistribution(w))
#        print(c.committers(w))
#        t=c.checktags(r,set(['RELEASE_DAY_1','RELEASE_DAY_2']))
#        print(t)
        #c.clone(r,"repos/")

except YAMLError as exc:
    print(exc)


