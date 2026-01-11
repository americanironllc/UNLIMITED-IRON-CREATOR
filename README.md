# UNLIMITED IRON CREATOR 🚀

## AN UNLIMITED AI MULTIMEDIA GENERATOR. No Limits.

A powerful, flexible AI multimedia generation framework that enables you to create text, images, audio, and video content without artificial limitations. Built with Python, this tool provides a unified interface for generating any type of media content using AI.

---

## ⚡ One-Click Deployment

Deploy this application to Google Cloud Run with a single click - no setup required!

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/americanironllc/UNLIMITED-IRON-CREATOR.git)

**What happens when you click:**
1. Opens Google Cloud Shell with this repository
2. Automatically builds the Docker container
3. Deploys to Cloud Run with optimized settings (2GB RAM, 2 CPUs)
4. Provides you with a live URL in ~3-5 minutes
5. App is fully functional immediately - API keys are optional and can be added later

**Requirements:**
- A Google Cloud account (free tier available)
- Billing enabled (you get $300 in free credits for new accounts)

**Cost:** Most usage falls within the [free tier](https://cloud.google.com/run/pricing). Typical cost: $0-5/month for light usage.

📚 **Detailed Guides:**
- [ONE-CLICK-DEPLOY.md](./ONE-CLICK-DEPLOY.md) - Complete deployment walkthrough
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Manual deployment & advanced configuration
- [DEPLOYMENT-CHECKLIST.md](./DEPLOYMENT-CHECKLIST.md) - Technical verification checklist

---

## 🌟 Features

### Unlimited Media Generation
- **📝 Text Generation**: Create stories, articles, scripts, and any text content
- **🖼️ Image Generation**: Generate images from text descriptions
- **🔊 Audio Generation**: Create speech, music, and sound effects
- **🎬 Video Generation**: Generate video content from prompts
- **🎯 Multimedia Projects**: Combine all media types into cohesive projects

### No Limits Philosophy
- **Flexible Configuration**: Customize every aspect of generation
- **Multiple AI Backends**: Support for various AI APIs and services
- **Extensible Architecture**: Easy to add new generation capabilities
- **Batch Processing**: Generate multiple assets simultaneously
- **Quality Controls**: Fine-tune output quality and style

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/americaniron/UNLIMITED-IRON-CREATOR.git
cd UNLIMITED-IRON-CREATOR

# Install dependencies (optional, based on your needs)
pip install -r requirements.txt

# Make the script executable
chmod +x multimedia_generator.py
```

### Basic Usage

#### Generate Text
```bash
python multimedia_generator.py text "Write a story about space exploration"
```

#### Generate Image
```bash
python multimedia_generator.py image "A futuristic cityscape at sunset" --size 1920x1080
```

#### Generate Audio
```bash
python multimedia_generator.py audio "Calm meditation music" --type music --duration 60
```

#### Generate Video
```bash
python multimedia_generator.py video "A time-lapse of clouds moving" --duration 10 --resolution 1920x1080
```

#### Generate Complete Multimedia Project
```bash
python multimedia_generator.py project --config project_example.json
```

### Web Interface

The easiest way to use UNLIMITED IRON CREATOR is through the Streamlit web interface:

```bash
# Local installation
streamlit run streamlit_app.py
```

Or use the **one-click Cloud Run deployment** button above for instant cloud hosting!

## 📖 Documentation

### Command-Line Interface

```
usage: multimedia_generator.py [-h] [--config CONFIG] [--output-dir OUTPUT_DIR]
                              [--style STYLE] [--type TYPE] [--duration DURATION]
                              [--size SIZE] [--format FORMAT]
                              {text,image,audio,video,project} [prompt]

UNLIMITED IRON CREATOR - AI Multimedia Generator

positional arguments:
  {text,image,audio,video,project}
                        Type of content to generate
  prompt                Generation prompt

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Path to configuration file
  --output-dir OUTPUT_DIR
                        Output directory for generated files
  --style STYLE         Generation style
  --type TYPE           Audio type (speech/music/sound_effect) or video type
  --duration DURATION   Duration in seconds (for audio/video)
  --size SIZE           Size/resolution (e.g., 1024x1024)
  --format FORMAT       Output format
```

### Configuration

Create a configuration file (e.g., `config.json`) to customize defaults:

```json
{
  "output_dir": "generated_media",
  "default_format": "png",
  "quality": "high",
  "enable_text": true,
  "enable_image": true,
  "enable_audio": true,
  "enable_video": true,
  "defaults": {
    "text": {
      "max_length": 500,
      "temperature": 0.7,
      "style": "creative"
    },
    "image": {
      "size": "1024x1024",
      "style": "realistic"
    },
    "audio": {
      "voice": "neutral",
      "type": "speech",
      "format": "mp3"
    },
    "video": {
      "resolution": "1920x1080",
      "fps": 30,
      "duration": 5
    }
  }
}
```

See `config.example.json` for a complete configuration template.

### Python API

You can also use the generator programmatically:

```python
from multimedia_generator import UnlimitedMultimediaGenerator

# Initialize generator
generator = UnlimitedMultimediaGenerator(config_path='config.json')

# Generate text
text = generator.generate_text("Write a poem about nature")

# Generate image
image_path = generator.generate_image("A serene mountain landscape", 
                                      size="1920x1080", 
                                      style="photorealistic")

# Generate audio
audio_path = generator.generate_audio("Epic cinematic soundtrack",
                                      type="music",
                                      duration=60)

# Generate video
video_path = generator.generate_video("Northern lights dancing in the sky",
                                      duration=15,
                                      resolution="1920x1080",
                                      fps=60)

# Generate complete project
results = generator.generate_multimedia_project({
    'text': 'Write about the future of AI',
    'image': 'Futuristic AI cityscape',
    'audio': 'Inspiring background music',
    'video': 'AI visualization'
})
```

## 🎨 Examples

### Example 1: Generate a Story with Illustration
```bash
python multimedia_generator.py text "A short story about a time-traveling scientist" --style narrative
python multimedia_generator.py image "A scientist in a time machine surrounded by swirling energy" --style cinematic
```

### Example 2: Create a Video with Soundtrack
```bash
python multimedia_generator.py video "A journey through space" --duration 20 --style cinematic
python multimedia_generator.py audio "Epic space exploration music" --type music --duration 20
```

### Example 3: Complete Multimedia Project
Use the provided `project_example.json` template to generate a complete project:
```bash
python multimedia_generator.py project --config project_example.json
```

## 🔧 Advanced Features

### Media Types & Parameters

#### Text Generation
- `max_length`: Maximum length of generated text
- `temperature`: Creativity level (0.0-1.0)
- `style`: creative, formal, technical, narrative, etc.

#### Image Generation
- `size`: Image dimensions (e.g., "1024x1024", "1920x1080")
- `style`: realistic, abstract, cartoon, photorealistic, etc.
- `format`: png, jpg, webp, etc.

#### Audio Generation
- `type`: speech, music, sound_effect
- `voice`: neutral, energetic, calm, etc. (for speech)
- `duration`: Length in seconds
- `format`: mp3, wav, ogg, etc.

#### Video Generation
- `resolution`: Video dimensions (e.g., "1920x1080", "3840x2160")
- `fps`: Frames per second (24, 30, 60, etc.)
- `duration`: Length in seconds
- `style`: realistic, abstract, cinematic, etc.

## 🚀 Cloud Deployment

### One-Click Deployment to Google Cloud Run

The fastest way to get UNLIMITED IRON CREATOR running in the cloud:

1. **Click the Deploy Button** at the top of this README
2. **Sign in** to Google Cloud (or create a free account)
3. **Wait 3-5 minutes** for automatic deployment
4. **Access your app** at the provided Cloud Run URL
5. **Optional:** Add API keys later via Google Cloud Console → Secret Manager

**What's Included:**
- ✅ Fully configured Streamlit web interface
- ✅ Optimized Cloud Run settings (2GB RAM, 2 CPUs, auto-scaling)
- ✅ HTTPS endpoint with Google's security
- ✅ Automatic builds and deployments
- ✅ Health checks and monitoring
- ✅ 99.95% uptime SLA

**Post-Deployment (Optional):**
To enable real AI generation, add your API keys:
1. Go to [Google Cloud Secret Manager](https://console.cloud.google.com/security/secret-manager)
2. Create secrets for your API keys (e.g., `openai-api-key`, `elevenlabs-api-key`)
3. Update your Cloud Run service to mount these secrets as environment variables

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions and configuration options.

### Alternative Deployment Methods

**Manual Cloud Run Deployment:**
```bash
gcloud run deploy unlimited-iron-creator \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

**Docker Deployment:**
```bash
docker build -t unlimited-iron-creator .
docker run -p 8080:8080 unlimited-iron-creator
```

**Other Platforms:**
- **Heroku:** Use the included Dockerfile
- **AWS ECS/Fargate:** Deploy the Docker container
- **Azure Container Instances:** Use the Dockerfile
- **Kubernetes:** Use the included `service.yaml` as a starting point

## 🎯 Use Cases

- **Content Creation**: Generate blog posts, social media content, marketing materials
- **Storytelling**: Create illustrated stories with narration and music
- **Education**: Generate educational videos and presentations
- **Art Projects**: Create unique multimedia art installations
- **Prototyping**: Quickly prototype video/audio content ideas
- **Game Development**: Generate assets for games
- **Marketing**: Create ad campaigns with multiple media types

## 🔌 Extending the Generator

The framework is designed to be extensible. To integrate with real AI services:

1. **Add API Integration**: Update the generation methods to call actual AI APIs
2. **Install Additional Libraries**: Uncomment needed dependencies in `requirements.txt`
3. **Add API Keys**: Store API keys in your config file or environment variables
4. **Implement Custom Generators**: Subclass `UnlimitedMultimediaGenerator` to add new capabilities

### Supported AI Services (when configured)

- **Text**: OpenAI GPT, Anthropic Claude, Google PaLM, local LLMs
- **Image**: DALL-E, Midjourney, Stable Diffusion, Adobe Firefly
- **Audio**: ElevenLabs, Google TTS, Azure Speech, MusicGen
- **Video**: Runway, Pika, Stable Video Diffusion, Synthesia

## 🛠️ Development

### Project Structure
```
UNLIMITED-IRON-CREATOR/
├── multimedia_generator.py    # Main generator script
├── requirements.txt           # Python dependencies
├── config.example.json       # Example configuration
├── project_example.json      # Example project config
├── README.md                 # This file
└── generated_media/          # Output directory (created automatically)
```

### Running Tests

```bash
# Test text generation
python multimedia_generator.py text "Test prompt" --output-dir test_output

# Test all media types
python multimedia_generator.py project --config project_example.json
```

## 📝 License

This project is open source and available for unlimited use and modification.

## 🤝 Contributing

Contributions are welcome! This is an unlimited creativity tool, so feel free to:
- Add new media generation capabilities
- Integrate additional AI services
- Improve the CLI interface
- Add new features and functionality
- Improve documentation

## 🌐 Support

For issues, questions, or feature requests, please open an issue on GitHub.

## ⚡ Performance Tips

- Use batch processing for multiple assets
- Configure output directories to organize content
- Adjust quality settings based on your needs
- Cache frequently used prompts
- Use appropriate resolution/duration for your use case

## 🎉 Credits

Created with the goal of removing artificial limitations from AI content generation.

---

**Remember: The only limit is your imagination!** 🚀✨