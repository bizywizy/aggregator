from time import sleep

import feedparser

from models import Subscription, db


def subscribe(name, url):
    subscription = Subscription(name, url, get_last_link(url))
    db.session.add(subscription)
    db.session.commit()


def get_updates():
    subscriptions = Subscription.query.all()
    for subscription in subscriptions:
        new = get_new_link_list(subscription.url, subscription.last_link)
        subscription.last_link = new[0]
        db.session.add(subscription)
        db.session.commit()
        yield new


# feedparser
def get_last_link(url):
    d = feedparser.parse(url)
    return d.entries[0].link


def get_new_link_list(url, last_link):
    d = feedparser.parse(url)
    link_list = []
    for entry in d.entries:
        if entry.link == last_link:
            break
        link_list.append(entry.link)
    return link_list


if __name__ == '__main__':
    while True:
        for news in get_updates():
            print(news)
            sleep(10)
