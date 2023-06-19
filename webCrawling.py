import requests
from bs4 import BeautifulSoup

# Make a request to the website
r = requests.get('https://www.youtube.com/@OpeninApp')
# Create an object to parse the HTML format
soup = BeautifulSoup(r.content, 'html.parser')
# Retrieve all popular news links
link = []
for i in soup.find('div', {'class': 'contentContainer'}).find_all('a'):
    i['href'] = i['href'] + '?page=all'
    link.append(i['href'])
# For each link, we retrieve paragraphs from it, combine each paragraph as one string, and save it to documents (Fig. 2)
documents = []
for i in link:
    # Make a request to the link
    r = requests.get(i)

    # Initialize BeautifulSoup object to parse the content
    soup = BeautifulSoup(r.content, 'html.parser')

    # Retrieve all paragraphs and combine it as one
    sen = []
    for i in soup.find('div', {'class': 'style-scope ytd-browse'}).find_all('div'):
        sen.append(i.text)

    # Add the combined paragraphs to documents
    documents.append(' '.join(sen))
    print(documents)

    import re

    documents_clean = []
    for d in documents:
        # Remove Unicode
        document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
        # Remove Mentions
        document_test = re.sub(r'@\w+', '', document_test)
        # Lowercase the document
        document_test = document_test.lower()
        # Remove punctuations
        #document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
        # Lowercase the numbers
        document_test = re.sub(r'[0-9]', '', document_test)
        # Remove the doubled space
        document_test = re.sub(r'\s{2,}', ' ', document_test)
        documents_clean.append(document_test)
        print(documents_clean)


