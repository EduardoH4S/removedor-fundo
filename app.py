from flask import Flask, request, render_template, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return 'Nenhum arquivo enviado', 400
    
    file = request.files['image']
    if file.filename == '':
        return 'Nenhum arquivo selecionado', 400

    # Ler a imagem
    img = Image.open(file.stream)
    
    # Remover fundo
    output = remove(img)
    
    # Salvar em um buffer
    img_byte_arr = io.BytesIO()
    output.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
