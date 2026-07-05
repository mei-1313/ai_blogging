"""
Generator functions for compiling keyword and persona instructions into a Markdown article.
Features functional design where pure logic is separated from side effects (API calls).
All comments and docstrings in this module are written in English.
"""

from google import genai
from google.genai import types
from ai_blogging.models import Persona, ArticleSchema


def create_client(api_key: str | None = None) -> genai.Client:
    """
    Creates and returns a Gemini API client instance.
    This is an initialization step that sets up the connection interface.
    """
    return genai.Client(api_key=api_key)


def create_persona(name: str, description: str) -> Persona:
    """
    Pure function to create a Persona data model.
    """
    return Persona(name=name, description=description)


import datetime
import os

def log_prompt(keyword: str, persona: Persona, model: str) -> None:
    """
    Side-effect function to log the prompt request to a file.
    Creates a 'logs' directory if it doesn't exist and appends log details.
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "prompt_history.log")
    
    timestamp = datetime.datetime.now().isoformat()
    log_entry = (
        f"=== Generation Request [{timestamp}] ===\n"
        f"Model: {model}\n"
        f"Keyword: {keyword}\n"
        f"Persona Name: {persona.name}\n"
        f"Persona Description:\n{persona.description}\n"
        f"=========================================\n\n"
    )
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)


def generate_article(
    client: genai.Client,
    persona: Persona,
    keyword: str,
    model: str = "gemini-2.5-flash"
) -> ArticleSchema:
    """
    Sends a request to the Gemini API to generate structured article data.
    This function contains side-effects (Network API call and local logging).
    """
    # Log the prompt inputs before generating
    log_prompt(keyword=keyword, persona=persona, model=model)
    
    prompt = f"Please write a high-quality blog article based on the keyword: '{keyword}'"
    
    # Set the persona's description as system instruction,
    # and enforce structured output mapping to ArticleSchema.
    config = types.GenerateContentConfig(
        system_instruction=persona.description,
        response_mime_type="application/json",
        response_schema=ArticleSchema,
        temperature=0.7,
    )
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    
    if not response.text:
        raise ValueError("Received empty response from the Gemini API.")
        
    return ArticleSchema.model_validate_json(response.text)


import re

def sanitize_heading(text: str) -> str:
    """
    Pure function to remove leading markdown heading characters (#) and strip surrounding whitespace.
    This acts as a guard against the AI accidentally generating heading markdown inside schema fields.
    """
    # Remove leading/trailing spaces, then remove any leading hash characters followed by spaces.
    return re.sub(r'^#+\s*', '', text.strip())



def convert_to_markdown(article: ArticleSchema) -> str:
    """
    Pure function to serialize ArticleSchema into a structured markdown string.
    Guarantees structural integrity based on the following template:
    
    # [Main Title]
    > メタディスクリプション: [Meta Description]
    
    ## [H2 Section Title]
    ### [H3 Subsection Title]
    [Content]
    """
    lines = []
    lines.append(f"# {sanitize_heading(article.title)}")
    lines.append(f"> メタディスクリプション: {article.meta_description.strip()}")
    lines.append("")
    
    for section in article.sections:
        lines.append(f"## {sanitize_heading(section.h2_title)}")
        for sub in section.subsections:
            lines.append(f"### {sanitize_heading(sub.h3_title)}")
            lines.append(sub.content.strip())
            lines.append("")  # Blank line after each H3 content
            
    # Combine lines and return normalized string (ending in a single newline)
    return "\n".join(lines).rstrip() + "\n"
