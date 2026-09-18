"""
AI-Powered Multi-Agent System for Research and Article Generation
=================================================================

Agents:
    1. Research Agent  - Researches the topic
    2. Planning Agent  - Creates an article outline
    3. Writing Agent   - Writes the final article

Workflow:
    Research → Planning → Writing

Provider:
    Google Gemini through CrewAI

Usage:
    python main.py
"""

import os
import time
from pathlib import Path

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM


# ---------------------------------------------------------------------------
# Environment Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(
    dotenv_path=BASE_DIR / ".env",
    override=True,
)


# ---------------------------------------------------------------------------
# 1. LLM Configuration
# ---------------------------------------------------------------------------

def get_llm() -> LLM:
    """
    Configure Google Gemini through CrewAI.
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. "
            "Please configure it in the .env file."
        )

    return LLM(
        model="gemini/gemini-3.1-flash-lite",
        api_key=api_key.strip(),
        temperature=0.2,
        max_tokens=900,
    )


# ---------------------------------------------------------------------------
# 2. Agent Definitions
# ---------------------------------------------------------------------------

def create_research_agent(llm: LLM) -> Agent:
    """
    Research Agent:
    Produces concise and useful research notes.
    """

    return Agent(
        role="Senior Research Analyst",
        goal=(
            "Research the given topic and provide concise, accurate, "
            "well-organized research notes."
        ),
        backstory=(
            "You are an experienced research analyst who explains complex "
            "topics clearly and focuses on practical, useful information."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_planning_agent(llm: LLM) -> Agent:
    """
    Planning Agent:
    Converts research notes into a concise article structure.
    """

    return Agent(
        role="Content Strategist and Outline Architect",
        goal=(
            "Convert research notes into a clear and logical article outline "
            "with a title, introduction, body sections, and conclusion."
        ),
        backstory=(
            "You are a professional content strategist who creates simple, "
            "well-organized article structures."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_writing_agent(llm: LLM) -> Agent:
    """
    Writing Agent:
    Generates the final article using the outline.
    """

    return Agent(
        role="Professional Article Writer",
        goal=(
            "Write a complete, polished, readable article based on the "
            "research and outline."
        ),
        backstory=(
            "You are an experienced professional writer who produces "
            "well-structured articles in clear language."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


# ---------------------------------------------------------------------------
# 3. Task Definitions
# ---------------------------------------------------------------------------

def create_research_task(
    agent: Agent,
    topic: str,
    instructions: str = "",
) -> Task:
    """
    Research task.
    """

    extra_instructions = ""

    if instructions and instructions.strip():
        extra_instructions = (
            "\n\nAdditional user instructions:\n"
            f"{instructions.strip()}"
        )

    return Task(
        description=(
            "Research the following topic and prepare concise research notes.\n\n"
            f"Topic: {topic}"
            f"{extra_instructions}\n\n"
            "Cover:\n"
            "1. Important concepts\n"
            "2. Key developments\n"
            "3. Practical examples\n"
            "4. Benefits or applications\n"
            "5. Challenges or risks\n"
            "6. Future outlook\n\n"
            "Keep the research concise and under approximately 300 words. "
            "Avoid repetition, large tables, and unsupported statistics."
        ),
        expected_output=(
            "A concise research summary under approximately 300 words."
        ),
        agent=agent,
    )


def create_planning_task(
    agent: Agent,
    research_task: Task,
) -> Task:
    """
    Planning task based on research output.
    """

    return Task(
        description=(
            "Using the research summary, create a concise article outline.\n\n"
            "Include:\n"
            "1. One article title\n"
            "2. Introduction direction\n"
            "3. Three or four main body sections\n"
            "4. Key points under each section\n"
            "5. Conclusion direction\n\n"
            "Do not repeat the full research report. "
            "Keep the outline under approximately 180 words."
        ),
        expected_output=(
            "A concise Markdown article outline with title, sections, "
            "key points, and conclusion."
        ),
        agent=agent,
        context=[research_task],
    )


def create_writing_task(
    agent: Agent,
    planning_task: Task,
    article_length: str = "medium",
    tone: str = "professional",
) -> Task:
    """
    Writing task with controlled length and tone.
    """

    length_instructions = {
        "short": (
            "Write approximately 250-350 words. "
            "Keep the article complete and concise."
        ),
        "medium": (
            "Write approximately 400-500 words. "
            "Provide balanced coverage without repetition."
        ),
        "long": (
            "Write approximately 600-700 words. "
            "Provide useful explanations and examples."
        ),
    }

    selected_length = length_instructions.get(
        article_length.lower(),
        length_instructions["medium"],
    )

    tone_instructions = {
        "professional": (
            "Use a polished, professional, and informative tone."
        ),
        "casual": (
            "Use a conversational and approachable tone."
        ),
        "academic": (
            "Use a formal, analytical, and evidence-oriented tone."
        ),
        "friendly": (
            "Use a warm, engaging, and reader-friendly tone."
        ),
    }

    selected_tone = tone_instructions.get(
        tone.lower(),
        tone_instructions["professional"],
    )

    return Task(
        description=(
            "Using the research summary and article outline, write the final "
            "article.\n\n"
            f"Length requirement:\n{selected_length}\n\n"
            f"Tone requirement:\n{selected_tone}\n\n"
            "Requirements:\n"
            "- Return only the final article\n"
            "- Start with one Markdown title using #\n"
            "- Use three or four clear headings\n"
            "- Use short readable paragraphs\n"
            "- Include practical examples when useful\n"
            "- Avoid unsupported statistics\n"
            "- Do not include agent reasoning\n"
            "- Do not include notes about word count\n"
            "- End with a meaningful conclusion\n"
            "- Do not stop mid-sentence"
        ),
        expected_output=(
            "A complete, polished Markdown article with a title, "
            "introduction, structured sections, and conclusion."
        ),
        agent=agent,
        context=[planning_task],
    )


# ---------------------------------------------------------------------------
# 4. Crew Setup
# ---------------------------------------------------------------------------

def build_crew(
    topic: str,
    instructions: str = "",
    article_length: str = "medium",
    tone: str = "professional",
    progress_callback=None,
) -> Crew:
    """
    Build the sequential multi-agent Crew.

    Workflow:
        Research → Planning → Writing
    """

    llm = get_llm()

    researcher = create_research_agent(llm)
    planner = create_planning_agent(llm)
    writer = create_writing_agent(llm)

    research_task = create_research_task(
        agent=researcher,
        topic=topic,
        instructions=instructions,
    )

    planning_task = create_planning_task(
        agent=planner,
        research_task=research_task,
    )

    writing_task = create_writing_task(
        agent=writer,
        planning_task=planning_task,
        article_length=article_length,
        tone=tone,
    )

    if progress_callback:

        def research_completed_callback(task_output):
            print("Research Agent completed.")
            progress_callback("planning")
            return task_output

        def planning_completed_callback(task_output):
            print("Planning Agent completed.")
            progress_callback("writing")
            return task_output

        def writing_completed_callback(task_output):
            print("Writing Agent completed.")
            progress_callback("completed")
            return task_output

        research_task.callback = research_completed_callback
        planning_task.callback = planning_completed_callback
        writing_task.callback = writing_completed_callback

    return Crew(
        agents=[
            researcher,
            planner,
            writer,
        ],
        tasks=[
            research_task,
            planning_task,
            writing_task,
        ],
        process=Process.sequential,
        verbose=True,
    )


# ---------------------------------------------------------------------------
# 5. Crew Execution
# ---------------------------------------------------------------------------

def run_crew(
    topic: str,
    instructions: str = "",
    article_length: str = "medium",
    tone: str = "professional",
    progress_callback=None,
) -> str:
    """
    Run the complete multi-agent pipeline.

    Temporary errors such as 429 and 503 are retried automatically.
    """

    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    topic = topic.strip()

    print("\n" + "=" * 60)
    print("  Multi-Agent Article Generator")
    print(f"  Topic: {topic}")
    print(f"  Article Length: {article_length}")
    print(f"  Tone: {tone}")
    print("  Provider: Google Gemini")
    print("=" * 60 + "\n")

    if progress_callback:
        progress_callback("research")

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:
            print(
                f"\nStarting CrewAI execution attempt "
                f"{attempt}/{max_attempts}..."
            )

            crew = build_crew(
                topic=topic,
                instructions=instructions,
                article_length=article_length,
                tone=tone,
                progress_callback=progress_callback,
            )

            result = crew.kickoff()

            article = (
                result.raw
                if hasattr(result, "raw")
                else str(result)
            )

            article = str(article).strip()

            if not article:
                raise ValueError(
                    "The AI returned an empty article."
                )

            if progress_callback:
                progress_callback("completed")

            print("\n" + "=" * 60)
            print("  FINAL ARTICLE")
            print("=" * 60 + "\n")
            print(article)

            return article

        except Exception as error:

            error_text = str(error).lower()

            print("\n" + "=" * 60)
            print("Article generation failed.")
            print(f"Error type: {type(error).__name__}")
            print(f"Error details: {error}")
            print("=" * 60)

            is_temporary_error = (
                "429" in error_text
                or "rate limit" in error_text
                or "ratelimit" in error_text
                or "too many requests" in error_text
                or "503" in error_text
                or "service unavailable" in error_text
                or "temporarily unavailable" in error_text
                or "server error" in error_text
            )

            if is_temporary_error and attempt < max_attempts:

                wait_seconds = 20 * attempt

                print(
                    "\nTemporary Gemini service issue detected."
                )
                print(
                    f"Waiting {wait_seconds} seconds before retrying..."
                )

                time.sleep(wait_seconds)

            else:
                raise


# ---------------------------------------------------------------------------
# 6. Main Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    TOPIC = (
        "The Role of Artificial Intelligence in Cybersecurity"
    )

    run_crew(
        topic=TOPIC,
        instructions=(
            "Focus on threat detection, anomaly detection, malware and "
            "phishing prevention, incident response, practical examples, "
            "benefits, limitations, ethical concerns, and future developments."
        ),
        article_length="short",
        tone="professional",
    )