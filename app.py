import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Wisdom Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #FFFFF0; /* Ivory */
            color: #2A132A; /* Darker Purple */
            margin: 0;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #4A234A; /* Base Purple */
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #E6E6FA; /* Pale Lilac */
            border: 1px solid #4A234A; /* Base Purple */
            border-radius: 8px;
        }
        .form-container {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #36454F; /* Charcoal */
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #4A234A; /* Base Purple */
            color: #FFFFF0; /* Ivory */
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #2A132A; /* Darker Purple */
        }
        .copy-section {
            margin-bottom: 20px;
        }
        .copy-section h2 {
            margin-top: 0;
        }
        .message, .output {
            white-space: pre-wrap;
            background-color: #FFFFF0; /* Ivory */
            padding: 10px;
            border-radius: 4px;
            border: 1px solid #4A234A; /* Base Purple */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>YouTube Wisdom Extractor</h1>
        <div class="form-container">
            <form method="POST">
                <input type="text" name="url" size="50" placeholder="https://youtube.com/watch?v=..."><br>
                <input type="submit" value="Extract Wisdom">
            </form>
            <p class="message">{{ message }}</p>
            <pre class="output">{{ fabric_output }}</pre>
        </div>
        <div class="copy-section">
            <h2>Destiny Is Earned - Integrating Vision, Technology, and Sustainability</h2>
            <p>"Bridging innovation and practicality for a sustainable future"</p>
            <h3>About [Your Name]:</h3>
            <p>A visionary systems integrator, designer, and sustainability advocate. With a diverse background spanning construction, design, and data science, [Your Name] brings a unique, holistic approach to solving complex challenges.</p>
            <h3>Our Ethos:</h3>
            <p>"Function is beautiful. Sustainability is essential. Knowledge should be accessible to all."</p>
            <h3>Our Initiatives:</h3>
            <h4>1. cibusaqua.casa: The Global Knowledge Nexus</h4>
            <p>"Cultivating Wisdom, Harvesting Change"</p>
            <p>cibusaqua.casa is a living, breathing ecosystem of global wisdom. Here, knowledge transcends borders, adapting to local needs while addressing universal challenges. Our geo-tagged system ensures that solutions are always culturally relevant and practically applicable. By contributing insights, you're not just sharing information – you're catalyzing change on a global scale.</p>
            <p>"In a world drowning in information, cibusaqua.casa is your lifeline to actionable wisdom."</p>
            <h4>2. Datafied Foresight: Illuminating the Path Ahead</h4>
            <p>"Where Data Whispers, We Listen"</p>
            <p>We translate complexity into clarity, uncertainty into opportunity. By analyzing global trends and their ripple effects, we provide a crystal ball for strategic decision-making. We dive deep into organizational DNA, identifying inefficiencies and untapped potential. With us, you're not just preparing for the future – you're actively shaping it.</p>
            <p>"We don't just predict the future. We help you shape it."</p>
            <h4>3. Digital Fortification: Securing the Unseen Realm</h4>
            <p>"Your Digital Citadel Awaits"</p>
            <p>In today's hyperconnected world, your home network is the new frontier of personal security. We build digital fortresses for those who can't afford to be vulnerable. Our solutions are comprehensive security ecosystems that adapt to your lifestyle, anticipating threats before they materialize.</p>
            <p>"Because in the digital age, your home network is your castle's keep."</p>
            <h4>4. Gaia's Engineers: Crafting Tomorrow's Environment</h4>
            <p>"Breathing Life Back into Mother Earth"</p>
            <p>We're reimagining humanity's relationship with nature. Our environmental systems blend cutting-edge technology with time-tested natural processes to create scalable, sustainable solutions. From carbon sequestration to waste transformation, we're pioneering approaches that actively regenerate our planet.</p>
            <p>"We're not just reducing our footprint. We're leaving a positive imprint."</p>
            <h4>5. Elite Courier: Discretion in Motion</h4>
            <p>"When 'Handle with Care' Isn't Enough"</p>
            <p>Elite Courier is the pinnacle of discrete, high-security logistics. We understand that true luxury lies in flawless execution and ironclad trust. Our team treats each item as if it were the crown jewels, ensuring your most valuable possessions move across the world as if they never left your sight.</p>
            <p>"Because some deliveries are too important for ordinary hands."</p>
            <h3>Our Vision:</h3>
            <p>[Your Name]'s journey from builder to systems integrator has fostered a unique perspective on the interconnectedness of our world. We create functional, beautiful solutions that address real-world problems, spanning individual, corporate, and global scales.</p>
            <p>We're committed to bridging the gap between visionary concepts and practical implementation, laying the groundwork for meaningful, sustainable change. Join us in creating a future where technology and nature work in harmony, where knowledge is freely accessible, and where sustainability is at the core of every decision.</p>
            <h3>Connect:</h3>
            <p>[Your contact information]</p>
        </div>
    </div>
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
