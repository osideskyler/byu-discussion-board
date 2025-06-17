from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_all_posts, add_post, search_posts, upvote_post, downvote_post, toggle_post_pin, toggle_post_resolved, delete_post
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env file.")
    else:
        genai.configure(api_key=api_key)
        print("Gemini API configured successfully.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

@app.route('/')
def index():
    posts = get_all_posts()
    return render_template('index.html', posts=posts)

# THIS IS THE ROUTE THAT WAS MISSING
@app.route('/add_post', methods=['POST'])
def add_post_route():
    # 1. Get data from the form
    title = request.form['title']
    topic = request.form['topic']
    question_body = request.form['question_body']
    
    ai_response_text = "Sorry, the AI assistant could not generate a response at this time."
    
    try:
        # 2. Initialize the Gemini Model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # 3. Create the prompt for the AI
        prompt = f"""
        You are a friendly and helpful AI teaching assistant for a BYU data analytics class that uses R. 
        A student has a question. Your task is to provide a clear, helpful, and accurate answer.
        Structure your response in the following way:
        1.  Start with a friendly, encouraging opening.
        2.  Directly address the student's question or explain the error.
        3.  If code is involved, provide a corrected R code snippet inside a markdown block (```r ... ```).
        4.  Explain *why* the correction works.

        Here is the student's question:
        ---
        Title: {title}
        Question: {question_body}
        ---
        """
        
        # 4. Generate the response from Gemini
        print("--- Sending prompt to Gemini API... ---")
        response = model.generate_content(prompt)
        ai_response_text = response.text
        print("--- Received response from Gemini. ---")

    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        
    # 5. Save to the database
    add_post(title=title, question_body=question_body, ai_response=ai_response_text, topic=topic)
    
    # 6. Redirect to the homepage
    return redirect(url_for('index'))

# THIS IS THE NEW SEARCH ROUTE
@app.route('/search')
def search():
    # Get the search term from the URL (e.g., /search?query=...)
    query = request.args.get('query')
    
    # If there's no query, just redirect to the homepage
    if not query:
        return redirect(url_for('index'))
    
    # Use our new database function to find matching posts
    posts = search_posts(query)
    
    # Render the SAME index.html template, but pass it the filtered posts
    # and the search query itself (so we can display it in the search box)
    return render_template('index.html', posts=posts, search_query=query)


# This is a small but important fix. The url_for needs to know the function name.
# Our form was looking for `add_post`, but our function is named `add_post_route`.
# We will fix this in the HTML.
# But for now, add this to app.py
app.add_url_rule('/add_post', 'add_post', add_post_route, methods=['POST'])

# NEW VOTE ROUTES
@app.route('/vote/up/<int:post_id>', methods=['POST'])
def upvote_route(post_id):
    new_counts = upvote_post(post_id)
    # Return the new counts as JSON so our JavaScript can read it
    return jsonify({'upvotes': new_counts['upvotes'], 'downvotes': new_counts['downvotes'], 'status': 'success'})

@app.route('/vote/down/<int:post_id>', methods=['POST'])
def downvote_route(post_id):
    new_counts = downvote_post(post_id)
    return jsonify({'upvotes': new_counts['upvotes'], 'downvotes': new_counts['downvotes'], 'status': 'success'})

@app.route('/pin/<int:post_id>', methods=['POST'])
def pin_route(post_id):
    new_status = toggle_post_pin(post_id)
    return jsonify({'status': 'success', 'is_pinned': new_status})

@app.route('/resolve/<int:post_id>', methods=['POST'])
def resolve_route(post_id):
    new_status = toggle_post_resolved(post_id)
    return jsonify({'status': 'success', 'is_resolved': new_status})

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_route(post_id):
    delete_post(post_id)
    # Note: In a real app, add a confirmation step ("Are you sure?").
    return jsonify({'status': 'success', 'message': 'Post deleted'})

if __name__ == '__main__':
    app.run(debug=True)