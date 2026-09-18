from django.contrib import admin
from django.urls import path

from research import views


urlpatterns = [
    path("admin/", admin.site.urls),

    # =====================================================
    # HTML PAGES
    # =====================================================

    # Dashboard
    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    # All Research / History
    path(
        "research/",
        views.all_research,
        name="all_research",
    ),

    # Articles
    path(
        "articles/",
        views.articles,
        name="articles",
    ),

    # Create New Research
    path(
        "research/new/",
        views.new_research,
        name="new_research",
    ),

    # Processing Page
    path(
        "research/<int:research_id>/processing/",
        views.processing,
        name="processing",
    ),

    # Result Page
    path(
        "research/<int:research_id>/result/",
        views.result,
        name="result",
    ),

    # Research Status
    path(
        "research/<int:research_id>/status/",
        views.research_status,
        name="research_status",
    ),

    # Edit Article
    path(
        "articles/<int:article_id>/edit/",
        views.edit_article,
        name="edit_article",
    ),

    # =====================================================
    # API ENDPOINTS
    # =====================================================

    # GET  /api/research/
    # POST /api/research/
    path(
        "api/research/",
        views.api_research_collection,
        name="api_research_collection",
    ),

    # GET /api/research/{id}/
    path(
        "api/research/<int:research_id>/",
        views.api_research_detail,
        name="api_research_detail",
    ),

    # POST /api/research/{id}/generate/
    path(
        "api/research/<int:research_id>/generate/",
        views.api_research_generate,
        name="api_research_generate",
    ),

    # GET /api/research/{id}/article/
    path(
        "api/research/<int:research_id>/article/",
        views.api_research_article,
        name="api_research_article",
    ),

    # PUT /api/articles/{id}/
    path(
        "api/articles/<int:article_id>/",
        views.api_article_update,
        name="api_article_update",
    ),
]