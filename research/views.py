import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Research, Article
from .services.generation_service import start_background_generation


# =========================================================
# HTML PAGES
# =========================================================

def dashboard(request):
    researches = Research.objects.all().order_by("-created_at")

    context = {
        "researches": researches,
        "total_count": researches.count(),
        "completed_count": researches.filter(
            status="completed"
        ).count(),
        "in_progress_count": researches.filter(
            status="in_progress"
        ).count(),
        "failed_count": researches.filter(
            status="failed"
        ).count(),
    }

    return render(
        request,
        "dashboard.html",
        context,
    )


# =========================================================
# HTML: ALL RESEARCH / HISTORY
# =========================================================

def all_research(request):
    researches = Research.objects.all().order_by("-created_at")

    context = {
        "researches": researches,
        "total_count": researches.count(),
        "completed_count": researches.filter(
            status="completed"
        ).count(),
        "in_progress_count": researches.filter(
            status="in_progress"
        ).count(),
        "failed_count": researches.filter(
            status="failed"
        ).count(),
    }

    return render(
        request,
        "all_research.html",
        context,
    )


# =========================================================
# HTML: ARTICLES
# =========================================================

def articles(request):
    completed_researches = (
        Research.objects.filter(
            status="completed"
        )
        .select_related("article")
        .order_by("-created_at")
    )

    return render(
        request,
        "articles.html",
        {
            "researches": completed_researches,
        },
    )


# =========================================================
# HTML: CREATE NEW RESEARCH
# =========================================================

def new_research(request):
    if request.method == "POST":
        topic = request.POST.get(
            "topic",
            "",
        ).strip()

        instructions = request.POST.get(
            "instructions",
            "",
        ).strip()

        article_length = request.POST.get(
            "article_length",
            "medium",
        )

        tone = request.POST.get(
            "tone",
            "professional",
        )

        if topic:
            research = Research.objects.create(
                topic=topic,
                instructions=instructions,
                article_length=article_length,
                tone=tone,
                status="in_progress",
                current_stage="research",
            )

            start_background_generation(
                research.id
            )

            return redirect(
                "processing",
                research_id=research.id,
            )

    return render(
        request,
        "new_research.html",
    )


# =========================================================
# HTML: PROCESSING PAGE
# =========================================================

def processing(request, research_id):
    research = get_object_or_404(
        Research,
        id=research_id,
    )

    return render(
        request,
        "processing.html",
        {
            "research": research,
        },
    )


# =========================================================
# HTML: RESULT PAGE
# =========================================================

def result(request, research_id):
    research = get_object_or_404(
        Research,
        id=research_id,
    )

    article = get_object_or_404(
        Article,
        research=research,
    )

    context = {
        "research": research,
        "article": article,
        "word_count": len(
            article.content.split()
        ),
    }

    return render(
        request,
        "result.html",
        context,
    )


# =========================================================
# HTML: RESEARCH STATUS
# =========================================================

def research_status(request, research_id):
    research = get_object_or_404(
        Research,
        id=research_id,
    )

    article_exists = Article.objects.filter(
        research=research
    ).exists()

    return JsonResponse({
        "id": research.id,
        "status": research.status,
        "current_stage": research.current_stage,
        "article_exists": article_exists,
        "result_url": (
            f"/research/{research.id}/result/"
        ),
    })


# =========================================================
# API HELPERS
# =========================================================

def research_to_dict(research):
    return {
        "id": research.id,
        "topic": research.topic,
        "instructions": research.instructions,
        "article_length": research.article_length,
        "tone": research.tone,
        "status": research.status,
        "current_stage": research.current_stage,
        "created_at": research.created_at.isoformat(),
    }


def article_to_dict(article):
    return {
        "id": article.id,
        "research_id": article.research_id,
        "title": article.title,
        "content": article.content,
        "word_count": len(
            article.content.split()
        ),
        "created_at": article.created_at.isoformat(),
        "updated_at": article.updated_at.isoformat(),
    }


# =========================================================
# API 1: LIST + CREATE RESEARCH
#
# GET  /api/research/
# POST /api/research/
# =========================================================

@csrf_exempt
def api_research_collection(request):

    # -------------------------
    # GET - List all research
    # -------------------------
    if request.method == "GET":
        researches = Research.objects.all().order_by(
            "-created_at"
        )

        return JsonResponse({
            "count": researches.count(),
            "results": [
                research_to_dict(research)
                for research in researches
            ],
        })

    # -------------------------
    # POST - Create research
    # -------------------------
    if request.method == "POST":
        try:
            data = json.loads(
                request.body or "{}"
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "error": "Invalid JSON body."
                },
                status=400,
            )

        topic = str(
            data.get(
                "topic",
                "",
            )
        ).strip()

        if not topic:
            return JsonResponse(
                {
                    "error": "Topic is required."
                },
                status=400,
            )

        instructions = str(
            data.get(
                "instructions",
                "",
            )
        ).strip()

        article_length = data.get(
            "article_length",
            "medium",
        )

        tone = data.get(
            "tone",
            "professional",
        )

        valid_lengths = {
            choice[0]
            for choice in Research.LENGTH_CHOICES
        }

        valid_tones = {
            choice[0]
            for choice in Research.TONE_CHOICES
        }

        if article_length not in valid_lengths:
            return JsonResponse(
                {
                    "error": (
                        "Invalid article_length. "
                        "Use short, medium, or long."
                    )
                },
                status=400,
            )

        if tone not in valid_tones:
            return JsonResponse(
                {
                    "error": (
                        "Invalid tone. "
                        "Use professional, casual, "
                        "academic, or friendly."
                    )
                },
                status=400,
            )

        research = Research.objects.create(
            topic=topic,
            instructions=instructions,
            article_length=article_length,
            tone=tone,
            status="pending",
            current_stage="research",
        )

        return JsonResponse(
            {
                "message": (
                    "Research created successfully."
                ),
                "research": research_to_dict(
                    research
                ),
            },
            status=201,
        )

    return JsonResponse(
        {
            "error": "Method not allowed."
        },
        status=405,
    )


# =========================================================
# API 2: RESEARCH DETAIL
#
# GET /api/research/{id}/
# =========================================================

def api_research_detail(
    request,
    research_id,
):

    if request.method != "GET":
        return JsonResponse(
            {
                "error": (
                    "Only GET method is allowed."
                )
            },
            status=405,
        )

    research = get_object_or_404(
        Research,
        id=research_id,
    )

    response = research_to_dict(
        research
    )

    article = Article.objects.filter(
        research=research
    ).first()

    if article:
        response["article"] = (
            article_to_dict(article)
        )
    else:
        response["article"] = None

    return JsonResponse(
        response
    )


# =========================================================
# API 3: START GENERATION
#
# POST /api/research/{id}/generate/
# =========================================================

@csrf_exempt
def api_research_generate(
    request,
    research_id,
):

    if request.method != "POST":
        return JsonResponse(
            {
                "error": (
                    "Only POST method is allowed."
                )
            },
            status=405,
        )

    research = get_object_or_404(
        Research,
        id=research_id,
    )

    if research.status not in [
        "pending",
        "failed",
        "completed",
    ]:
        return JsonResponse(
            {
                "error": (
                    "Research is already being "
                    "generated."
                ),
                "research": research_to_dict(
                    research
                ),
            },
            status=409,
        )

    research.status = "in_progress"
    research.current_stage = "research"

    research.save(
        update_fields=[
            "status",
            "current_stage",
        ]
    )

    start_background_generation(
        research.id
    )

    return JsonResponse(
        {
            "message": (
                "Article generation started."
            ),
            "research": research_to_dict(
                research
            ),
        },
        status=202,
    )


# =========================================================
# API 4: GET ARTICLE
#
# GET /api/research/{id}/article/
# =========================================================

def api_research_article(
    request,
    research_id,
):

    if request.method != "GET":
        return JsonResponse(
            {
                "error": (
                    "Only GET method is allowed."
                )
            },
            status=405,
        )

    research = get_object_or_404(
        Research,
        id=research_id,
    )

    article = get_object_or_404(
        Article,
        research=research,
    )

    return JsonResponse(
        article_to_dict(article)
    )


# =========================================================
# API 5: UPDATE ARTICLE
#
# PUT /api/articles/{id}/
# =========================================================

@csrf_exempt
def api_article_update(
    request,
    article_id,
):

    if request.method != "PUT":
        return JsonResponse(
            {
                "error": (
                    "Only PUT method is allowed."
                )
            },
            status=405,
        )

    article = get_object_or_404(
        Article,
        id=article_id,
    )

    try:
        data = json.loads(
            request.body or "{}"
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "Invalid JSON body."
            },
            status=400,
        )

    title = str(
        data.get(
            "title",
            article.title,
        )
    ).strip()

    content = str(
        data.get(
            "content",
            article.content,
        )
    ).strip()

    if not title:
        return JsonResponse(
            {
                "error": (
                    "Title cannot be empty."
                )
            },
            status=400,
        )

    if not content:
        return JsonResponse(
            {
                "error": (
                    "Content cannot be empty."
                )
            },
            status=400,
        )

    article.title = title
    article.content = content
    article.save()

    return JsonResponse(
        {
            "message": (
                "Article updated successfully."
            ),
            "article": article_to_dict(
                article
            ),
        }
    )


# =========================================================
# HTML: EDIT ARTICLE
# =========================================================

def edit_article(
    request,
    article_id,
):

    article = get_object_or_404(
        Article,
        id=article_id,
    )

    if request.method == "POST":
        title = request.POST.get(
            "title",
            "",
        ).strip()

        content = request.POST.get(
            "content",
            "",
        ).strip()

        if title and content:
            article.title = title
            article.content = content
            article.save()

            return redirect(
                "result",
                research_id=article.research_id,
            )

    return render(
        request,
        "edit_article.html",
        {
            "article": article,
            "research": article.research,
        },
    )