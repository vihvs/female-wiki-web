from datetime import timedelta, datetime

from django.core.management.base import BaseCommand

from wiki.models import Page, Tag

from bs4 import BeautifulSoup
import requests
import wikipedia
from textblob import TextBlob


wikipedia.set_rate_limiting(True, min_wait=timedelta(milliseconds=100))

project_list = ['WikiProject_Women', 'Women%27s_History', 'Women_writers', 'Women_scientists', 'Women_artists', 'Women%27s_sport']


def page_scrapper(url):
    """Receive the wikipedia project url and returns a dataframe with name, link, summary, photo link and
    tags from the summary's text."""
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    """The table has two classes, so the list need to be sum."""
    name_containers_even = html_soup.find_all('tr', class_ = 'list-even')
    name_containers_odd = html_soup.find_all('tr', class_ = 'list-odd')
    name_containers = name_containers_even + name_containers_odd

    """Grab name and link from the page's table."""
    pages = []

    for item in name_containers:
        name = item.a.text
        link = item.a['href']

        try:
            page = wikipedia.WikipediaPage(name)
        except wikipedia.exceptions.PageError:
            continue


        """Grab the tags of the wikipedia's article from the summary."""
        tags = TextBlob(page.summary).tags
        tags = [row for row in tags if row[1] in ['NNP', 'NN']]

        page = {
            'name': name,
            'link': link,
            'summary': page.summary,
            'tags':tags
        }

        pages.append(page)

    return pages



class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting download...")
        for project_name in project_list:
            print(f"[{datetime.now().strftime('%A, %d. %B %Y %I:%M:%S%p')}] Downloading Pages for project: {project_name}")

            """Include the information about the project and page that will be used."""
            offset_number = 1
            limit_number = 3

            """Create the url that will be used in the function page_scrapper."""
            while True:
                base = 'https://tools.wmflabs.org/enwp10/cgi-bin/list2.fcgi?run=yes'
                project = f'&projecta={project_name}'
                limit = f'&limit={limit_number}'
                offset = f'&offset={offset_number}'

                url = base + project + limit + offset
                print(f"[{datetime.now().strftime('%A, %d. %B %Y %I:%M:%S%p')}] Downloading url: {url}")

                pages = page_scrapper(url)
                for page in pages:
                    tags = page.pop("tags")
                    new_page = Page.objects.create(**page)
                    print(f"[{datetime.now().strftime('%A, %d. %B %Y %I:%M:%S%p')}] Page: {new_page}")

                    new_tags = []
                    for tag, _ in tags:
                        tag, created = Tag.objects.get_or_create(text=tag)
                        new_tags.append(tag)

                    new_page.tags.add(*new_tags)

                offset_number += limit_number
                if len(pages) == 0:
                    break
