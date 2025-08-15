# Configurações para os scrappers

MAX_NEWS_PER_CATEGORY = 20
ITEMS_PER_CATEGORY_PAGE = 10

TARGET_CATEGORIES = {
    'economia': 'c46d078f-4753-47a0-8d87-94a9b1230dd3',
    'saude': 'b504eb45-a42b-4d85-a163-d618fcd33d6d',
    'educacao': '0a78db0c-a35b-49ae-8696-70a1ee15cef6',
    'mundo': 'dd647bff-9afc-47b2-b421-3875d8cf60d8',
    'politica': '1b9deafa-9519-48a2-af13-5db036018bad',
    'meio ambiente': '2e1fc644-6743-47b7-8438-9cf9b97fd483',
    'tecnologia': 'e361f955-0b39-4647-aecf-5ff3c6c137cc',
    'turismo': '8e3adac4-8d23-4d38-ae76-35ae3eb3e81a',
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

DELAY_RANGE = (1, 3)

