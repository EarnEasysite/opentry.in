from flask import Flask, jsonify, render_template
import cloudinary
import cloudinary.api
import os
app = Flask(__name__)

# Configure Cloudinary with your credentials
cloudinary.config(
    cloud_name="dwj7tznit",
    api_key="678549699212321",
    api_secret="b0QPfC_oXWUluc6Mt2Y92YzNK6E"
)

# Function to fetch videos by tag from Cloudinary
def fetch_videos_by_tags(tags):
    categorized_videos = {}
    try:
        # Loop through each tag and fetch videos
        for tag in tags:
            response = cloudinary.api.resources_by_tag(
                tag=tag,
                resource_type="video",  # Specify video type
                max_results=10  # Limit number of videos fetched per tag
            )

            # Extract video URLs for this tag
            video_urls = [resource['secure_url'] for resource in response.get('resources', [])]

            # Add videos to the categorized dictionary
            if video_urls:
                categorized_videos[tag] = video_urls

        return categorized_videos

    except Exception as e:
        print(f"Error: {str(e)}")
        return {}

# Route to fetch categorized videos
@app.route('/get_videos', methods=['GET'])
def get_videos():
    # List of tags to categorize videos
    tags = ['ads', 'text', 'image', 'banner']  # Modify this list as needed
    categorized_videos = fetch_videos_by_tags(tags)
    return jsonify(categorized_videos)

# Route to serve the main page with video templates
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the edit template page
@app.route('/edit_template')
def edit_template():
    return render_template('edit_template.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get port from environment, default to 5000
    app.run(host='0.0.0.0', port=port)
