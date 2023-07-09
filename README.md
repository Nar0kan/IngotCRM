# <center>IngotCRM</center>

<!-- PROJECT LOGO -->
<div id="readme-top">
<br />
<div align="center">
  <a href="https://github.com/Nar0kan/IngotCRM">
    <img src="static/images/logo.png" alt="IngotCRM Logo" width="80" height="80">
  </a>

  <h3 align="center">IngotCRM</h3>

  <p align="center">
    CRM system to manage your Agents/Leads/Documents
    <br/><br/>
    <a href="https://ingot-crm.vercel.app/" target="_blank">View Demo</a>
    ·
    <a href="https://github.com/Nar0kan/IngotCRM/issues" target="_blank">Report Bug</a>
    ·
    <a href="https://github.com/Nar0kan" target="_blank">Contact</a>
  </p>
</div>
</div>


<!-- TABLE OF CONTENTS -->
<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about">About</a></li>
    <li><a href="#how-to-deploy">How to deploy</a></li>
    <li><a href="#technologies">Technologies</a></li>
    <li><a href="#screenshots">Screenshots</a></li>
    <li><a href="#sources">Sources</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
<div id="about">
  <p>IngotCRM is my project to manage Leads, Agents, and Documents and explore even more. It has CRUD+L principle, Authentication, 
    Filter, and Pagination features connected via views, PayPal API, custom TailwindCSS design, Static Files Collection, and Media Files represented as Documents. 
    Users can create their accounts (Organisations) and via these accounts add more (Agents). Each agent can be assigned to a Lead. Documents can be related 
    to specific Leads and, besides, can have a secret mark.</p>
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- HOW TO DEPLOY -->
### INSTALLATION
<div id="how-to-deploy">

To deploy this project in localhost consider next:

1) You will need to have S3 bucket. If you are not having any - in your .env file set USE_S3 to FALSE.
2) You need to connect to your own PostgreSQL Database. Deploy it localy, or through the web. Otherwice change the Settings.py file.
3) You might wanna use different credentials for Paypal. Don't forget to change the veriables in .env file.
4) For Email variables you can use your own Gmail account, or just create a new one, as it is running with Gmail SMTP.
5) Before you run the server set READ_FROM_DOT_ENV_FILE default to True in Settings.py

## STEPS

1. Clone the project
  ```sh
  git clone https://github.com/Nar0kan/IngotCRM.git
  ```
  or download the zip file...

2. Create your virtual environment and activate it
  ```sh
  python -m venv venv
  venv\Scripts\activate
  ```

3. Install dependencies from <a href="https://github.com/Nar0kan/IngotCRM/blob/main/requirements.txt" target="_blank">requirements.txt</a> file
  ```sh
  pip install -r requirements.txt
  ```
   
4. Create your own .env file in /ingotcrm directory and fill it up with your own data (example - <a href="https://github.com/Nar0kan/IngotCRM/blob/main/ingotcrm/.template.env" target="_blank">.template.env</a>)

5. Change settings.py file default to True and run server

  ![image](https://github.com/Nar0kan/IngotCRM/assets/79106222/b3fc9261-fc49-47a4-bdab-e78a4fa2fd92)

   ```sh
   python manage.py runserver
   ```
</div>
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- TECHNOLOGIES -->
## Technologies
<div id="technologies">

<div align="center">Languages & Frameworks</div>

* Python
* HTML5
* CSS3
* Django
* PostgreSQL
* TaiwindCSS
* JQuery

<div align="center">Modules</div>

* django-crispy-forms
* django-environ
* django-filter
* django-jquery
* django-paypal
* django-storages
* boto3
* psycopg2-binary
* whitenoise
</div>
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap
<div id="screenshots">
  
<div align="center">
  <p>Landing page</p>
  <a href="https://ibb.co/NKDkhY5"><img src="https://i.ibb.co/89vR38q/Screenshot-3.png" alt="Screenshot-3" border="0" target="_blank"></a>

  <p>Leads page</p>
  <a href="https://ibb.co/8Xq55K3"><img src="https://i.ibb.co/Fn2wwxv/Screenshot-4.png" alt="Screenshot-4" border="0" target="_blank"></a>
  
  <p>Lead details page</p>
  <a href="https://ibb.co/M28bwfL"><img src="https://i.ibb.co/3rfw6vH/Screenshot-5.png" alt="Screenshot-5" border="0" target="_blank"></a>
  
  <p>Agent details page</p>
  <a href="https://ibb.co/7pjgPxK"><img src="https://i.ibb.co/z2Q8pWZ/Screenshot-6.png" alt="Screenshot-6" border="0" target="_blank"></a>

  <p>Documents page</p>
  <a href="https://ibb.co/sCvjCRx"><img src="https://i.ibb.co/MfDnfSw/Screenshot-7.png" alt="Screenshot-7" border="0" target="_blank"></a>
</div>

</div>
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- SOURCES -->
## Sources
<div id="sources">

<ul>
  <li>Youtube guides
    <ul>
      <li>
        <a href="https://www.youtube.com/watch?v=fOukA4Qh9QA&t=17133s&pp=ygUKZGphbmdvIGNybQ%3D%3D" target="_blank">Idea</a>
      </li>
      <li>
        <a href="https://www.youtube.com/@zackplauche" target="_blank">APIs</a>
      </li>
      <li>
        <a href="https://www.youtube.com/@DennisIvy/videos" target="_blank">Other</a>
      </li>
    </ul>
  </li>
  <li>Documentation</li>
  <ul>
      <li>
        <a href="https://django-filter.readthedocs.io/en/stable/" target="_blank">Filters</a>
      </li>
      <li>
        <a href="https://whitenoise.readthedocs.io/en/latest/" target="_blank">Whitenoise</a>
      </li>
      <li>
        <a href="https://docs.djangoproject.com/en/4.2/topics/email/" target="_blank">Mails</a>
      </li>
      <li>
        <a href="https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/" target="_blank">Generic views</a>
      </li>
    </ul>
  <li>Stack Overflow</li>
</ul>

</div>
<p align="right">(<a href="#readme-top">back to top</a>)</p>
