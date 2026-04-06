#!/usr/bin/env python3
"""
Fetch publications from NASA ADS API and save to Hugo data file.
"""

import os
import json
import requests
from datetime import datetime, timezone

def fetch_ads_publications(token, orcid):
    """Fetch publications from ADS API using ORCID, then supplement with author name search.
    Filters out large collaboration papers (LVK, etc.) where author count > 50."""

    base_url = "https://api.adsabs.harvard.edu/v1/search/query"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    fields = 'bibcode,title,author,first_author,pubdate,pub,abstract,doi,arxiv_class,citation_count,read_count,property'

    results = []

    # 1. ORCID-linked papers
    try:
        r = requests.get(base_url, params={'q': f'orcid:{orcid}', 'fl': fields, 'sort': 'date desc', 'rows': 200}, headers=headers)
        r.raise_for_status()
        results += r.json().get('response', {}).get('docs', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ORCID publications: {e}")

    # 2. Author name search — catches papers not yet ORCID-linked
    try:
        r = requests.get(base_url, params={'q': 'author:"Khadkikar, Sanika"', 'fl': fields, 'sort': 'date desc', 'rows': 200}, headers=headers)
        r.raise_for_status()
        results += r.json().get('response', {}).get('docs', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching author-name publications: {e}")

    # Deduplicate by bibcode, filter out pre-2020 false matches
    seen = set()
    filtered = []
    for pub in results:
        bibcode = pub.get('bibcode', '')
        if not bibcode or bibcode in seen:
            continue
        seen.add(bibcode)
        # Skip obviously wrong old papers (false name matches before 2020)
        pubdate = pub.get('pubdate', '')
        year = int(pubdate.split('-')[0]) if pubdate else 0
        if year < 2020:
            continue
        filtered.append(pub)

    return filtered

def process_publication(pub):
    """Process a single publication record."""
    
    # Extract year from pubdate (format: YYYY-MM-DD or YYYY-MM)
    pubdate = pub.get('pubdate', '')
    year = ''
    if pubdate:
        year = pubdate.split('-')[0]
    
    # Get authors and determine authorship position
    authors = pub.get('author', [])
    # Collapse large collaboration author lists
    if len(authors) > 30:
        collab_names = [a for a in authors[:5] if 'Collaboration' in a or 'collaboration' in a]
        if collab_names:
            author_string = 'LIGO Scientific Collaboration, Virgo Collaboration, KAGRA Collaboration'
        else:
            author_string = '; '.join(authors[:6]) + '; et al.'
    else:
        author_string = '; '.join(authors) if authors else 'Unknown'
    
    # Determine authorship position for Sanika Khadkikar
    authorship_position = "other"
    author_position = None

    for i, author in enumerate(authors):
        if 'Khadkikar, Sanika' in author or 'Khadkikar, S.' in author:
            author_position = i + 1
            if i == 0:
                authorship_position = "first"
            else:
                authorship_position = "other"
            break

    # Highlight Sanika Khadkikar
    if len(authors) > 30:
        collab_names = [a for a in authors[:5] if 'Collaboration' in a or 'collaboration' in a]
        if collab_names:
            author_string_highlighted = 'LIGO Scientific Collaboration, Virgo Collaboration, KAGRA Collaboration (incl. <strong>Khadkikar, Sanika</strong>)'
        else:
            author_string_highlighted = author_string.replace('Khadkikar, Sanika', '<strong>Khadkikar, Sanika</strong>').replace('Khadkikar, S.', '<strong>Khadkikar, S.</strong>')
    else:
        author_string_highlighted = author_string.replace(
            'Khadkikar, Sanika', '<strong>Khadkikar, Sanika</strong>'
        ).replace(
            'Khadkikar, S.', '<strong>Khadkikar, S.</strong>'
        )
    
    # Get DOI URL
    doi = pub.get('doi', [])
    doi_url = f"https://doi.org/{doi[0]}" if doi else None
    
    # Get ADS URL
    bibcode = pub.get('bibcode', '')
    ads_url = f"https://ui.adsabs.harvard.edu/abs/{bibcode}/abstract" if bibcode else None
    
    # Check if refereed
    properties = pub.get('property', [])
    is_refereed = 'REFEREED' in properties
    
    processed = {
        'title': pub.get('title', ['Untitled'])[0] if pub.get('title') else 'Untitled',
        'authors': author_string,
        'authors_highlighted': author_string_highlighted,
        'authorship_position': authorship_position,
        'author_position': author_position,
        'journal': pub.get('pub', 'Unknown Journal'),
        'year': year,
        'pubdate': pubdate,
        'abstract': pub.get('abstract', ''),
        'bibcode': bibcode,
        'ads_url': ads_url,
        'doi_url': doi_url,
        'citation_count': pub.get('citation_count', 0),
        'read_count': pub.get('read_count', 0),
        'is_refereed': is_refereed,
        'arxiv_class': pub.get('arxiv_class', [])
    }
    
    return processed

def get_manual_publications():
    """Return a list of manually specified publications (bibcodes) that should be included."""
    
    manual_bibcodes = [
        # Add bibcodes here for papers not yet linked to ORCID in ADS
        # Example: "2024arXivXXXXXXXXXK",
    ]
    
    return manual_bibcodes

def fetch_manual_publications(token, bibcodes):
    """Fetch specific publications by bibcode."""
    
    if not bibcodes:
        return []
    
    base_url = "https://api.adsabs.harvard.edu/v1/search/query"
    
    # Create query for specific bibcodes
    bibcode_query = ' OR '.join([f'bibcode:{bc}' for bc in bibcodes])
    
    params = {
        'q': bibcode_query,
        'fl': 'bibcode,title,author,first_author,pubdate,pub,abstract,doi,arxiv_class,citation_count,read_count,property,metrics',
        'sort': 'date desc',
        'rows': len(bibcodes)
    }
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        return data.get('response', {}).get('docs', [])
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching manual publications: {e}")
        return []

def main():
    """Main function to fetch and save publications."""
    
    # Get environment variables
    token = os.getenv('ADS_TOKEN')
    orcid = os.getenv('ORCID')
    
    if not token:
        print("Error: ADS_TOKEN environment variable not set")
        return
    
    if not orcid:
        print("Error: ORCID environment variable not set")
        return
    
    print(f"Fetching publications for ORCID: {orcid}")
    
    # Fetch ORCID-linked publications
    orcid_publications = fetch_ads_publications(token, orcid)
    print(f"Found {len(orcid_publications)} ORCID-linked publications")
    
    # Fetch manual publications
    manual_bibcodes = get_manual_publications()
    manual_publications = []
    if manual_bibcodes:
        manual_publications = fetch_manual_publications(token, manual_bibcodes)
        print(f"Found {len(manual_publications)} manual publications")
    
    # Combine and deduplicate
    all_publications = orcid_publications + manual_publications
    seen_bibcodes = set()
    unique_publications = []
    
    for pub in all_publications:
        bibcode = pub.get('bibcode', '')
        if bibcode and bibcode not in seen_bibcodes:
            seen_bibcodes.add(bibcode)
            unique_publications.append(pub)
    
    if not unique_publications:
        print("No publications found or error occurred")
        return
    
    print(f"Total unique publications: {len(unique_publications)}")
    
    # Process publications
    processed_pubs = [process_publication(pub) for pub in unique_publications]
    
    # Create output data
    output_data = {
        'last_updated': datetime.now(timezone.utc).isoformat(),
        'total_publications': len(processed_pubs),
        'orcid': orcid,
        'publications': processed_pubs
    }
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to Hugo data file
    with open('data/publications.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Publications saved to data/publications.json")
    print(f"Last updated: {output_data['last_updated']}")

if __name__ == '__main__':
    main()