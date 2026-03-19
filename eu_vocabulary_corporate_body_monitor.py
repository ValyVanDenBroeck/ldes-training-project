"""
╔═══════════════════════════════════════════════════════════════════╗
║     EU Vocabularies - Corporate Body Version Monitor              ║
╠═══════════════════════════════════════════════════════════════════╣
║  Fetches available versions of the Corporate Body authority       ║
║  table from the EU Publications Office using their RDF endpoint.  ║
║                                                                   ║
║  Dataset: Corporate Body (corporate-body)                         ║
║  Source:  https://op.europa.eu/en/web/eu-vocabularies              ║
║                                                                   ║
║  Usage:                                                           ║
║    from eu_vocabulary_monitor import CorporateBodyMonitor         ║
║    monitor = CorporateBodyMonitor()                               ║
║    versions = monitor.get_available_versions()                    ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import requests
import re
from rdflib import Graph


class CorporateBodyMonitor:
    """Fetches available versions of the EU Corporate Body authority table."""
    
    DATASET_ID = "corporate-body"
    BASE_URL = "http://publications.europa.eu/resource/dataset"
    
    def get_available_versions(self):
        """Get all available versions via RDF content negotiation."""
        url = f"{self.BASE_URL}/{self.DATASET_ID}"
        response = requests.get(url, headers={"Accept": "application/rdf+xml"})
        
        # Extract version patterns (YYYYMMDD-0) from the RDF
        versions = set()
        pattern = rf"{self.DATASET_ID}/(\d{{8}}-\d)"
        
        for match in re.findall(pattern, response.text):
            versions.add(match)
        
        return sorted(versions, reverse=True)
    
    def get_latest_versions(self, count=2):
        """Get the N most recent versions."""
        versions = self.get_available_versions()
        return versions[:count]
    
    def get_download_url(self, version):
        """Get download URL for a specific version."""
        return f"{self.BASE_URL}/{self.DATASET_ID}/{version}"
    
    def download_version(self, version):
        """Download and parse a version as RDF graph."""
        url = self.get_download_url(version)
        response = requests.get(url, headers={"Accept": "application/rdf+xml"})
        
        graph = Graph()
        graph.parse(data=response.content, format="xml")
        return graph


if __name__ == "__main__":
    print("🔍 EU Vocabularies - Corporate Body Monitor\n")
    
    monitor = CorporateBodyMonitor()
    versions = monitor.get_available_versions()
    
    print(f"✅ Found {len(versions)} versions")
    print(f"   Latest: {versions[0]}")
    print(f"   Oldest: {versions[-1]}")
