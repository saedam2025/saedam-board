from flask import Flask, render_template, request, redirect, url_for
import json
import os
from uuid import uuid4

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_posts(posts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts[::-1])

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        posts = load_posts()
        post = {
            'id': str(uuid4()),
            'title': request.form['title'],
            'content': request.form['content']
        }
        posts.append(post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('write.html')

@app.route('/post/<post_id>')
def post(post_id):
    posts = load_posts()
    for p in posts:
        if p['id'] == post_id:
            return render_template('post.html', post=p)
    return "글을 찾을 수 없습니다.", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
