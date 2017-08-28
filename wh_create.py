from requests import get

from aggregator import token


def set_webhook(token):
    url = 'https://api.telegram.org/bot{token}/{method}'.format(token=token, method='setWebhook')
    params = {'url': 'https://aggregator-bizy.herokuapp.com/{}/'.format(token)}
    res = get(url=url, params=params)
    return res.status_code


if __name__ == '__main__':
    status = set_webhook(token)
