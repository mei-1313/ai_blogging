"""
Example usage of the ai_blogging library.
All comments and docstrings in this module are written in English.
"""

import os
from ai_blogging import create_client, create_persona, generate_article, convert_to_markdown

def main():
    # Load environment variables from .env if present
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    parts = line.strip().split("=", 1)
                    if len(parts) == 2:
                        os.environ[parts[0].strip()] = parts[1].strip().strip("'\"")

    # 1. Initialize Gemini API Client
    # Ensure GEMINI_API_KEY environment variable is set.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[WARNING] GEMINI_API_KEY environment variable is not set.")
        print("Please set it to generate real articles. Running mockup test run instead.\n")
        
    # 2. Define the persona (Immutable model)
    # The persona dictates the AI's role and writing rules.
    persona = create_persona(
        name="Tech Instructor Mirai",
        description=(
            "You are a friendly and structured technical instructor. "
            "Explain concepts clearly, use bold formatting for key terms, "
            "and write in a polite teaching tone (Japanese). "
            "Ensure sections strictly follow H2 (##) and H3 (###) structure."
        )
    )
    
    # 3. Generate article (Side effect)
    if api_key:
        client = create_client(api_key=api_key)
        try:
            print("Generating article using Gemini API with gemini-3.1-flash-lite...")
            article_data = generate_article(
                client=client,
                persona=persona,
                keyword="Python Functional Programming Benefits",
                model="gemini-3.1-flash-lite"
            )
            
            # 4. Serialize to Markdown (Pure function)
            markdown_article = convert_to_markdown(article_data)
            print("\n--- Generated Markdown Article ---\n")
            print(markdown_article)
            
            # Save to a file
            output_file = "generated_article.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown_article)
            print(f"Article saved to {output_file}")
            
        except Exception as e:
            print(f"Error generating article: {e}")
    else:
        # Dry-run with mock data to showcase the serialization
        from ai_blogging.models import ArticleSchema, Section, Subsection
        print("--- Dry Run (Serialization Test) ---")
        mock_article = ArticleSchema(
            title="Introduction to Functional Programming in Python",
            meta_description="Learn how to write cleaner, more maintainable code using functional concepts in Python.",
            sections=[
                Section(
                    h2_title="What is Functional Programming?",
                    subsections=[
                        Subsection(
                            h3_title="Core Concepts",
                            content="Functional programming (FP) is a paradigm that treats computation as the evaluation of mathematical functions and avoids changing-state and mutable data."
                        ),
                        Subsection(
                            h3_title="Pure Functions",
                            content="A **pure function** is a function where the return value is solely determined by its input values, without observable side effects."
                        )
                    ]
                )
            ]
        )
        
        markdown_article = convert_to_markdown(mock_article)
        print(markdown_article)


if __name__ == "__main__":
    main()
