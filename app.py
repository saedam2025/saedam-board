from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    posts = load_posts()
    posts.reverse()  # 최신 글이 위로
    return render_template('index.html', posts=posts)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d %H:%M')

        new_post = {
            'title': title,
            'author': author,
            'content': content,
            'date': date
        }

        posts = load_posts()
        posts.append(new_post)
        save_posts(posts)
        return redirect('/')
    return render_template('write.html')

@app.route('/post/<int:index>')
def post(index):
    posts = load_posts()
    if 0 <= index < len(posts):
        post = posts[index]
        return render_template('post.html', post=post)
    return '글을 찾을 수 없습니다', 404

# 🔥 반드시 맨 아래!
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
