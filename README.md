# FootyPy
> FootyPy is a small Python library to extract and analyse football data. It uses libraries such as [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/) and [Pandas](https://pandas.pydata.org) to retrieve data from the www.

<br>

## Documentation

``` python
from footypy.data import match_stats

match_data = match_stats(2021, 'laliga')
player_data = players_stats(2021, 'laliga')

```

## Usage

Please be mindful when using FootyPy as it could potentially take down a website if you make constant HTTP requests to the server. If you are interested in the ethics of it, please read the [DOs and DON'Ts of Web Scraping](https://www.zenrows.com/blog/dos-and-donts-of-web-scraping#do-rotate-ips).

<br>

## License & copyright

© Frank Jimenez

Licensed under the [MIT Licence](LICENSE).