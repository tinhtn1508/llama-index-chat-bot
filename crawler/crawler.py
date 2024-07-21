import requests
import hashlib
import re
import os
import config
import json

LLAMA_INDEX_BLOGS_URL = 'https://www.llamaindex.ai/blog'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Authorization': 'Bearer {}'.format(config.conf['crawler']['jina_api_key'])
}

def list_llama_index_blogs() -> list:
    jina_reader_url = 'https://r.jina.ai/{}'.format(LLAMA_INDEX_BLOGS_URL)
    response = requests.get(url=jina_reader_url, headers=HEADERS, timeout=30)
    if response.status_code != 200:
        raise Exception('Failed to fetch the page: {}, err: {}'.format(jina_reader_url, response.text))
    raw_text = response.text
    raw_text = raw_text.split("Markdown Content:")[1].split('\n')
    pattern = r"\[(.*?)\]\((.*?)\)"
    tmpArray = []
    for i in range(0, len(raw_text)):
        if raw_text[i].strip() == '':
            continue
        match = re.search(pattern, raw_text[i])
        if match:
            tmpArray.append(match.group(1))
            tmpArray.append(match.group(2))
        else:
            tmpArray.append(raw_text[i].strip())
    result = []
    for i in range(0, len(tmpArray)-5, 5):
        result.append({
            "title": tmpArray[i+2],
            "url": tmpArray[i+3],
            "date": tmpArray[i+4],
            "image": tmpArray[i+1],
        })
    return result

def get_blog_detail(url: str, response_type: str) -> str:
    jina_reader_url = 'https://r.jina.ai/{}'.format(url)
    header = HEADERS
    header['x-respond-with'] = response_type
    response = requests.get(url=jina_reader_url, headers=header, timeout=60)
    if response.status_code != 200:
        raise Exception('Failed to fetch the page: {}, err: {}'.format(jina_reader_url, response.text))
    return response.text

def store_blog_detail(meta: dict, text: str, markdown: str) -> None:
    file_name = hashlib.md5(meta['url'].encode()).hexdigest()
    if not os.path.exists(config.conf['crawler']['data_path']):
        os.makedirs(config.conf['crawler']['data_path'])
    path = '{}/{}.json'.format(config.conf['crawler']['data_path'], file_name)
    if os.path.exists(path):
        print('The file {} already exists, skip storing'.format(file_name))
        return
    print('Start storing the blog detail to file: {}'.format(path))
    with open(path, 'w') as f:
        f.write(json.dumps({
            'meta': meta,
            'text_content': text,
            'markdown_content': markdown
        }))
