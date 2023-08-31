import requests
from bs4 import BeautifulSoup
import csv

class ProjectsAndTendersScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def fetch_data(self):
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data from {self.base_url}: {e}")
            return None

    def parse_data(self, html_content):
        data = []
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Example parsing logic: Assuming projects are in <div class="project">
        project_divs = soup.find_all("div", class_="project")
        
        for project_div in project_divs:
            project_name = project_div.find("h2").text
            description = project_div.find("p").text
            
            # Extract other relevant details as needed
            # e.g., location = project_div.find("span", class_="location").text
            
            data.append([project_name, description])
        
        return data

    def save_to_csv(self, data, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Project Name', 'Description'])  # Write header
            writer.writerows(data)

# Your main script
if __name__ == '__main__':
    sources = [
        {"url": "https://example.com/projects", "filename": "projects.csv"},
        # Add more source URLs and filenames as needed
    ]
    
    for source in sources:
        scraper = ProjectsAndTendersScraper(source["url"])
        try:
            html_content = scraper.fetch_data()
            
            if html_content is None:
                print(f"Failed to fetch data from {source['url']}")
                continue
                
            extracted_data = scraper.parse_data(html_content)
            
            if extracted_data:
                scraper.save_to_csv(extracted_data, source["filename"])
                print(f"Data saved for {source['filename']}")
            else:
                print(f"No data extracted from {source['url']}")
        except requests.RequestException as request_error:
            print(f"Request error occurred while processing {source['url']}: {request_error}")
        except Exception as e:
            print(f"An error occurred while processing {source['url']}: {str(e)}")
