import subprocess
import os
import re
from urllib.parse import urlparse, parse_qs
from flask import Flask, request, render_template_string, url_for

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Create</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50 text-gray-800">
    <div class="container mx-auto p-4">

        <div class="mt-8 bg-white shadow-md rounded-lg p-6 space-y-6">
            <h2 class="text-xl font-bold text-purple-700">Studio Create- Integrating Vision, Technology, and Sustainability</h2>
            <p class="text-gray-700">"Bridging innovation and practicality for a sustainable future"</p>
            <div>
                <h3 class="text-lg font-semibold text-gray-900">About Studio Create:</h3>
                <p class="text-gray-700">Visionary systems integrators, designers, and sustainability advocates. With many diverse background we bring a unique and holistic approach to solving complex challenges.</p>
            </div>
            <div>
                <h3 class="text-lg font-semibold text-gray-900">Our Ethos:</h3>
                <p class="text-gray-700">"Function is beautiful. Sustainability is essential. Knowledge should be accessible to all."</p>
            </div>
            <div>
                <h3 class="text-lg font-semibold text-gray-900">Our Initiatives:</h3>
                <div class="space-y-4">
                    <div>
                        <h4 class="text-md font-semibold text-purple-700">1. cibusaqua.casa: The Global Knowledge Nexus</h4>
                        <p class="text-gray-700">"Cultivating Wisdom, Harvesting Change"</p>
                        <p class="text-gray-700">cibusaqua.casa is a living, breathing ecosystem of global wisdom. Here, knowledge transcends borders, adapting to local needs while addressing universal challenges. Our geo-tagged system ensures that solutions are always culturally relevant and practically applicable. By contributing insights, you're not just sharing information – you're catalyzing change on a global scale.</p>
                        <p class="text-gray-700">"In a world drowning in information, cibusaqua.casa is your lifeline to actionable wisdom."</p>
                    </div>
                    <div>
                        <h4 class="text-md font-semibold text-purple-700">2. Datafied Foresight: Illuminating the Path Ahead</h4>
                        <p class="text-gray-700">"Where Data Whispers, We Listen"</p>
                        <p class="text-gray-700">We translate complexity into clarity, uncertainty into opportunity. By analyzing global trends and their ripple effects, we provide a crystal ball for strategic decision-making. We dive deep into organizational DNA, identifying inefficiencies and untapped potential. With us, you're not just preparing for the future – you're actively shaping it.</p>
                        <p class="text-gray-700">"We don't just predict the future. We help you shape it."</p>
                    </div>
                    <div>
                        <h4 class="text-md font-semibold text-purple-700">3. Digital Fortification: Securing the Unseen Realm</h4>
                        <p class="text-gray-700">"Your Digital Citadel Awaits"</p>
                        <p class="text-gray-700">In today's hyperconnected world, your home network is the new frontier of personal security. We build digital fortresses for those who can't afford to be vulnerable. Our solutions are comprehensive security ecosystems that adapt to your lifestyle, anticipating threats before they materialize.</p>
                        <p class="text-gray-700">"Because in the digital age, your home network is your castle's keep."</p>
                    </div>
                    <div>
                        <h4 class="text-md font-semibold text-purple-700">4. Gaia's Engineers: Crafting Tomorrow's Environment</h4>
                        <p class="text-gray-700">"Breathing Life Back into Mother Earth"</p>
                        <p class="text-gray-700">We're reimagining humanity's relationship with nature. Our environmental systems blend cutting-edge technology with time-tested natural processes to create scalable, sustainable solutions. From carbon sequestration to waste transformation, we're pioneering approaches that actively regenerate our planet.</p>
                        <p class="text-gray-700">"We're not just reducing our footprint. We're leaving a positive imprint."</p>
                    </div>
                    <div>
                        <h4 class="text-md font-semibold text-purple-700">5. Elite Courier: Discretion in Motion</h4>
                        <p class="text-gray-700">"When 'Handle with Care' Isn't Enough"</p>
                        <p class="text-gray-700">Elite Courier is the pinnacle of discrete, high-security logistics. We understand that true luxury lies in flawless execution and ironclad trust. Our team treats each item as if it were the crown jewels, ensuring your most valuable possessions move across the world as if they never left your sight.</p>
                        <p class="text-gray-700">"Because some deliveries are too important for ordinary hands."</p>
                    </div>
                </div>
            </div>
            <div>
                <h3 class="text-lg font-semibold text-gray-900">Our Vision:</h3>
                <p class="text-gray-700">Studio Create's is on a journey to foster a unique perspective on the interconnectedness of our world. We create functional, beautiful solutions that address real-world problems, spanning individual, corporate, and global scales.</p>
                <p class="text-gray-700">We're committed to bridging the gap between visionary concepts and practical implementation, laying the groundwork for meaningful, sustainable change. Join us in creating a future where technology and nature work in harmony, where knowledge is freely accessible, and where sustainability is at the core of every decision.</p>
            </div>
            <div>
                <h3 class="text-lg font-semibold text-gray-900">Connect:</h3>
                <p class="text-gray-700">@destinyisearned</p>
            </div>
        </div>
            <div class="bg-white shadow-md rounded-lg p-6">
                <h1 class="text-2xl font-bold text-purple-700 mb-4">YouTube Wisdom Extractor</h1>
                <form method="POST" class="space-y-4" onsubmit="showLoading()">
                    <div>
                        <label for="url" class="block text-sm font-medium text-gray-700">Enter YouTube URL</label>
                        <input type="text" name="url" id="url" class="block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm" placeholder="https://youtube.com/watch?v=...">
                    </div>
                    <div>
                        <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                            Extract Wisdom
                        </button>
                    </div>
                </form>
                <p class="mt-4 text-sm text-gray-600">{{ message }}</p>
                <pre class="mt-2 p-4 bg-gray-100 rounded-lg shadow-inner text-sm text-gray-800 font-mono whitespace-pre-wrap overflow-x-auto break-all max-w-full">{{ fabric_output }}</pre>
            </div>
        </div>
    </div>
</body>
</html>
'''

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':  # Shortened URL
        return parsed_url.path[1:]  # The ID is in the path, strip leading '/'
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    return None

def process_youtube_url(url):
    try:
        proxies = {
            "http": "http://gw.dataimpulse.com:823",
            "https": "http://gw.dataimpulse.com:823",
        }
        os.environ['HTTP_PROXY'] = proxies['http']
        os.environ['HTTPS_PROXY'] = proxies['https']

        yt_command = f"yt --transcript {url}"
        wisdom_command = "fabric --stream --pattern extract_wisdom"
        
        yt_result = subprocess.run(yt_command, shell=True, capture_output=True, text=True, check=True)
        wisdom_result = subprocess.run(wisdom_command, shell=True, capture_output=True, text=True, check=True, input=yt_result.stdout)
        
        video_id = extract_video_id(url)
        if video_id:
            filename = f"{video_id}.txt"
            filepath = os.path.join(os.getcwd(), filename)
            with open(filepath, 'w') as file:
                file.write(wisdom_result.stdout)
            return wisdom_result.stdout + f"\n\nOutput also saved to: {filepath}"
        else:
            return "Error: Could not extract video ID from the URL"
        
    except subprocess.CalledProcessError as e:
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
