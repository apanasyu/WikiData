import tweepy
import sys

def testAPI(api):
    try:
        api.home_timeline()
        return api
    except:
        print("Could not authenticate API exiting...")
        sys.exit(0)

def getAPI(apiUserType=True,proxyURL=None):
    """
    :mode: either "user" or "app"
    """
    #yelena_panasyuk
    '''
    consumer_key = 'yvj9Wfuk7IDY3VClHhQDqHBX8' # own key
    consumer_secret = 'AzmWpo8CWnBKTvWMBEdcKrcPlTWwkbmiGw2zpRzD6QeBFVtKyt' # own key
    access_token = '873335699277262848-IKq9J4SzG2xheeUnJzoIRZWYmIflxrs' # own key
    access_token_secret = 'yzjdqRrLMPffk1RxD17FEJdXCu8zhZQqj0oFWcd8k14HU' # own key
    '''
    #'''
    consumer_key = 'EU9ZJA5s6P6k0Mj2Hqtotijav' # own key
    consumer_secret = 'x1lXUVS6A7C0Ba5R6gEyjF8fGJqYdSQuKY4OPz8i6rzdmGyjiT' # own key
    access_token = '982410003461148673-U45W6KzuY57y7Gr8e096xYhLvsBOIIF' # own key
    access_token_secret = 'SRI8WnKxZTpiARolYAfxF6eq6GSuNDksKuF6aZbW6OtxP' # own key
    #'''
    
    '''
    consumer_key = 'o090U8x4YuYauxWSkuSqdY9FP' # own key
    consumer_secret = 'uHPnxL9q4rfJoV0k7IG1UYn2M49dxWGd2eJOMSVPvBQmJRrchP' # own key
    access_token = '873347330233290752-4jNPLcJ4u3srEJsyNRXSNeetvuBpc7V' # own key
    access_token_secret = 'MYD8wztrs9mUjHrdJAGsus9LtihJj2rcnxhhcxQOW5J6E' # own key
    '''
    
    if apiUserType:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    else:
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    
    testAPI(api)
    return api

def getAPI2(apiUserType=True,proxyURL=None):
    """
    :mode: either "user" or "app"
    """
    #yelena_panasyuk
    '''
    consumer_key = 'yvj9Wfuk7IDY3VClHhQDqHBX8' # own key
    consumer_secret = 'AzmWpo8CWnBKTvWMBEdcKrcPlTWwkbmiGw2zpRzD6QeBFVtKyt' # own key
    access_token = '873335699277262848-IKq9J4SzG2xheeUnJzoIRZWYmIflxrs' # own key
    access_token_secret = 'yzjdqRrLMPffk1RxD17FEJdXCu8zhZQqj0oFWcd8k14HU' # own key
    '''
    '''
    consumer_key = 'EU9ZJA5s6P6k0Mj2Hqtotijav' # own key
    consumer_secret = 'x1lXUVS6A7C0Ba5R6gEyjF8fGJqYdSQuKY4OPz8i6rzdmGyjiT' # own key
    access_token = '982410003461148673-U45W6KzuY57y7Gr8e096xYhLvsBOIIF' # own key
    access_token_secret = 'SRI8WnKxZTpiARolYAfxF6eq6GSuNDksKuF6aZbW6OtxP' # own key
    '''
    
    #'''
    consumer_key = 'o090U8x4YuYauxWSkuSqdY9FP' # own key
    consumer_secret = 'uHPnxL9q4rfJoV0k7IG1UYn2M49dxWGd2eJOMSVPvBQmJRrchP' # own key
    access_token = '873347330233290752-4jNPLcJ4u3srEJsyNRXSNeetvuBpc7V' # own key
    access_token_secret = 'MYD8wztrs9mUjHrdJAGsus9LtihJj2rcnxhhcxQOW5J6E' # own key
    #'''
    
    if apiUserType:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    else:
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    
    testAPI(api)
    return api

def getAPI3(apiUserType=True,proxyURL=None):
    """
    :mode: either "user" or "app"
    """
    #yelena_panasyuk
    #'''
    consumer_key = 'yvj9Wfuk7IDY3VClHhQDqHBX8' # own key
    consumer_secret = 'AzmWpo8CWnBKTvWMBEdcKrcPlTWwkbmiGw2zpRzD6QeBFVtKyt' # own key
    access_token = '873335699277262848-IKq9J4SzG2xheeUnJzoIRZWYmIflxrs' # own key
    access_token_secret = 'yzjdqRrLMPffk1RxD17FEJdXCu8zhZQqj0oFWcd8k14HU' # own key
    #'''
    '''
    consumer_key = 'EU9ZJA5s6P6k0Mj2Hqtotijav' # own key
    consumer_secret = 'x1lXUVS6A7C0Ba5R6gEyjF8fGJqYdSQuKY4OPz8i6rzdmGyjiT' # own key
    access_token = '982410003461148673-U45W6KzuY57y7Gr8e096xYhLvsBOIIF' # own key
    access_token_secret = 'SRI8WnKxZTpiARolYAfxF6eq6GSuNDksKuF6aZbW6OtxP' # own key
    '''
    
    '''
    consumer_key = 'o090U8x4YuYauxWSkuSqdY9FP' # own key
    consumer_secret = 'uHPnxL9q4rfJoV0k7IG1UYn2M49dxWGd2eJOMSVPvBQmJRrchP' # own key
    access_token = '873347330233290752-4jNPLcJ4u3srEJsyNRXSNeetvuBpc7V' # own key
    access_token_secret = 'MYD8wztrs9mUjHrdJAGsus9LtihJj2rcnxhhcxQOW5J6E' # own key
    '''
    
    if apiUserType:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    else:
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    
    testAPI(api)
    return api

def getAPI4(apiUserType=True,proxyURL=None):
    """
    :mode: either "user" or "app"
    """
    #'''
    consumer_key = 'oHkRQ01UUhEoJ8oVwIYyX49cI' # own key
    consumer_secret = 'liia12t0eipI6b2Le6UFnglqEbzYGV8AesadD28GlAgz0gk4KK' # own key
    access_token = '2751956811-7yBFKPBvKRyFWzP7DR9wbUyFegAsIHWqH8O4VUP' # own key
    access_token_secret = '2W2cUJykTyWWHseiX4h8uXzl2JmgTSV1HNYjkbYjgEEeB' # own key
    #'''
    
    if apiUserType:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    else:
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    
    testAPI(api)
    return api

def getAPI5(apiUserType=True,proxyURL=None):
    """
    :mode: either "user" or "app"
    """
    #'''
    consumer_key = 'NrL7Nr0UcgGeOqIMttskrA' # own key
    consumer_secret = '3JCpjEiSnDOBUy6uZQbGCVwJokUHMzK73TZKVSGyTcc' # own key
    access_token = '890904109-K99R5wrxleR9Z146O2E1ZHxEqobb7S2YTOeTmX3b' # own key
    access_token_secret = 'INXzIsCQleyrjYVJyJoyhvhJUQ9ar9sr8d0BsHtQqoCQZ' # own key
    #'''
    
    if apiUserType:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    else:
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    
    testAPI(api)
    return api

def getAPI6(apiUserType=True,proxyURL=None):
    """
    :mode: either "user" or "app"
    """
    #'''
    consumer_key = '8QCYM0Av0PBqCKg4873px7jg7' # own key
    consumer_secret = '724osY8vIX1mWz1a1R8NC7YnicWgvYycHPGgEYGmOPswUfdf5i' # own key
    access_token = '919748656143663104-QjNeTSKznCrxDybGZu4WPWQTer2WHEF' # own key
    access_token_secret = 'q56ddFi94w7CxxjLcZoSptpwRitW0K1DJYHibUilaLuwc' # own key
    #'''
    
    if apiUserType:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    else:
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,proxy=proxyURL, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]))
    
    testAPI(api)
    return api

import json
class customParser(tweepy.parsers.ModelParser):
    def parse(self, method, payload):
        result = super(customParser, self).parse(method, payload)
        result._payload = json.loads(payload)
        return result
