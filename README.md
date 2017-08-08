SQLiv
===

### Massive SQL injection scanner
**Features**
1. multiple domain scanning with SQL injection dork
2. targetted scanning by providing specific domain (with crawling)
4. reverse domain scanning

---

**1. Multiple domain scanning with SQLi dork**  
- it simply search multiple websites from given dork and scan the results one by one
```python
python sqliv.py -d <SQLI DORK> -e <SEARCH ENGINE>  
python sqliv.py -d "inurl:index.php?id=" -e google  
```

**2. Targetted scanning**  
- can provide only domain name or specifc url with query params
- if only domain name is provided, it will crawl and get urls with query
- then scan the urls one by one
> python sqliv.py -t <URL>  
> python sqliv.py -t www.example.com  
> python sqliv.py -t www.example.com/index.php?id=1  
