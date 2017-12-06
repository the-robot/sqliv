SQLiv
===

### Massive SQL injection scanner  
**Features**  
1. multiple domain scanning with SQL injection dork by Bing, Google, or Yahoo
2. targetted scanning by providing specific domain (with crawling)
3. reverse domain scanning

> both SQLi scanning and domain info checking are done in multiprocessing  
> so the script is super fast at scanning many urls

> quick tutorial & screenshots are shown at the bottom  
> project contribution tips at the bottom  

---

**Installation**  
1. git clone https://github.com/Hadesy2k/sqliv.git
2. sudo python2 setup.py -i

> Dependencies  
> - [bs4](https://pypi.python.org/pypi/bs4)  
> - [termcolor](https://pypi.python.org/pypi/termcolor)  
> - [google](https://pypi.python.org/pypi/google)
> - [nyawc](https://pypi.python.org/pypi/nyawc/)

**Pre-installed Systems**  
- [BlackArch Linux](https://blackarch.org/scanner.html) ![BlackArch](https://raw.githubusercontent.com/BlackArch/blackarch-artwork/master/logo/logo-38-49.png)

---
### Quick Tutorial  
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
```python
python sqliv.py -t <URL>  
python sqliv.py -t www.example.com  
python sqliv.py -t www.example.com/index.php?id=1  
```

**3. Reverse domain and scanning**  
- do reverse domain and look for websites that hosted on same server as target url
```python
python sqliv.py -t <URL> -r
```

**4. Dumping scanned result**
- you can dump the scanned results as json by giving this argument
```python
python sqliv.py -d <SQLI DORK> -e <SEARCH ENGINE> -o result.json
```

**View help**  
```python
python sqliv.py --help

usage: sqliv.py [-h] [-d D] [-e E] [-p P] [-t T] [-r]

optional arguments:
  -h, --help  show this help message and exit
  -d D        SQL injection dork
  -e E        search engine [Google only for now]
  -p P        number of websites to look for in search engine
  -t T        scan target website
  -r          reverse domain
```

---
### screenshots
![1](https://raw.githubusercontent.com/Hadesy2k/sqliv/master/screenshots/1.png)
![2](https://raw.githubusercontent.com/Hadesy2k/sqliv/master/screenshots/2.png)
![3](https://raw.githubusercontent.com/Hadesy2k/sqliv/master/screenshots/3.png)
![4](https://raw.githubusercontent.com/Hadesy2k/sqliv/master/screenshots/4.png)

---

### Development
**TODO**  
1. POST form SQLi vulnerability testing
