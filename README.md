# AI-Powered Multi-Agent Research Article Generator

A Django-based web application that uses CrewAI and multiple AI agents to research a topic, plan the article structure, and generate a complete research article through an easy-to-use web interface.

## Features

* Create research requests with:

  * Topic
  * Additional instructions
  * Article length
  * Writing tone
* Multi-agent AI workflow:

  * Research Agent
  * Planning Agent
  * Writing Agent
* Processing status display
* Generated article result page
* Article title and content display
* Word count and generated date
* Edit and save generated articles
* Copy article content
* Download articles as PDF files
* Dashboard with research statistics
* Research history
* Completed articles listing
* View previous generated articles
* SQLite database for development
* Django REST API endpoints
* Background article generation using Python threading
* Clean and responsive user interface

## Application Workflow

```text
User enters research topic
        ↓
Research Agent
        ↓
Planning Agent
        ↓
Writing Agent
        ↓
Final Article Generated
        ↓
User can view, edit, copy, download, and save article
```

## Technology Stack

### Backend

* Python
* Django
* Django REST Framework
* SQLite
* CrewAI
* Gemini API
* Python Threading

### Frontend

* Django Templates
* HTML
* CSS
* JavaScript

### AI

* CrewAI sequential multi-agent workflow
* Gemini LLM integration
* Three specialized AI agents:

  * Research Agent
  * Planning Agent
  * Writing Agent

## Project Structure

```text
Multi_AI_Research_Submission/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── research/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services/
│   │   ├── ai_service.py
│   │   └── generation_service.py
│   ├── migrations/
│   └── templatetags/
│
├── templates/
│   ├── dashboard.html
│   ├── new_research.html
│   ├── processing.html
│   ├── result.html
│   ├── edit_article.html
│   ├── all_research.html
│   └── articles.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│
├── manual_tests/
│   ├── test_anthropic_manual.py
│   ├── test_groq_manual.py
│   └── test_gemini.py
│
├── db.sqlite3
├── main.py
├── manage.py
├── requirements.txt
└── README.md
```

## Database Models

### Research

Stores research request information.

Fields include:

* Topic
* Instructions
* Article length
* Tone
* Status
* Current processing stage
* Created date

### Article

Stores the generated article.

Fields include:

* Related research
* Article title
* Article content
* Created date
* Updated date

## Requirements

* Python 3.10 or higher
* pip
* Gemini API key
* Internet connection for AI generation

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SwethaVenkat31/Multi_AI_Agent_Research_Articles.git
```

```bash
cd Multi_AI_Agent_Research_Articles
```

### 2. Create a Virtual Environment

#### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\Activate.ps1
```

#### macOS/Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure the API Key

Create a `.env` file in the project root directory.

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your actual Gemini API key.

Do not upload the `.env` file to GitHub.

## Database Setup

Run migrations:

```bash
python manage.py migrate
```

## Run the Application

Start the Django development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## How to Use the Application

1. Open the dashboard.
2. Click **New Research**.
3. Enter the research topic.
4. Add additional instructions if required.
5. Select article length.
6. Select the writing tone.
7. Click **Generate Article**.
8. Monitor the processing stages:

   * Research Agent
   * Planning Agent
   * Writing Agent
9. View the generated article.
10. Copy the article content if needed.
11. Download the article as a PDF.
12. Edit the article and save changes.
13. View previous research from the history section.
14. Open completed articles from the Articles section.

## API Endpoints

### Create Research

```http
POST /api/research/
```

Example request:

```json
{
  "topic": "Artificial Intelligence in Healthcare",
  "instructions": "Write a detailed research article with practical examples",
  "article_length": "Medium",
  "tone": "Professional"
}
```

### List Research

```http
GET /api/research/
```

### Get Research Details

```http
GET /api/research/{id}/
```

### Generate Article

```http
POST /api/research/{id}/generate/
```

### Get Generated Article

```http
GET /api/research/{id}/article/
```

### Update Article

```http
PUT /api/articles/{id}/
```

Example request:

```json
{
  "title": "Updated Article Title",
  "content": "Updated article content"
}
```

## AI Agent Workflow

The application uses a sequential CrewAI workflow.

### 1. Research Agent

Collects and organizes relevant information about the selected topic.

### 2. Planning Agent

Creates the article structure, sections, and logical flow.

### 3. Writing Agent

Uses the research and plan to generate the final article.

The AI logic is separated from Django views through service modules.

## Background Processing

Article generation runs in the background using Python threading so that the web application can display processing progress while the AI agents are working.

The user can see the current stage without exposing internal AI reasoning.

## Testing

Run Django system checks:

```bash
python manage.py check
```

Run Django tests:

```bash
python manage.py test
```

Manual AI provider test scripts are available inside:

```text
manual_tests/
```

## Troubleshooting

### API Key Error

Make sure the `.env` file exists and contains:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Migration Error

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Server Not Starting

Check that the virtual environment is activated and all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Article Generation Failure

Check:

* Internet connection
* Gemini API key
* API quota
* Terminal error messages
* Correct Python environment

## Application Screenshots

Screenshots of the application interface can be found in the `screenshots/` directory.

## Future Improvements

Possible future enhancements include:

* User authentication
* PostgreSQL database support
* PDF export improvements
* WebSocket-based live updates
* Celery and Redis task processing
* Multiple LLM provider support
* Docker deployment
* Advanced article search and filtering
* Improved article formatting
* Cloud deployment

## Project Status

The application currently supports the complete basic workflow:

* Research creation
* Multi-agent article generation
* Processing status
* Article viewing
* Article editing
* Article saving
* Article copying
* PDF downloading
* Research history
* Completed article listing

## Author

**Swetha S V**

GitHub:
[SwethaVenkat31](https://github.com/SwethaVenkat31)

Repository:
[AI-Powered Multi-Agent Research Article Generator](https://github.com/SwethaVenkat31/Multi_AI_Agent_Research_Articles)
