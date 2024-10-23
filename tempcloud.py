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

# Global variable to hold preloaded video data
video_cache = {}

# Function to fetch videos by tag from Cloudinary
def fetch_videos_by_tags(tags):
    categorized_videos = {}
    try:
        for tag in tags:
            response = cloudinary.api.resources_by_tag(
                tag=tag,
                resource_type="video",  
                max_results=10  # Adjust this limit as needed
            )

            # Extract video URLs and generate thumbnails
            video_urls = [
                {
                    'video_url': resource['secure_url'],
                    'thumbnail_url': cloudinary.CloudinaryImage(resource['public_id']).build_url(
                        resource_type="video", format="jpg", transformation=[{'start_offset': '2', 'width': 300, 'height': 200, 'crop': 'fill'}]
                    )
                }
                for resource in response.get('resources', [])
            ]

            if video_urls:
                categorized_videos[tag] = video_urls

        return categorized_videos
    except Exception as e:
        print(f"Error: {str(e)}")
        return {}

# Function to preload videos at server startup
def preload_videos():
    global video_cache
    tags = ['ads', 'text', 'image', 'banner']  # Modify this list as needed
    video_cache = fetch_videos_by_tags(tags)
    print("Videos preloaded successfully.")

# Route to fetch categorized videos
@app.route('/get_videos', methods=['GET'])
def get_videos():
    return jsonify(video_cache)

# Route to serve the main page with video templates
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the edit template page
@app.route('/edit_template')
def edit_template():
    return render_template('edit_template.html')
# Route to manually refresh cached videos
@app.route('/refresh_cache', methods=['POST'])
def refresh_cache():
    preload_videos()  # Reload video data from Cloudinary
    return jsonify({"message": "Cache refreshed successfully"}), 200


if __name__ == '__main__':
    preload_videos()  # Preload videos before starting the server
    port = int(os.environ.get('PORT', 5000))  # Get port from environment, default to 5000
    app.run(host='0.0.0.0', port=port)
