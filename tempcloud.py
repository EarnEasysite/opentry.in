function attachDownloadToButton(videoUrl) {
    const downloadButton = document.getElementById('export-templete');
    if (downloadButton) {
        downloadButton.style.display = 'inline-block';  // Show download button
        downloadButton.href = videoUrl;  // Set the video URL as download link
        downloadButton.download = 'rendered_video.mp4';  // File name for download
    }
}

// Handle the download when the button is clicked
document.getElementById('export-templete').addEventListener('click', function() {
    const videoUrl = document.getElementById('videoPlayer').src;
    if (videoUrl) {
        const a = document.createElement('a');
        a.href = videoUrl;
        a.download = 'rendered_video.mp4';  // Set file name
        document.body.appendChild(a);
        a.click();  // Trigger download
        document.body.removeChild(a);  // Clean up
    }
});

// Open the video URL in a new tab when the button is clicked
function openVideoUrl() {
    if (video_url && video_url.trim() !== "") {
        window.open(video_url, '_blank');
    }
}
