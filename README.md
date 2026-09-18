# AI-Powered Multi-Agent Research Article Generator

A Django-based web application that uses a CrewAI multi-agent workflow to research a topic, plan an article, and generate a complete research article through a simple web interface.

The application provides a dashboard, research creation form, agent-processing status, article results, editing, history, and REST-style JSON API endpoints.

---

## Features

- Create new research articles
- Enter research topic and custom instructions
- Select article length
- Select article tone
- Multi-agent article generation using CrewAI
- Research Agent
- Planning Agent
- Writing Agent
- Processing status page
- View generated articles
- Edit and save articles
- Copy article content
- Download article as a text file
- View previous research history
- REST-style JSON API endpoints
- SQLite database support
- Background article generation using Python threading

---

## Application Workflow

```text
User
 |
 | Enter topic, instructions, length, and tone
 v
Create Research
 |
 v
Research Agent
 |
 v
Planning Agent
 |
 v
Writing Agent
 |
 v
Final Article Generated
 |
 v
View / Edit / Copy / Download Article
```

---

## Multi-Agent Architecture

The application uses three sequential AI agents:

### 1. Research Agent

Collects and organizes relevant information about the given topic.

### 2. Planning Agent

Creates a structured article outline and determines the flow of the content.

### 3. Writing Agent

Uses the research and plan to generate the final article.

The agents are executed sequentially using CrewAI.

---

## Technology Stack

### Backend

- Python
- Django
- Django JSON API views
- SQLite

### AI and Agent Framework

- CrewAI
- Google Gemini LLM
- Python-based AI service integration

### Frontend

- Django Templates
- HTML
- CSS
- JavaScript

### Development Tools

- Git
- Virtual Environment
- Django Development Server

---

## Project Structure

```text
Multi_AI_Agent_Research_Articles-main/
|
|-- manage.py
|-- main.py
|-- requirements.txt
|-- README.md
|-- db.sqlite3
|
|-- config/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|
|-- research/
|   |-- models.py
|   |-- views.py
|   |-- urls.py
|   |-- admin.py
|   |-- tests.py
|   |
|   |-- migrations/
|   |
|   `-- services/
|       |-- ai_service.py
|       `-- generation_service.py
|
|-- templates/
|   |-- dashboard.html
|   |-- new_research.html
|   |-- processing.html
|   |-- result.html
|   `-- edit_article.html
|
`-- static/
    `-- css/
        `-- style.css
```

---

## Database Models

### Research

The `Research` model stores the details and status of each research request.

Fields include:

- Topic
- Instructions
- Article length
- Tone
- Status
- Current agent stage
- Created date

Possible research statuses:

- Pending
- In Progress
- Completed
- Failed

Possible processing stages:

- Research Agent
- Planning Agent
- Writing Agent
- Completed
- Failed

### Article

The `Article` model stores the generated article associated with a research request.

Fields include:

- Research reference
- Article title
- Article content
- Created date
- Updated date

Each research record can have one generated article.

---

## Requirements

Install the required Python packages using the `requirements.txt` file.

```powershell
pip install -r requirements.txt
```

Make sure Python is installed on your system.

---

## Environment Variables

Create a `.env` file in the project root directory.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your actual Google Gemini API key.

Do not commit the `.env` file to GitHub.

---

## Database Setup

Run the following commands from the project root directory.

```powershell
python manage.py makemigrations
python manage.py migrate
```

These commands create and update the SQLite database tables.

---

## Run the Application

Start the Django development server:

```powershell
python manage.py runserver
```

Open the following URL in your browser:

```text
http://127.0.0.1:8000/
```

---

## How to Use the Application

1. Open the application dashboard.
2. Click **New Research**.
3. Enter a research topic.
4. Add optional instructions.
5. Select the article length.
6. Select the article tone.
7. Click **Generate Article**.
8. The application starts the multi-agent workflow.
9. The processing page displays the current agent stage.
10. After completion, the generated article is displayed.
11. The article can be:
    - Viewed
    - Edited
    - Copied
    - Downloaded
    - Generated again

---

## REST API Endpoints

### 1. Get All Research Records

```http
GET /api/research/
```

Returns a list of all research requests.

---

### 2. Create a Research Request

```http
POST /api/research/
```

Example request body:

```json
{
  "topic": "The Future of Solar Energy",
  "instructions": "Explain the benefits and challenges of solar energy.",
  "article_length": "short",
  "tone": "professional"
}
```

---

### 3. Get Research Details

```http
GET /api/research/{id}/
```

Returns the details of a specific research request and its article if available.

---

### 4. Start Article Generation

```http
POST /api/research/{id}/generate/
```

Starts the background article-generation workflow.

---

### 5. Get Generated Article

```http
GET /api/research/{id}/article/
```

Returns the article associated with a research request.

---

### 6. Update an Article

```http
PUT /api/articles/{id}/
```

Example request body:

```json
{
  "title": "Updated Solar Energy Research",
  "content": "Updated article content goes here."
}
```

---

## Example API Workflow

### Create Research

```powershell
$body = @{
    topic = "The Future of Solar Energy"
    instructions = "Explain the benefits and challenges of solar energy."
    article_length = "short"
    tone = "professional"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/research/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Start Generation

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/research/1/generate/" `
    -Method POST
```

Replace `1` with the actual research ID.

### Check Research Status

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/research/1/" `
    -Method GET
```

### Get the Article

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/research/1/article/" `
    -Method GET
```

---

## Running the Original CrewAI Workflow

The original AI workflow can also be executed directly through `main.py`.

```powershell
python main.py
```

The workflow performs the following steps:

```text
Research Agent
    |
Planning Agent
    |
Writing Agent
    |
Final Article
```

The Django application reuses this existing AI workflow through the AI service layer.

---

## Background Processing

Article generation runs in a background thread so that the Django web application remains responsive while the AI agents are working.

The generation process updates the research status and current stage:

```text
Pending
   |
   v
In Progress
   |
   v
Research Agent
   |
   v
Planning Agent
   |
   v
Writing Agent
   |
   v
Completed
```

If an error occurs during generation, the research status is updated to:

```text
Failed
```

---

## AI Service Separation

The AI logic is kept separate from the Django views.

The main service files are:

```text
research/services/ai_service.py
research/services/generation_service.py
```

### `ai_service.py`

Connects the Django application with the existing CrewAI workflow.

### `generation_service.py`

Handles:

- Background generation
- Agent stage updates
- Article creation
- Research status updates
- Error handling

This separation keeps the Django application organized and makes the AI workflow easier to maintain.

---

## Testing

Run Django checks:

```powershell
python manage.py check
```

Run the Django test suite:

```powershell
python manage.py test
```

The API endpoints can also be tested using:

- PowerShell
- Postman
- Browser GET requests
- REST clients

---

## Troubleshooting

### Django Server Does Not Start

Make sure the virtual environment is activated and dependencies are installed.

```powershell
pip install -r requirements.txt
```

### Database Errors

Run migrations again:

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Gemini API Error

Check whether the `.env` file contains a valid API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Article Generation Fails

Check:

- Gemini API key
- Internet connection
- API rate limits
- Terminal output
- Django server logs

### Port Already in Use

Run Django on another port:

```powershell
python manage.py runserver 8001
```

Then open:

```text
http://127.0.0.1:8001/
```

---

## Future Improvements

Possible future improvements include:

- User authentication
- PostgreSQL database
- PDF article export
- Rich text editor
- WebSocket-based live progress updates
- Celery-based background processing
- Redis task queue
- Multiple LLM provider support
- Article search and filtering
- Improved article version history
- Docker support
- Deployment to a cloud platform

---

## Project Status

The application currently supports:

- Django web interface
- Research creation
- Multi-agent article generation
- Research status tracking
- Article result page
- Article editing
- Article copying
- Article downloading
- Research history
- REST-style API endpoints
- SQLite database persistence

The complete workflow is:

```text
Create Research
    |
    v
Run AI Agents
    |
    v
Generate Article
    |
    v
View Article
    |
    v
Edit / Save / Copy / Download
```

---

## Author

Developed as part of a multi-agent AI research article generator project using Django and CrewAI.