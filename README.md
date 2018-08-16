# Influenza - Analysing Singapore's network of influencers'

This is a project to visualise a network between Singapore's instagram influencers. Each node in the network is an influencer, and the edges between them are defined by the pairwise Jaccard similarity of both influencers' followers.

## Setup

### Dependencies 
* Numpy 
* Pickle
* Selenium
* Multiprocessing
* Pandas
* NetworkX

### Seed influencer list in seed_list.txt

## Usage

### Scraping 

Use object Scraper and script RunScraper.py to crawl Instagram posts. Hardcode Instagram username and password for scraping. The current Multiprocessing function only uses one core but increase it along with more IG accounts to improve efficiency.

### Analysis 

Use Network Analysis.ipynb for network graph. Credits to Plotly(https://plot.ly/python/3d-network-graph/) for providing graphing code. 
