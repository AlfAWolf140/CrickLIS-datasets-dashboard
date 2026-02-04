#!/usr/bin/env python3
"""
Query OpenAlex API for datasets created by researchers at the Francis Crick Institute.
"""

import requests
import json
import time

def get_crick_datasets(per_page=200, max_results=None):
    """
    Retrieve datasets from the Francis Crick Institute using OpenAlex API.
    
    Args:
        per_page: Number of results per page (max 200)
        max_results: Maximum number of results to retrieve (None for all)
    
    Returns:
        List of dataset works
    """
    base_url = "https://api.openalex.org/works"
    
    # The Francis Crick Institute ROR ID
    crick_ror = "https://ror.org/029chgv08"
    
    # Parameters to filter for datasets from Crick Institute
    params = {
        "filter": f"institutions.ror:{crick_ror},type:dataset",
        "per-page": per_page,
        "mailto": "beth.montague-hellen@crick.a.uk"  # Replace with your email for polite pool
    }
    
    all_datasets = []
    page = 1
    
    print(f"Querying OpenAlex for datasets from Francis Crick Institute...")
    print(f"ROR ID: {crick_ror}\n")
    
    while True:
        params["page"] = page
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            meta = data.get("meta", {})
            
            if not results:
                break
            
            all_datasets.extend(results)
            
            print(f"Page {page}: Retrieved {len(results)} datasets")
            print(f"Total so far: {len(all_datasets)}")
            print(f"Total available: {meta.get('count', 'unknown')}\n")
            
            # Check if we've reached max_results or end of data
            if max_results and len(all_datasets) >= max_results:
                all_datasets = all_datasets[:max_results]
                break
            
            if len(results) < per_page:
                break
            
            page += 1
            time.sleep(0.1)  # Be polite to the API
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break
    
    return all_datasets


def save_datasets(datasets, filename="crick_datasets.json"):
    """Save datasets to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(datasets, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(datasets)} datasets to {filename}")


def print_summary(datasets):
    """Print a summary of the retrieved datasets."""
    print("\n" + "="*80)
    print("SUMMARY OF FRANCIS CRICK INSTITUTE DATASETS")
    print("="*80)
    print(f"\nTotal datasets found: {len(datasets)}\n")
    
    if datasets:
        print("Sample datasets (first 5):\n")
        for i, dataset in enumerate(datasets[:5], 1):
            title = dataset.get('title', 'No title')
            pub_year = dataset.get('publication_year', 'Unknown year')
            doi = dataset.get('doi', 'No DOI')
            open_access = dataset.get('open_access', {}).get('is_oa', False)
            
            print(f"{i}. {title}")
            print(f"   Year: {pub_year}")
            print(f"   DOI: {doi}")
            print(f"   Open Access: {open_access}")
            print()


def main():
    # Get all datasets (remove max_results limit to get all)
    datasets = get_crick_datasets(per_page=200)
    
    if datasets:
        # Save to JSON file
        save_datasets(datasets)
        
        # Print summary
        print_summary(datasets)
        
        print("\nDataset fields available:")
        if datasets:
            print(json.dumps(list(datasets[0].keys()), indent=2))
    else:
        print("\nNo datasets found or error occurred.")


if __name__ == "__main__":
    main()