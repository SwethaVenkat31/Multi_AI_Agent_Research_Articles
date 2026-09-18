import sys
from pathlib import Path

# Add the project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import run_crew


def generate_article(
    topic,
    instructions="",
    article_length="medium",
    tone="professional",
    progress_callback=None,
):
    """
    Generate an article using the CrewAI multi-agent pipeline.

    Workflow:
        Research Agent → Planning Agent → Writing Agent
    """

    if not topic or not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    # Notify the generation service about the current stage.
    def update_progress(stage):
        if progress_callback:
            progress_callback(stage)

    # Initial stage
    update_progress("research")

    # Run the CrewAI pipeline
    result = run_crew(
        topic=topic.strip(),
        instructions=instructions,
        article_length=article_length,
        tone=tone,
        progress_callback=progress_callback,
    )

    result_text = str(result).strip()

    return {
        "title": topic.strip(),
        "content": result_text,
        "word_count": len(result_text.split()),
    }