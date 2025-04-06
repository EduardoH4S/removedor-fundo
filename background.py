import io
import base64
from rembg import remove
from PIL import Image
from flask import Flask, request, jsonify, render_template, send_file

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400
    
    file = request.files['image']
    img = Image.open(file.stream)
    
    # Remover fundo
    output = remove(img)
    
    # Salvar em buffer de memória
    img_byte_arr = io.BytesIO()
    output.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Retornar a imagem processada
    return send_file(img_byte_arr, mimetype='image/png', 
                    download_name='background_removed.png')

@app.route('/api/remove-bg', methods=['POST'])
def api_remove_bg():
    try:
        # Obter dados JSON
        data = request.json
        
        if 'image' not in data:
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400
        
        # Decodificar a imagem base64
        img_data = base64.b64decode(data['image'].split(',')[1])
        img = Image.open(io.BytesIO(img_data))
        
        # Remover fundo
        output = remove(img)
        
        # Converter de volta para base64
        buffered = io.BytesIO()
        output.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_str}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
