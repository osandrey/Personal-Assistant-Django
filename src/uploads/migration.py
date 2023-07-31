import os
import json
from quoteapp.models import Tag, Author, Quote
from pymongo import MongoClient


with open('authors.json', 'r') as f:
    authors = json.load(f)
    for author in authors:
        Author.objects.get_or_create(
            name=author['fullname'],
            born_date=author['born_date'],
            born_location=author['born_location'],
            description=author['description'])

with open('quotes.json', 'r') as f:
    quotes = json.load(f)
    for quote in quotes:
        Quote.objects.get_or_create(
            tags=quote['tags'],
            authors=quote['author'],
            quote=quote['quote'])
