from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_super_segura' # Necessário para usar sessões

# Lista simples para simular um banco de dados
posts = [
    {
        'id': 1,
        'titulo': 'Primeiro Post',
        'conteudo': 'Este é o conteúdo do primeiro post do nosso blog!',
        'autor': 'Admin'
    },
    {
        'id': 2,
        'titulo': 'Segundo Post',
        'conteudo': 'Olá mundo! Este é o segundo post.',
        'autor': 'Admin'
    }
]
next_post_id = 3

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html', posts=posts)

# Rota para ver um post individual
@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    return "Post não encontrado", 404

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'vibewill' and request.form['password'] == 'Guns@123':
            session['logged_in'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# Rota para a área de administração (somente para quem está logado)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    global next_post_id

    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        posts.append({'id': next_post_id, 'titulo': titulo, 'conteudo': conteudo, 'autor': 'Admin'})
        next_post_id += 1
        return redirect(url_for('admin'))

    return render_template('admin.html', posts=posts)

# Rota para deletar um post
@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    global posts
    posts = [p for p in posts if p['id'] != post_id]
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)