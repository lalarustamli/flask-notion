import requests
import config

NOTION_API_KEY = config.NOTION_TOKEN

headers = {
    'Authorization': 'Bearer ' + NOTION_API_KEY,
    'Notion-Version': '2021-05-13',
    "content-type": "application/json"
}

MAPPING_CONTENT_TYPE = {
    'paragraph': 'p',
    'heading_1': 'h1',
    'heading_2': 'h2',
    'heading_3': 'h3',
    'child_page': 'a',
    'to_do': 'li',
    'bulleted_list_item': 'li',
    'unsupported': None
}

def get_api_results(URL):
    return requests.get(URL, headers=headers).json()


def get_page_title(page_id):
    URL = f"https://api.notion.com/v1/pages/{page_id}"
    raw_results = get_api_results(URL)
    return raw_results['properties']['title']['title'][0]['text']['content']


def get_block_children(block_id):
    URL = f"https://api.notion.com/v1/blocks/{block_id}/children"
    raw_results = get_api_results(URL)
    return raw_results.get('results')


def get_database(db_id):
    URL = f"https://api.notion.com/v1/databases/{db_id}"
    raw_results = get_api_results(URL)
    return raw_results.get('results')


def get_attr_classes(item):
    item_class = ''
    for key, value in item['annotations']:
        if value:
            item_class = key
            item_class.append(f' {key}')
    return item_class


def parse_text_item(item, raw_html, tag):
    if len(item.get(item['type']).get('text')) > 1:
        for x in item.get(item['type']).get('text'):
            url = x['text']['link']
            content = x['plain_text']
            if url:
                html = f'<a href={url}>{content} </a>'
            else:
                html = f'<{tag}> {content} </{tag}>'
            raw_html += html
    else:
        content = item.get(item['type']).get('text')[0]['plain_text']
        html = f'<{tag}> {content} </{tag}><br>'
        raw_html += html
    return raw_html


def parse_content(block_id):
    raw_data = get_block_children(block_id)
    raw_html = ''
    for item in raw_data:
        tag = MAPPING_CONTENT_TYPE[item['type']]
        if item.get(item['type']).get('text'):
            raw_html = parse_text_item(item, raw_html, tag)
        else:
            content = item.get(item['type']).get('title')
            if content:
                html = f'<{tag} href={item.get("id")}>🗎  {content} </{tag}><br>'
                raw_html += html
    return raw_html
