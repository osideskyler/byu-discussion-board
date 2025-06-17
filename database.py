import sqlite3

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect('discussion.db')
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    return conn

def init_db():
    """Initializes the database table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            question_body TEXT NOT NULL,
            ai_response TEXT,
            upvotes INTEGER DEFAULT 0,
            downvotes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            topic TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

def add_sample_data():
    """Adds a few sample posts to the database."""
    conn = get_db_connection()
    post_count = conn.execute('SELECT COUNT(id) FROM posts').fetchone()[0]
    if post_count == 0:
        print("--- Adding sample data to the database. ---")
        posts = [
            (
                'How to filter a data frame in R?',
                'I have a data frame called `df` with a column `age`. I want to keep only the rows where age is greater than 30. How do I do this using dplyr?',
                'Great question! The best way to filter in `dplyr` is using the `filter()` function. You can use the pipe operator `%>%` to make your code more readable. Here is the corrected code:\n\n```r\nlibrary(dplyr)\n\n# Assuming your data frame is named df\nfiltered_df <- df %>% \n  filter(age > 30)\n\nprint(filtered_df)\n```\n\nThis works because the `filter()` function takes a logical condition and returns only the rows where that condition is TRUE.',
                'Lectures'
            ),
            (
                'ggplot error: "Don\'t know how to automatically pick scale"',
                'I am trying to make a scatter plot with ggplot but I keep getting this error. Here is my code: `ggplot(data = my_data, aes(x = weight, y = height)) + geom_point` What did I do wrong?',
                'This is a very common error! It usually happens when you forgot to add the parentheses `()` to the `geom_point` layer. Your code should be:\n\n```r\nlibrary(ggplot2)\n\n# The key is adding () after geom_point\nggplot(data = my_data, aes(x = weight, y = height)) + \n  geom_point()\n```\n\nThe `geom_` functions in ggplot are themselves functions that return a layer object. You need to call them with `()` to add that layer to the plot.',
                'Projects'
            )
        ]
        conn.executemany('INSERT INTO posts (title, question_body, ai_response, topic) VALUES (?, ?, ?, ?)', posts)
        conn.commit()
    conn.close()

def get_all_posts():
    """Fetches all posts, with pinned posts appearing first."""
    conn = get_db_connection()
    # NEW: Order by is_pinned DESC first, then by creation date
    posts = conn.execute('SELECT * FROM posts ORDER BY is_pinned DESC, created_at DESC').fetchall()
    conn.close()
    return posts

def add_post(title, question_body, ai_response, topic):
    """Inserts a new post into the database."""
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, question_body, ai_response, topic) VALUES (?, ?, ?, ?)', (title, question_body, ai_response, topic))
    conn.commit()
    conn.close()

def search_posts(query):
    """Searches for posts, ensuring pinned results are first."""
    conn = get_db_connection()
    search_term = f"%{query}%"
    # NEW: Order by is_pinned DESC first, then by creation date
    posts = conn.execute(
        'SELECT * FROM posts WHERE title LIKE ? OR question_body LIKE ? ORDER BY is_pinned DESC, created_at DESC',
        (search_term, search_term)
    ).fetchall()
    conn.close()
    return posts

def upvote_post(post_id):
    """Increments the upvote count for a specific post."""
    conn = get_db_connection()
    conn.execute('UPDATE posts SET upvotes = upvotes + 1 WHERE id = ?', (post_id,))
    conn.commit()
    # Fetch the new counts to return them
    post = conn.execute('SELECT upvotes, downvotes FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return post

def downvote_post(post_id):
    """Increments the downvote count for a specific post."""
    conn = get_db_connection()
    conn.execute('UPDATE posts SET downvotes = downvotes + 1 WHERE id = ?', (post_id,))
    conn.commit()
    # Fetch the new counts to return them
    post = conn.execute('SELECT upvotes, downvotes FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return post

def toggle_post_pin(post_id):
    """Toggles the is_pinned status of a post."""
    conn = get_db_connection()
    # NOT is_pinned flips the value (0 to 1, 1 to 0)
    conn.execute('UPDATE posts SET is_pinned = NOT is_pinned WHERE id = ?', (post_id,))
    conn.commit()
    new_status = conn.execute('SELECT is_pinned FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return new_status['is_pinned']

def toggle_post_resolved(post_id):
    """Toggles the is_resolved status of a post."""
    conn = get_db_connection()
    conn.execute('UPDATE posts SET is_resolved = NOT is_resolved WHERE id = ?', (post_id,))
    conn.commit()
    new_status = conn.execute('SELECT is_resolved FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return new_status['is_resolved']