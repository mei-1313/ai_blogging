"""
AI Blogging assistant library using Gemini API with functional programming approach.
All comments and docstrings in this module are written in English.
"""

from ai_blogging.models import Persona, ArticleSchema, Section, Subsection
from ai_blogging.generator import (
    create_client,
    create_persona,
    generate_article,
    convert_to_markdown,
)

__all__ = [
    "Persona",
    "ArticleSchema",
    "Section",
    "Subsection",
    "create_client",
    "create_persona",
    "generate_article",
    "convert_to_markdown",
]
