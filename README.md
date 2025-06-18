# AI-Powered Discussion Board for BYU Analytics

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Framework Flask](https://img.shields.io/badge/Framework-Flask-blue.svg)](https://flask.palletsprojects.com/)

This project is a fully functional web application designed to serve as an AI-powered discussion board for an R-based analytics class. The primary goal is to facilitate quick debugging and active learning by providing students with an immediate, AI-generated response to their coding questions and errors.

---

### Key Features

*   **AI-Powered Answers:** Students can submit questions (including R code and error messages) and receive a detailed, helpful answer generated in real-time by the Google Gemini API.
*   **Rich Content Display:** AI responses are rendered from Markdown to formatted HTML, including syntax highlighting for R code blocks, making answers easy to read and understand.
*   **Dynamic & Responsive UI:**
    *   A modern three-column layout with a fixed navigation sidebar and independently scrollable content and details columns.
*   **Topic-Based Navigation:** Users can filter the post list by topic ("General", "Lectures", "Projects"). The active topic is highlighted, and the view header updates dynamically to provide user context.
*   **Full-Text Search:** A search bar allows users to filter posts by keywords in the title or question body.
*   **Comprehensive Admin Controls:**
    *   **Pin Post:** Pin important posts to the top of the feed for visibility.
    *   **Mark as Resolved:** Visually mark posts as resolved, giving students clear signals on what issues are closed.
    *   **Delete Post:** Remove irrelevant or duplicate posts from the board.
*   **Interactive Voting:** Asynchronous upvote/downvote system that updates counts instantly without a page reload, providing a smooth user experience.

---

### Tech Stack

*   **Backend:** Python 3, Flask
*   **Frontend:** HTML5, CSS3 (Bootstrap 5), JavaScript (ES6)
*   **Database:** SQLite 3
*   **AI:** Google Gemini API (`gemini-1.5-flash-latest`)
*   **Frontend Libraries:**
    *   `Marked.js` (Markdown Parsing)
    *   `DOMPurify` (HTML Sanitization for Security)
    *   `highlight.js` (Code Syntax Highlighting)

---

### Local Setup & Running the Application

To run this project locally, please follow these steps.

**Prerequisites:**
*   Python 3.8+
*   Git

**Instructions:**

1.  **Clone the repository:**
    ```bash
    git clone [Your GitHub Repository URL]
    cd byu-discussion-board 
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the environment file:**
    Create a file named `.env` in the root of the project directory. Add your Google Gemini API key to this file:
    ```
    GEMINI_API_KEY='YOUR_API_KEY_HERE'
    ```

5.  **Initialize the database (THIS FILE SHOULD ALREADY BE IN THE REPO.):**
    This script creates the `discussion.db` file and can be run to add columns if the schema changes.
    ```bash
    python migrate_db.py 
    ```
    *(Note: If you are starting fresh, run `python create_db.py` if that script is available.)*

6.  **Run the Flask application:**
    ```bash
    flask run
    ```

7.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

---

