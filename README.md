# AI Blogging (`ai_blogging`)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](#english) | [日本語](#日本語)

---

## English

An elegant Python library leveraging the Gemini API to automatically generate highly structured, high-quality blog articles in Markdown format without structure breakage.

### Features
* **Functional Programming (FP) Approach**: Separation of pure logic (Markdown rendering, sanitization) from side effects (API calls, logging). Designed around immutable data models and data transformation.
* **Structured Output Enforcement**: Leverages the Gemini API's schema enforcement to guarantee nested article layouts (H2 sections with child H3 subsections).
* **Robust Markdown Serialization**: Automatically converts structured data into a standard Markdown post, preventing broken formatting and header nesting issues.
* **Prompt Logging**: Automatically records every generation prompt configuration to a local log file, keeping track of history.
* **Global Standard Codebase**: All source code comments and docstrings are written in English.

### Requirements
* Python 3.9 or higher
* A Gemini API Key (accessible via the `GEMINI_API_KEY` environment variable or `.env` file)

### Installation

1. Clone the repository and navigate into the project directory:
   ```bash
   git clone <repository-url>
   cd ai_blogging
   ```

2. Create a virtual environment and install the package:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

### Quick Start

1. Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY="your-actual-api-key-here"
   ```

2. Run the example usage script:
   ```bash
   PYTHONPATH=. .venv/bin/python example.py
   ```

3. Read the generated article in `generated_article.md` and check prompt parameters in `logs/prompt_history.log`.

### API Usage Example

```python
import os
from ai_blogging import create_client, create_persona, generate_article, convert_to_markdown

# 1. Initialize Gemini Client
client = create_client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Define the immutable Persona
persona = create_persona(
    name="Tech Instructor",
    description="Explain concepts clearly in Japanese, using bold tags and polite tones."
)

# 3. Generate article (Side effect)
article_data = generate_article(
    client=client,
    persona=persona,
    keyword="Python Programming benefits",
    model="gemini-3.1-flash-lite"
)

# 4. Serialize to Markdown (Pure function)
markdown_text = convert_to_markdown(article_data)
print(markdown_text)
```

### Running Tests

Execute pytest in the virtual environment:
```bash
PYTHONPATH=. pytest
```

---

## 日本語

Gemini APIを活用し、構造崩れのない高品質なブログ記事（Markdown形式）を自動生成するための堅牢なPythonライブラリです。

### 機能・特徴
* **関数型プログラミング（FP）アプローチ**: 純粋なロジック（Markdown変換やサニタイズ）と副作用（API通信やロギング）を分離。イミュータブルなデータ構造とデータの変換処理を軸に設計されています。
* **スキーマによる構造崩れ防止**: Gemini APIの「構造化出力機能」を活用し、大見出し（H2）とその配下の小見出し（H3）の階層構造をシステム的に保証します。
* **Markdown自動コンバーター**: 生成された構造化データを即座にブログ投稿可能な美しいMarkdown文字列へ自動的にシリアライズ。
* **プロンプト記録システム**: AIに送信されたすべてのキーワードやペルソナ指定を自動的に `logs/prompt_history.log` にログとして記録します。
* **グローバル仕様のコードベース**: ソースコード内のコメントやdocstringはすべて英語で記述されています。

### 動作環境
* Python 3.9 以上
* Gemini APIキー（環境変数 `GEMINI_API_KEY` または `.env` ファイルに設定）

### インストール方法

1. リポジトリをクローンしてディレクトリへ移動します:
   ```bash
   git clone <repository-url>
   cd ai_blogging
   ```

2. 仮想環境を作成してライブラリをインストールします:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

### クイックスタート

1. プロジェクトのルートディレクトリに `.env` ファイルを作成します:
   ```env
   GEMINI_API_KEY="実際のAPIキーをここに記述"
   ```

2. サンプルプログラムを実行します:
   ```bash
   PYTHONPATH=. .venv/bin/python example.py
   ```

3. 生成されたブログ記事が `generated_article.md` に保存され、プロンプトの送信内容が `logs/prompt_history.log` に追記されます。

### 基本的なコード例

```python
import os
from ai_blogging import create_client, create_persona, generate_article, convert_to_markdown

# 1. クライアントの作成
client = create_client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. イミュータブルなペルソナの作成
persona = create_persona(
    name="Tech Instructor",
    description="技術的なコンセプトを、太字を交えて日本語で分かりやすく説明してください。"
)

# 3. 記事データの自動生成（副作用）
article_data = generate_article(
    client=client,
    persona=persona,
    keyword="Python プログラミングのメリット",
    model="gemini-3.1-flash-lite"
)

# 4. Markdownへのシリアライズ（純粋関数）
markdown_text = convert_to_markdown(article_data)
print(markdown_text)
```

### テストの実行

仮想環境で以下のコマンドを実行し、ユニットテストを実行できます:
```bash
PYTHONPATH=. pytest
```

---

## License / ライセンス

This project is licensed under the MIT License. See the [LICENSE](file:///home/mirai/work/ai_blogging/LICENSE) file for details.
