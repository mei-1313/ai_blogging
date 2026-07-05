"""
Data structures and models for the AI blogging assistant.
All comments and docstrings in this module are written in English.
"""

from typing import List
from pydantic import BaseModel, Field


class Persona(BaseModel):
    """
    Immutable model representing the persona of the AI blog writer.
    Used to guide the AI's tone, style, and rules.
    """
    name: str = Field(..., description="The unique name or identifier of the persona.")
    description: str = Field(
        ...,
        description="Detailed instructions describing the persona's expertise, style, tone, and rules."
    )


class Subsection(BaseModel):
    """
    Represents a subsection of the article, which corresponds to H3 in Markdown.
    """
    h3_title: str = Field(
        ...,
        description="The subsection title (H3). Do NOT include Markdown symbols like '###' or '#'."
    )
    content: str = Field(
        ...,
        description=(
            "The body text for this subsection. Should contain appropriate line breaks, "
            "bold highlights, bullet points, etc. using standard markdown formatting. "
            "Do NOT include heading markdown markers like '##' or '###'."
        )
    )


class Section(BaseModel):
    """
    Represents a section of the article, which corresponds to H2 in Markdown.
    Each section can have one or more subsections.
    """
    h2_title: str = Field(
        ...,
        description="The section title (H2). Do NOT include Markdown symbols like '##' or '#'."
    )
    subsections: List[Subsection] = Field(
        ...,
        description="List of subsections (H3 and content) belonging to this H2 section."
    )


class ArticleSchema(BaseModel):
    """
    The structured layout of the generated article.
    Passed as the response schema to the Gemini API to prevent structure breaking.
    """
    title: str = Field(
        ...,
        description="The overall main title of the article. Do NOT include markdown header markers like '#'."
    )
    meta_description: str = Field(
        ...,
        description="A search meta description summarizing the article."
    )
    sections: List[Section] = Field(
        ...,
        description="The structural content list of H2 sections in the article."
    )
