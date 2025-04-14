# SubCNAME Hunter

`SubCNAME Hunter` is a Python tool that helps discover subdomains for a given domain, retrieve their CNAME records, check their availability, and save the results to files. It combines the use of `subfinder`, `dig`, and `httpx` to provide a full subdomain enumeration and CNAME checking solution.

### Created by [ghost4ft] 🐺

---

## Features
- Discover subdomains using `subfinder`.
- Retrieve CNAME records for each subdomain using `dig`.
- Check the availability of CNAME URLs using `httpx`.
- Progress bar to show the status of CNAME checks.
- Save results into two separate files: one for subdomains and another for CNAME results.
- Display results in tables, showing alive and not alive domains.

---

## Prerequisites

To use this application, you will need the following tools installed:
- **subfinder**: For discovering subdomains.
- **dig**: For fetching CNAME records.
- **httpx**: For checking if URLs are alive.

### Install Required Libraries
To install the necessary Python libraries, create a virtual environment and install the dependencies:

```bash
pip install -r requirements.txt
```
### Usage
python subcname_hunter.py example.com
