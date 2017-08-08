SQLiv
===

### Massive SQL injection scanner
**Features**
1. multiple domain scanning with SQL injection dork
2. targetted scanning by providing specific domain (with crawling)
4. reverse domain scanning

**1. Multiple domain scanning with SQLi dork**
> python sqliv.py -d <SQLI DORK> -e <SEARCH ENGINE>
> python sqliv.py -d "inurl:index.php?id=" -e google

It simple search multiple websites from given dork and scan the results one by one

**2. Targetted scanning**
> python sqliv.py -t <URL>
