# Jop Portal For Django
<p align="center">
    <img src="img/logo1.png">
</p>
<p align="center">
    <a href="#Git" alt="Git">
        <img src="https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white" />
    </a>
    <a href="https://github/OZX-OG" alt="Github">
        <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/>
    </a>
    <a href="https://www.djangoproject.com/" alt="Django">
        <img src="https://img.shields.io/badge/-Django-092E20.svg?style=for-the-badge&logo=django"/>
    </a>
    <a href="https://python.org/" alt="Python">
        <img src="https://img.shields.io/badge/-Python3-F7D756.svg?style=for-the-badge&logo=python"/>
    </a>
    <a href="https://www.selenium.dev/" alt="selenium">
        <img src="https://img.shields.io/badge/selenium-00AE00.svg?style=for-the-badge&logo=selenium&logoColor=white"/>
    </a>
</p>

This Django-based job portal aggregates Django-related job listings from Indeed and LinkedIn using Selenium for web scraping. Focused solely on Django jobs, the portal streamlines the job search process. Additionally, it includes a RESTful API for programmatically accessing job data.


## Installation

1. Make sure you have Python 3.x installed on your system.

2. Clone the repository:
```bash
git clone https://github.com/OZX-OG/JobPortal-django.git
```
3. Set Up Virtual Environment:
Ensure you have virtual environments installed on your machine. If not, install them using:
```bash
pip install virtualenv
```

4. Create a Virtual Environment:
Navigate to the project directory and create a virtual environment:
```bash
virtualenv venv
```

5. Activate the Virtual Environment:

   - On Windows:
      ```bash
      venv\Scripts\activate
      ```
      
   - On Unix or MacOS::
      ```bash
      source venv/bin/activate
      ```

6. Install the required packages:

```bash
pip install -r requirements.txt
```

7. Start the Server:
Once all requirements are installed, start the Django server:
```bash
python manage.py runserver
```

8. Access the Portal:
Open a web browser and navigate to the URL displayed in the terminal where the Django server is running:

## Celery Configuration & Scraping :

1. **Update CELERY_BROKER_URL:**
   - In `settings.py`, update the `CELERY_BROKER_URL` with the URL provided by  [Railway](https://railway.app/).
     ```python
     CELERY_BROKER_URL = 'redis://default:NhmAigipb1kn3el1N4DaDEpnl1PpNcCe@viaduct.proxy.rlwy.net:39379'
     ```

2. **Start Celery Worker:**
   - Open a command prompt and run the following command to start the Celery worker:
     ```
     celery -A JobPortal worker -l INFO --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo
     ```

3. **Scraping Data with Selenium:**
   - To initiate scraping data with Selenium, use the following URLs:
     - `/scrape_linkedin/`: Scrapes job listings from LinkedIn.
     - `/scrape_indeed/`: Scrapes job listings from Indeed.
     - `/clear/`: Clears all unavailable jobs from both LinkedIn and Indeed.

Now your Celery worker is up and running, and you can start scraping data by accessing the provided URLs.
:

## API Information:

1. **Random Job Endpoint:**
   - Endpoint: `/api/random/`
   - Description: Access this endpoint to retrieve a random job listing without authentication. Each refresh provides a new random job.
   - JSON Response Template:
     ```json
     {
       "title": "{{ Job Title }}",
       "company": "{{ Company Name }}",
       "link": "{{ Job Link }}",
       "salary": "{{ salary }}",
       "specific_location": "{{ Location }}",
       "publish_date": "{{ Publish Date }}"
     }
     ```

2. **Authenticated Job Listings Endpoint:**
   - Endpoint: `/api/`
   - Description: Requires authentication with a token in the header (`'Authorization': 'Token {{ Your Token }}'`) to access all jobs in the database.
   - JSON Request Header Template (for authentication):
     ```json
     {
       "Authorization": "Token {{ Your Token }}"
     }
     ```
   - JSON Response Template:
     ```json
     {
       "source": "{{ Source }}",
       "location": ["{{ Location }}"],
       "title": "{{ Job Title }}",
       "company": "{{ Company Name }}",
       "job_link": "{{ Job Link }}",
       "company_url": "{{ Company URL }}",
       "image_url": "{{ Image URL }}",
       "salary": "{{ salary }}",
       "specific_location": "{{ Location }}",
       "applications": "{{ Applications }}",
       "seniority_level": "{{ Seniority Level }}",
       "employment_type": "{{ Employment Type }}",
       "Industries": "{{ Industries }}",
       "post_date": "{{ Post Date }}",
       "remote": "{{ Remote }}",
       "publish": "{{ Publish Date }}",
       "slug": "{{ Slug }}",
       "is_active": "{{ Is Active }}"
     }
     ```
   - Error Message Template (if token not provided):
     ```json
     {
         "detail": "Authentication credentials were not provided."
     }
     ```

Replace placeholders (`{{ }}`) with actual data when using the API endpoints. For the authenticated endpoint, ensure you include the correct token in the request header to access the job listings.



## Usage

To utilize the job portal:

- Ensure Django is installed and the project dependencies are met.
- Run the Django server.
- Navigate to the portal's URL in a web browser.
- Use the search functionality to find Django job listings fetched from Indeed and LinkedIn.
## Contributing

Contributions are always welcome!

Feel free to submit pull requests or open issues for any enhancements or bug fixes.


## Acknowledgements

We would like to express our gratitude to the following individuals and organizations for their contributions and support:

- **Django Community**: Thank you to the Django community for providing an excellent web framework that powers this project.

- **Selenium Project**: We extend our appreciation to the Selenium project for their powerful tool that enables automated web testing and scraping.

- **Railway**: Special thanks to Railway for providing a Redis instance for one day, which greatly facilitated our task of setting up Celery for asynchronous task processing.


## 📝 License

- [MIT License](https://github.com/OZX-OG/JobPortal-django/blob/master/LICENSE)
