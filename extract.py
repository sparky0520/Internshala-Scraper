import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def extract_data(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the required details
        data = {}

        # 1. Big Heading (class="heading_2_4 heading_title")
        big_heading = soup.find('h1', class_='heading_2_4 heading_title')
        data['Big Heading'] = big_heading.text.strip() if big_heading else 'N/A'

        # 2. Job Title (class="heading_4_5 profile")
        job_title = soup.find('div', class_='heading_4_5 profile')
        data['Job Title'] = job_title.text.strip() if job_title else 'N/A'

        # 3. Company Name (class="heading_6 company_name")
        company_name = soup.find('div', class_='heading_6 company_name')
        data['Company Name'] = company_name.text.strip() if company_name else 'N/A'

        # 4. Location (id="location_names")
        location = soup.find('div', id='location_names')
        data['Location'] = location.text.strip() if location else 'N/A'

        # 5. Stipend (class="stipend")
        stipend = soup.find('span', class_='stipend')
        data['Stipend'] = stipend.text.strip() if stipend else 'N/A'

        # 6. Salary (class="item_body salary")
        salary = soup.find('span', class_='item_body salary')
        data['Salary'] = salary.text.strip() if salary else 'N/A'

        # 7. Experience Required (class="other_detail_item job-experience-item")
        experience_required = soup.find('div', class_='other_detail_item job-experience-item')
        data['Experience Required'] = experience_required.text.strip() if experience_required else 'N/A'

        # 8. Apply By (Internship: class="other_detail_item apply_by", Job: class="item_body")
        apply_by_internship = soup.find('div', class_='other_detail_item apply_by')
        data['Apply By (Internship)'] = apply_by_internship.text.strip() if apply_by_internship else 'N/A'

        apply_by_job = soup.find_all('span', class_='item_body')
        data['Apply By (Job)'] = apply_by_job[4].text.strip() if len(apply_by_job) > 4 else 'N/A'

        # Add URL
        data['Apply Link'] = url

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return {'Big Heading': 'N/A', 'Job Title': 'N/A', 'Company Name': 'N/A', 'Location': 'N/A',
                'Stipend': 'N/A', 'Salary': 'N/A', 'Experience Required': 'N/A',
                'Apply By (Internship)': 'N/A', 'Apply By (Job)': 'N/A', 'Apply Link': url}
