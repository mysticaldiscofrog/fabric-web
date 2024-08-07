import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Wisdom Extractor</title>
</head>
<body>
    <h1>Enter YouTube URL</h1>
    <form method="POST">
        <input type="text" name="url" size="50" placeholder="https://youtube.com/watch?v=..."><br>
        <input type="submit" value="Extract Wisdom">
    </form>
    <p>{{ message }}</p>
    <pre>{{ fabric_output }}</pre>
</body>
</html>
'''

def process_youtube_url(url):
    try:
        yt_command = f"fabric yt --transcript {url}"
        wisdom_command = "fabric --stream --pattern extract_wisdom"
        
        print(f"Executing YT command: {yt_command}")
        yt_result = subprocess.run(yt_command, shell=True, capture_output=True, text=True, check=True)
        print(f"YT command output: {yt_result.stdout}")
        
        print(f"Executing Wisdom command: {wisdom_command}")
        wisdom_result = subprocess.run(wisdom_command, shell=True, capture_output=True, text=True, check=True, input=yt_result.stdout)
        print(f"Wisdom command output: {wisdom_result.stdout}")
        
        return wisdom_result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error processing URL: {e}")
        print(f"Error output: {e.stderr}")
        return f"Error: {e}\n\nStderr: {e.stderr}"

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    fabric_output = ''
    if request.method == 'POST':
        url = request.form['url']
        message = f'Processing URL: {url}'
        fabric_output = process_youtube_url(url)
    return render_template_string(HTML, message=message, fabric_output=fabric_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)