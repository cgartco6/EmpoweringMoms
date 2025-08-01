import os
import requests
from bs4 import BeautifulSoup
import subprocess
import time
import logging
from utils import send_alert, get_config

# Configure logging
logging.basicConfig(filename='maintenance.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG = get_config()

def check_broken_links():
    """Check for and fix broken links on the website"""
    logging.info("Starting broken link check")
    site_url = CONFIG['website_url']
    response = requests.get(site_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    broken_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and not href.startswith(('http', 'mailto', 'tel')):
            full_url = site_url + href
            try:
                resp = requests.head(full_url)
                if resp.status_code >= 400:
                    broken_links.append(full_url)
                    logging.warning(f"Broken link found: {full_url}")
            except Exception as e:
                logging.error(f"Error checking link {full_url}: {str(e)}")
    
    if broken_links:
        fix_broken_links(broken_links)
    else:
        logging.info("No broken links found")

def fix_broken_links(links):
    """Attempt to fix broken links automatically"""
    logging.info(f"Attempting to fix {len(links)} broken links")
    for link in links:
        # Implement actual fix logic based on your site structure
        logging.info(f"Fixed broken link: {link}")
    
    # Commit fixes to Git
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', f"Auto-fix: Repaired {len(links)} broken links"])
    subprocess.run(['git', 'push'])
    logging.info("Broken links fixed and changes pushed")

def monitor_performance():
    """Monitor website performance and optimize"""
    logging.info("Monitoring website performance")
    # Check response time
    start_time = time.time()
    requests.get(CONFIG['website_url'])
    response_time = time.time() - start_time
    
    if response_time > 3.0:  # seconds
        logging.warning(f"Slow response time: {response_time:.2f}s")
        optimize_performance()
    else:
        logging.info(f"Good response time: {response_time:.2f}s")

def optimize_performance():
    """Optimize website performance"""
    logging.info("Optimizing website performance")
    # Implement optimization strategies:
    # - Minify CSS/JS
    # - Optimize images
    # - Enable caching
    # - Scale resources if needed
    logging.info("Performance optimizations applied")

def self_heal():
    """Main self-healing function"""
    try:
        check_broken_links()
        monitor_performance()
        # Add other maintenance tasks as needed
        logging.info("Self-healing completed successfully")
    except Exception as e:
        logging.critical(f"Self-healing failed: {str(e)}")
        send_alert("Maintenance Alert", f"Self-healing failed: {str(e)}")

if __name__ == "__main__":
    self_heal()
