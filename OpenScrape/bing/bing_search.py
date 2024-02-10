import requests
from bs4 import BeautifulSoup

def search(query:str, num_results:int):
    """
    Searches Bing with the specified search term and retrieves a specified number of search results.

    Args:
        query (str): The search term.
        num_results (int): The number of search results to retrieve.

    Returns:
        list: A list of search results. Each search result is a dictionary containing a title, a link, and a description.

    Raises:
        requests.exceptions.RequestException: If the GET request fails.
        bs4.BeautifulSoup.Error: If HTML parsing fails.

    Note:
        This function depends on the HTML structure of Bing. If Bing changes its structure, this function may not work correctly.
        Also, be careful not to violate Bing's terms of use.
    """
    url = "https://www.bing.com/search"
    params = {
        "q": query,
    }
    results_list = []
    while len(results_list) < num_results:
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('li', class_='b_algo')
        for result in results:
            if len(results_list) >= num_results:
                break
            title = result.find('h2').text
            link = result.find('a')['href']
            description = result.find('p').text if result.find('p') else ''
            results_list.append({
                "title": title,
                "link": link,
                "description": description
            })
        next_page = soup.find('a', class_='sb_pagN')
        if next_page:
            url = "https://www.bing.com" + next_page['href']
        else:
            break
    return results_list
