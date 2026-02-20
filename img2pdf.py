from flask import Flask, request, send_file, render_template_string
from PIL import Image
from io import BytesIO

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Image to PDF Converter</title>
<style>
  body { font-family: Arial, sans-serif; background: #f4f6f8; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
  .container { background: white; padding: 30px 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); max-width: 500px; width: 90%; text-align: center; }
  h1 { margin-bottom: 20px; color: #333; }
  input[type=file] { margin: 20px 0; }
  button { background-color: #4CAF50; color: white; border: none; padding: 12px 25px; font-size: 16px; border-radius: 5px; cursor: pointer; }
  button:hover { background-color: #45a049; }
  p { color: #666; font-size: 14px; }
</style>
</head>
<body>
  <div class="container">
    <h1>Image to PDF Converter</h1>
    <p>Upload one or more images (JPG, PNG) to convert into a single PDF.</p>
    <form method="POST" action="/run" enctype="multipart/form-data">
      <input type="file" name="images" accept="image/*" multiple required><br>
      <button type="submit">Convert to PDF</button>
    </form>
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_FORM)

@app.route('/run', methods=['POST'])
def images_to_pdf():
    files = request.files.getlist('images')
    if not files:
        return "No images uploaded", 400

    images = []
    try:
        for file in files:
            img = Image.open(file.stream).convert('RGB')
            images.append(img)
    except Exception as e:
        return f"Error processing images: {e}", 400

    if not images:
        return "No valid images found", 400

    pdf_buffer = BytesIO()
    first_img, *rest_imgs = images
    first_img.save(pdf_buffer, format='PDF', save_all=True, append_images=rest_imgs)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="converted_images.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
