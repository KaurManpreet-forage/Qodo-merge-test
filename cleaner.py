import html2text
import requests
from bs4 import BeautifulSoup

def _clean_html_to_markdown(html_content, remove_elements=True):
    """
    Core function to clean HTML and convert to markdown
    
    Args:
        html_content (str): Raw HTML content
        remove_elements (bool): Remove header, footer, aside, nav, a tags
    
    Returns:
        str: Cleaned markdown content
    """
    if remove_elements:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted elements
        unwanted_tags = ['header', 'footer', 'aside', 'nav', 'script', 'style', 'meta', 'link']
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Remove <a> tags but keep text content
        for a_tag in soup.find_all('a'):
            a_tag.unwrap()
        
        html_content = str(soup)
    
    # Configure html2text
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.body_width = 0  # Don't wrap lines
    
    # Convert to markdown
    markdown_content = h.handle(html_content)
    
    return markdown_content.strip()


def fetch_and_clean_html(url, remove_elements=True, timeout=10):
    """
    Fetch HTML from URL and convert to clean text
    
    Args:
        url (str): URL to fetch
        remove_elements (bool): Remove header, footer, aside, nav, a tags
        timeout (int): Request timeout in seconds
    
    Returns:
        str: Cleaned markdown content
    """
    try:
        # Fetch HTML from URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        return _clean_html_to_markdown(response.text, remove_elements)
        
    except requests.RequestException as e:
        return f"Error fetching URL: {e}"
    except Exception as e:
        return f"Error processing HTML: {e}"


def process_page_to_clean_markdown(page, remove_elements=True):
    """
    Process page content to clean markdown
    
    Args:
        page: Page object with .html attribute or string content
        remove_elements (bool): Remove header, footer, aside, nav, a tags
    
    Returns:
        str: Cleaned markdown content
    """
    html_content = page.html if hasattr(page, "html") else str(page)
    return _clean_html_to_markdown(html_content, remove_elements)


def clean_html_string(html_content, remove_elements=True):
    """
    Clean HTML string and convert to markdown
    
    Args:
        html_content (str): Raw HTML content
        remove_elements (bool): Remove header, footer, aside, nav, a tags
    
    Returns:
        str: Cleaned markdown content
    """
    return _clean_html_to_markdown(html_content, remove_elements)


# Example usage
if __name__ == "__main__":
    # Example 1: Fetch from URL
    url = "https://www.gamweb.com"
    clean_text = fetch_and_clean_html(url)
    print("Cleaned content from URL:")
    print(clean_text)
    print("\n" + "="*50 + "\n")
