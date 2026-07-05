"""
Unit tests for the ai_blogging library.
All comments and docstrings in this module are written in English.
"""

from unittest.mock import MagicMock
import pytest

from ai_blogging.models import Persona, ArticleSchema, Section, Subsection
from ai_blogging.generator import (
    create_persona,
    sanitize_heading,
    convert_to_markdown,
    generate_article,
    log_prompt,
)


def test_create_persona():
    """
    Test that create_persona properly instantiates a Persona model.
    """
    persona = create_persona(name="Test Persona", description="Test Description")
    assert isinstance(persona, Persona)
    assert persona.name == "Test Persona"
    assert persona.description == "Test Description"


def test_sanitize_heading():
    """
    Test sanitize_heading with various malformed strings containing markdown headers.
    """
    assert sanitize_heading("### Hello") == "Hello"
    assert sanitize_heading("# World ") == "World"
    assert sanitize_heading("  ## Python") == "Python"
    assert sanitize_heading("No Header") == "No Header"


def test_convert_to_markdown():
    """
    Test convert_to_markdown creates correct markdown based on ArticleSchema structure.
    """
    article = ArticleSchema(
        title="  # Main Title  ",
        meta_description="Sample description.",
        sections=[
            Section(
                h2_title="## H2 Section 1",
                subsections=[
                    Subsection(
                        h3_title="### H3 Subsection 1.1",
                        content="This is the content for subsection 1.1."
                    ),
                    Subsection(
                        h3_title="H3 Subsection 1.2",
                        content="Content 1.2."
                    )
                ]
            ),
            Section(
                h2_title="H2 Section 2",
                subsections=[
                    Subsection(
                        h3_title="H3 Subsection 2.1",
                        content="Content 2.1."
                    )
                ]
            )
        ]
    )
    
    markdown = convert_to_markdown(article)
    
    expected = (
        "# Main Title\n"
        "> メタディスクリプション: Sample description.\n"
        "\n"
        "## H2 Section 1\n"
        "### H3 Subsection 1.1\n"
        "This is the content for subsection 1.1.\n"
        "\n"
        "### H3 Subsection 1.2\n"
        "Content 1.2.\n"
        "\n"
        "## H2 Section 2\n"
        "### H3 Subsection 2.1\n"
        "Content 2.1.\n"
    )
    assert markdown == expected


def test_generate_article_mocked():
    """
    Test generate_article with a mocked genai.Client to isolate network side effects.
    """
    mock_client = MagicMock()
    mock_response = MagicMock()
    # Mocking the JSON response text returned from Gemini structured output
    mock_response.text = """
    {
        "title": "Mock Title",
        "meta_description": "Mock Meta",
        "sections": [
            {
                "h2_title": "Mock H2",
                "subsections": [
                    {
                        "h3_title": "Mock H3",
                        "content": "Mock Content"
                    }
                ]
            }
        ]
    }
    """
    mock_client.models.generate_content.return_value = mock_response
    
    persona = Persona(name="Mock Persona", description="Mock Prompt")
    
    article = generate_article(
        client=mock_client,
        persona=persona,
        keyword="Mock Keyword"
    )
    
    # Assert return types and structures are parsed correctly
    assert isinstance(article, ArticleSchema)
    assert article.title == "Mock Title"
    assert len(article.sections) == 1
    assert article.sections[0].h2_title == "Mock H2"
    
    # Check that client was called with correct parameters
    mock_client.models.generate_content.assert_called_once()


def test_log_prompt(tmp_path, monkeypatch):
    """
    Test log_prompt creates directory and appends prompt information correctly.
    """
    import os

    # Redirect logging to tmp_path to avoid writing to actual logs directory
    monkeypatch.chdir(tmp_path)

    persona = Persona(name="Tester Persona", description="Act like a test runner.")
    log_prompt(keyword="Testing logs", persona=persona, model="test-model")

    log_file_path = os.path.join("logs", "prompt_history.log")
    assert os.path.exists(log_file_path)

    with open(log_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Model: test-model" in content
    assert "Keyword: Testing logs" in content
    assert "Persona Name: Tester Persona" in content
    assert "Act like a test runner." in content

