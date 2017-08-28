import contextlib

import feedparser

from models import Subscription as SubscriptionDomain, db


class Subscription:
    def __init__(self, subscription_domain):
        self._subscription_domain = subscription_domain
        self.name = subscription_domain.name
        self.url = subscription_domain.url
        self.last_link = subscription_domain.last_link

    def __str__(self):
        return '{} subscription'.format(self.name)

    @staticmethod
    def _get_last_link(url):
        d = feedparser.parse(url)
        return d.entries[0].link

    @classmethod
    def subscribe(cls, name, url, subscriber):
        s = SubscriptionDomain(name, url, cls._get_last_link(url), subscriber)
        db.session.add(s)
        db.session.commit()
        return cls(s)

    def _updates(self):
        d = feedparser.parse(self.url)
        new_link_list = []
        for entry in d.entries:
            new_link = entry.get('link')
            if new_link and new_link != self.last_link:
                new_link_list.append(new_link)
            elif new_link == self.last_link:
                break
        return new_link_list

    @contextlib.contextmanager
    def updates(self):
        last_news = self._updates()
        last_link = None
        if last_news:
            last_link = last_news[0]
        yield last_news
        if last_link:
            self.last_link = last_link
            self._subscription_domain.last_link = last_link
            db.session.add(self._subscription_domain)
            db.session.commit()
