import requests
from bs4 import BeautifulSoup
import re
import math
import joblib
import heapq
import numpy
import random

from requests.adapters import HTTPAdapter

scrape_memory = joblib.Memory(cachedir='scrape_cache', verbose=0)

@scrape_memory.cache
def scrape_amounts(id):
    session = requests.Session()
    session.mount('http://www.annualreports.com', HTTPAdapter(max_retries=5))

    url = 'http://www.annualreports.com/Company/%d' % id
    print 'scraping url', url

    r = session.get(url)
    soup = BeautifulSoup(r.text)

    for sp in soup.find_all('span'):
        if 'current' in sp.attrs['class']:
            name = sp.text
            break
    else:
        print 'could not find name'
        return

    report_url = None
    for a in soup.find_all('a'):
        href = a.attrs['href']
        if href.startswith('/Click/'):
            if a.text.find('Form 10K') != -1:
                report_url = href
                break
    else:
        print 'could not find report'
        return

    if report_url.find(':') != -1:
        return # URL is broken

    print 'scraping url', report_url

    url = 'http://www.annualreports.com' + report_url
    r = session.get(url)

    if r.headers['content-type'] != 'text/html':
        print 'not html'
        return

    soup = BeautifulSoup(r.text)
    text = soup.get_text()
    amounts = list(re.findall(r'\$\(?([0-9]+)', text))

    return name, amounts


def p_value(freq):
    n = sum(freq)
    ps = [(math.log(d+1) - math.log(d)) / math.log(10) for d in xrange(1, 10)]

    ks_obs = freq[1:]

    def ll(ks): # log-likelihood
        z = random.sample(zip(ks, ps), 8)
        return sum([k * math.log(p) for (k, p) in z])

    N = 10000
    P = 0
    for i in xrange(N):
        ks = numpy.random.multinomial(n, ps)
        if ll(ks) > ll(ks_obs): P += 1

    print 1.0 * P / N

def analyze(company_id):
    data = scrape_amounts(company_id)

    if data is None:
        return

    name, amounts = data

    freq = [0] * 10
    for amount in amounts:
        freq[int(amount[0])] += 1

    if sum(freq) < 100:
        return

    # Simple smoothing
    for d in xrange(1, 10):
        freq[d] += 100.0 * (math.log(d+1) - math.log(d)) / math.log(10)

    kl_div = 0.0
    for d in xrange(1, 10):
        Q = (math.log(d+1) - math.log(d)) / math.log(10)
        P = freq[d] / sum(freq[1:])
        kl_div += math.log(P / Q) * P

    return name, kl_div

if __name__ == '__main__':
    h = []
    for company_id in xrange(1, 10000):
        r = analyze(company_id)
        if r is not None:
            name, kl_div = r
            print name, kl_div
            h.append((kl_div, name))

    print 'worst offenders'
    for kl_div, name in sorted(h, reverse=True)[:10]:
        print '%12.9f %s' % (kl_div, name)

    print 'best'
    for kl_div, name in sorted(h)[:10]:
        print '%12.9f %s' % (kl_div, name)

    print
