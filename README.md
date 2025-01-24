# 🏗️ Procore CA Scraper

Welcome to **Procore CA Scraper**! 🚀 This tool helps you extract contractor data from the Canadian Procore website, focusing on **General Contractors** and **Specialty Contractors** in each province. The scraped data is stored in a database and made accessible via a shiny **FastAPI** application.  

---

## ✨ Features

🌟 **Scrapy-powered scraping** for reliable data extraction.  
🌟 Filters data by **Company Type** (General Contractors and Specialty Contractors).  
🌟 Organizes data neatly in a database for easy querying.  
🌟 Accessible via a **FastAPI** endpoint.  
🌟 Ready for deployment on platforms like **Railway.app**.  

---

## 🛠️ Setup & Installation

1. **Clone the Repo** 🐾  
   ```bash
   git clone https://github.com/yourusername/procore-ca-scraper.git
   cd procore-ca-scraper
   ```
2. **Create a Virtual Environment** 🌍
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```  
3. **Install Dependencies** 📦
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Your Database** 🗂️
<br>Make sure your database is up and running! Update the connection settings in settings.py or your .env file.
5. **Run the Scraper** 🕷️
   ```bash
   scrapy crawl contractors
   ```
6. **Explore the API** 🌐
   <br>Open http://127.0.0.1:8000/docs to test out the API endpoints.

## 🚀 Deployment on Railway.app
You can deploy this app privately on Railway.app (or any platform of your choice). Here’s how:

1. Create a project on Railway.app 🛠️.
2. Push your repo to Railway via GitHub integration.
3. Configure your environment variables (e.g., database URL).
4. Deploy! Share it securely via screenshots or documentation. 📸
<br><br>Note: For security, deployment instructions are shared through screenshots, ensuring the Procore website link is kept private.

## 🙏 Acknowledgement
Thanks for checking out Procore CA Contractors Scraper. Feel free to reach out if you have questions, suggestions, or just want to chat about web scraping! 😊
