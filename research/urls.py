from django.urls import path

from . import views


urlpatterns = [
    # HTML pages
    path("", views.dashboard, name="dashboard"),

    path(
        "research/",
        views.all_research,
        name="all_research",
    ),

    path(
        "new/",
        views.new_research,
        name="new_research",
    ),

    path(
        "<int:research_id>/processing/",
        views.processing,
        name="processing",
    ),

    path(
        "<int:research_id>/result/",
        views.result,
        name="result",
    ),

    path(
        "<int:research_id>/status/",
        views.research_status,
        name="research_status",
    ),

    # Required APIs
    path(
        "api/research/",
        views.api_research_collection,
        name="api_research_collection",
    ),

    path(
        "api/research/<int:research_id>/",
        views.api_research_detail,
        name="api_research_detail",
    ),

    path(
        "api/research/<int:research_id>/generate/",
        views.api_research_generate,
        name="api_research_generate",
    ),

    path(
        "api/research/<int:research_id>/article/",
        views.api_research_article,
        name="api_research_article",
    ),

    path(
        "api/articles/<int:article_id>/",
        views.api_article_update,
        name="api_article_update",
    ),
]