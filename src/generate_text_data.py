from __future__ import division, print_function
import pdb
import github3
import getpass
import re
import csv
import time

__author__ = "WeiFoo"
# pp = str(getpass.getpass())
pp = "WOxing1987!"
gh = github3.login(username="WeiFoo", password=pp)

def get_issues(gh, user, repo_name, include_code=True):
  def remove_code(line):
    line = re.sub(r'\[\]\r\n', ' ', line)
    lst = line.split("\r\n```")
    out = []
    for n, each in enumerate(lst):
      if not n % 2:
        out.append(each)
    # print(out)
    # pdb.set_trace()
    return " ".join(out)

  repo = gh.repository(user, repo_name)
  line = []
  count = 0
  for issue in repo.issues(state="all"):
    if count <= 4000:
      count += 1
    else:
      time.sleep(3600)
      count = 0
    this_labels = [i.name for i in issue.labels()]
    if this_labels:
      this_labels = [re.sub(r' ', '_', i) for i in this_labels]
      label = re.sub(r'[<>]', ' ', " ".join(this_labels).lower()).encode('ascii', 'ignore')
      if include_code:
        if not issue.body:
          body = re.sub(r"<(.*?)>|\n|(\\(.*?){)|}|[!$%^&*()_+|~\-={}\[\]:\";'<>?,.\/\\]|[]|[@]|\r|#|```", ' ',
                      issue.title.lower()).encode('ascii', 'ignore')
        else:
          body = re.sub(r"<(.*?)>|\n|(\\(.*?){)|}|[!$%^&*()_+|~\-={}\[\]:\";'<>?,.\/\\]|[]|[@]|\r|#|```", ' ',
                      issue.title.lower() + "\n" + remove_code(issue.body.lower())).encode('ascii', 'ignore')
      else:
        if not issue.body:
          body = re.sub(r"<(.*?)>|\n|(\\(.*?){)|}|[!$%^&*()_+|~\-={}\[\]:\";'<>?,.\/\\]|[]|[@]|\r|#|```", ' ',
                      issue.title.lower()).encode('ascii', 'ignore')
        else:
          body = re.sub(r"<(.*?)>|\n|(\\(.*?){)|}|[!$%^&*()_+|~\-={}\[\]:\";'<>?,.\/\\]|[]|[@]|\r|#|```", ' ',
                      issue.title.lower() + "\n" + issue.body_text.lower()).encode('ascii', 'ignore')
      line.append([word for word in re.sub(r'  ', ' ', body + '>>>' + label).split(' ') if len(word) > 1])

  with open('../data/' + repo_name + '2.txt', 'w') as fwrite:
    writer = csv.writer(fwrite, delimiter=' ')
    for l in line:
      try:
        writer.writerow(l)
      except:
        pdb.set_trace()
  print(gh.rate_limit())


if __name__ == "__main__":
  user_repo = {"ansible": "ansible", "elastic": "logstash",
               "graphite-project": "graphite-web", "atom": "atom","mbostock":"d3",
               "moment":"moment","TryGhost":"Ghost"}
  time.sleep(3600)
  # user_repo = { "scikit-learn": "scikit-learn"}
  for usr, repo in user_repo.iteritems():
    get_issues(gh, usr, repo)


