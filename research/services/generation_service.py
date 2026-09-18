import threading
import traceback

from django.db import close_old_connections

from ..models import Research, Article
from .ai_service import generate_article


def update_stage(research_id, stage):
    research = Research.objects.get(id=research_id)

    research.current_stage = stage
    research.status = "in_progress"

    research.save(
        update_fields=[
            "current_stage",
            "status",
        ]
    )

    print(
        f"[Research {research_id}] "
        f"Stage updated to: {stage}",
        flush=True,
    )


def generate_research_in_background(research_id):
    close_old_connections()

    print(
        f"[Research {research_id}] "
        "Background generation started.",
        flush=True,
    )

    try:
        research = Research.objects.get(
            id=research_id
        )

        print(
            f"[Research {research_id}] "
            f"Topic: {research.topic}",
            flush=True,
        )

        update_stage(
            research_id,
            "research",
        )

        print(
            f"[Research {research_id}] "
            "Calling generate_article()...",
            flush=True,
        )

        result = generate_article(
            topic=research.topic,
            instructions=research.instructions,
            article_length=research.article_length,
            tone=research.tone,
            progress_callback=lambda stage: update_stage(
                research_id,
                stage,
            ),
        )

        print(
            f"[Research {research_id}] "
            "generate_article() completed.",
            flush=True,
        )

        Article.objects.update_or_create(
            research=research,
            defaults={
                "title": result["title"],
                "content": result["content"],
            },
        )

        research.status = "completed"
        research.current_stage = "completed"

        research.save(
            update_fields=[
                "status",
                "current_stage",
            ]
        )

        print(
            f"[Research {research_id}] "
            "Generation completed successfully.",
            flush=True,
        )

    except Exception as error:
        print(
            f"[Research {research_id}] "
            "Generation failed.",
            flush=True,
        )

        print(
            str(error),
            flush=True,
        )

        traceback.print_exc()

        try:
            research = Research.objects.get(
                id=research_id
            )

            research.status = "failed"
            research.current_stage = "failed"

            research.save(
                update_fields=[
                    "status",
                    "current_stage",
                ]
            )

        except Exception:
            traceback.print_exc()

    finally:
        close_old_connections()

        print(
            f"[Research {research_id}] "
            "Background thread finished.",
            flush=True,
        )


def start_background_generation(research_id):
    print(
        f"[Research {research_id}] "
        "Starting background thread...",
        flush=True,
    )

    thread = threading.Thread(
        target=generate_research_in_background,
        args=(research_id,),
        daemon=True,
    )

    thread.start()

    print(
        f"[Research {research_id}] "
        "Background thread launched.",
        flush=True,
    )