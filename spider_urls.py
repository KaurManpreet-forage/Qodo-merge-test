from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import os
import time
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

app = Flask(__name__)

# Define the proxy information
PROXY_SERVER = os.environ.get("PROXY_SERVER")
PROXY_USERNAME = os.environ.get("PROXY_USERNAME")
PROXY_PASSWORD = os.environ.get("PROXY_PASSWORD")

proxy = {
    'http': f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_SERVER.split("//")[1]}',
    'https': f'https://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_SERVER.split("//")[1]}',
}

@app.route('/crawl', methods=['GET'])
def crawl():
    url = request.args.get('url')
    depth = int(request.args.get('depth', 1))  # Get depth from query parameters, default to 1

    if not url:
        return jsonify({'error': 'Please provide a URL as a query parameter (e.g., /crawl?url=https://www.example.com)'}), 400

    print(f"Crawling started with depth: {depth}...")

    crawl_results = []

    try:
        crawl_recursive(url, crawl_results, depth)
    except Exception as e:
        error_message = f"Error while crawling {url}: {str(e)}"
        return jsonify({'error': error_message}), 500

    print("Crawling completed.")

    formatted_results = []
    parent_path_counts = defaultdict(int)
    for result in crawl_results:
        parsed_result_url = urlparse(result["url"])
        parent_path_counts[result.get("parent", "/")] += 1
        result_obj = {
            "input_url": url,
            "url": result["url"],
            "depth": result["depth"],
            "netloc": parsed_result_url.netloc,
            "urlpath": result.get("urlpath", "/"),
            "path_count": result.get("path_count", 0),
            "parent": result.get("parent", "/")
        }
        formatted_results.append(result_obj)

    stats = {
        "input_url": url,
        "total_urls_crawled": len(formatted_results),
        "total_parent_paths": len(parent_path_counts),
        "urls_per_parent_path": dict(parent_path_counts)
    }

    return jsonify({"results": formatted_results, "stats": stats})

def crawl_recursive(url, crawl_results, max_depth):
    visited_urls = set()

    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc

    def visit_page(url, current_depth):
        if url in visited_urls or current_depth > max_depth:
            return

        visited_urls.add(url)

        parsed_current_url = urlparse(url)
        path = parsed_current_url.path.lstrip('/')
        path_count = len([x for x in parsed_current_url.path.split('/') if x]) if parsed_current_url.path != '/' else 0
        parent = '/' if len(parsed_current_url.path.rstrip('/').split('/')) <= 1 or not parsed_current_url.path.rstrip('/').split('/')[-1] else '/'.join(parsed_current_url.path.rstrip('/').split('/')[:-1]) or '/'

        crawl_results.append({
            "url": url,
            "depth": current_depth,
            "netloc": parsed_current_url.netloc,
            "urlpath": path if path else "/",
            "path_count": path_count,
            "parent": parent
        })

        try:
            response = requests.get(url, proxies=proxy, timeout=120)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                base_url = response.url

                print(f"URL: {url}, Depth: {current_depth}, Netloc: {parsed_current_url.netloc}, Path: {parsed_current_url.path}, Path Count: {path_count}, Parent: {parent}")

                if current_depth < max_depth:
                    for link in soup.find_all('a'):
                        page_url = link.get('href')
                        if page_url:
                            full_url = urljoin(base_url, page_url)
                            parsed_full_url = urlparse(full_url)
                            if parsed_full_url.netloc == base_domain:
                                visit_page(full_url, current_depth + 1)
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

    visit_page(url, 0)

if __name__ == '__main__':
    app.run(debug=True)
