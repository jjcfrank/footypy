# FootyPy
> FootyPy is a small Python library to extract and analyse football data. It uses libraries such as [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/) and [Pandas](https://pandas.pydata.org) to retrieve data from the www.

<br>

## 1. Documentation

### Importing library:
``` python
import footypy.data as fdata
```

### Check leagues available:
```python
#Currently available: Spanish La Liga, English Premier League, French Ligue1, German Bundesliga, Italian Serie A

leagues_available = fdata.leagues_available()
```

### Extracting match data:
```python
match_data = fdata.match_stats(2021, 'laliga')
```

### Extracting match data:
```python
player_data = fdata.players_stats(2021, 'laliga')
```

## 2. Coming soon
* Analysis functions
* Checking what years available by league
* Automatic bulk download of all years all leagues

## 2. Usage

Please be mindful when using FootyPy as it could potentially take down a website if you make constant HTTP requests to the server. If you are interested in the ethics of it, please read the [DOs and DON'Ts of Web Scraping](https://www.zenrows.com/blog/dos-and-donts-of-web-scraping#do-rotate-ips).

<br>

## License & copyright

© Frank Jimenez

Licensed under the [MIT Licence](LICENSE).