from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
CONTENT_DIR = 'content'

# Ensure content directory exists
if not os.path.exists(CONTENT_DIR):
    os.makedirs(CONTENT_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes', methods=['GET'])
def list_notes():
    try:
        files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
        files.sort()
        return jsonify({"notes": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/notes/<filename>', methods=['GET'])
def get_note(filename):
    if not filename.endswith('.md'):
        filename += '.md'
    filepath = os.path.join(CONTENT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"filename": filename, "content": content})
    else:
        return jsonify({"error": "Note not found"}), 404

@app.route('/api/notes/<filename>', methods=['POST'])
def save_note(filename):
    if not filename.endswith('.md'):
        filename += '.md'
    filepath = os.path.join(CONTENT_DIR, filename)
    data = request.json
    content = data.get('content', '')

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({"success": True, "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
