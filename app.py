from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Configuração do diretório de upload e categorias
UPLOAD_FOLDER = 'uploads'
CATEGORIES = ['CIs', 'Calendario Academico', 'Eventos']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cria as subpastas de categorias
for category in CATEGORIES:
    os.makedirs(os.path.join(UPLOAD_FOLDER, category), exist_ok=True)

@app.route('/')
def index():
    files_by_category = {}
    for category in CATEGORIES:
        category_path = os.path.join(app.config['UPLOAD_FOLDER'], category)
        files = os.listdir(category_path)
        files_by_category[category] = files
    return render_template('index.html', files_by_category=files_by_category)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file_handler():  # Renomeada para evitar conflito
    if request.method == 'POST':
        category = request.form.get('category')
        file = request.files['file']
        if file and category in CATEGORIES:
            category_path = os.path.join(app.config['UPLOAD_FOLDER'], category)
            filepath = os.path.join(category_path, file.filename)
            file.save(filepath)
            return redirect(url_for('index'))
    return render_template('upload.html', categories=CATEGORIES)

@app.route('/uploads/<category>/<filename>')
def uploaded_file(category, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], category), filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
@app.route('/')
def index():
    files_by_category = {}
    for category in CATEGORIES:
        category_path = os.path.join(app.config['UPLOAD_FOLDER'], category)
        # Certifique-se de que a pasta existe e lista os arquivos
        if os.path.exists(category_path):
            files = os.listdir(category_path)
        else:
            files = []
        files_by_category[category] = files
    return render_template('index.html', files_by_category=files_by_category)
