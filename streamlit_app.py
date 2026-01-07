#!/usr/bin/env python3
"""
UNLIMITED IRON CREATOR - Streamlit Web Interface
A comprehensive web interface for AI multimedia generation
"""

import streamlit as st
import json
import os
from datetime import datetime
from multimedia_generator import UnlimitedMultimediaGenerator

# Page configuration
st.set_page_config(
    page_title="UNLIMITED IRON CREATOR",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = UnlimitedMultimediaGenerator()
    st.session_state.history = []
    st.session_state.output_dir = 'generated_media'

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-top: 10px;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 UNLIMITED IRON CREATOR</h1>
    <h3>AI Multimedia Generator - No Limits</h3>
    <p>Generate text, images, audio, and video with AI - An extensible framework for unlimited creativity</p>
</div>
""", unsafe_allow_html=True)

# Quick Start Guide
with st.expander("📖 Quick Start Guide"):
    st.markdown("""
    ### Welcome to UNLIMITED IRON CREATOR!
    
    This is a comprehensive multimedia generation framework that can integrate with various AI APIs:
    
    **Features:**
    - 📝 **Text Generation**: Create stories, articles, scripts, and more
    - 🖼️ **Image Generation**: Generate images from text descriptions
    - 🔊 **Audio Generation**: Create speech, music, and sound effects
    - 🎬 **Video Generation**: Generate video content from prompts
    - 🎯 **Project Mode**: Generate all media types at once
    - 📊 **History**: Track and revisit your generations
    
    **How to use:**
    1. Select a tab for the type of content you want to generate
    2. Enter your prompt and adjust parameters
    3. Click the Generate button
    4. View and download your generated content
    
    **Note**: This is an extensible framework. Generated files include metadata showing what would be created when connected to real AI APIs (GPT, DALL-E, Stable Diffusion, ElevenLabs, etc.)
    """)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Output directory configuration
    output_dir = st.text_input(
        "Output Directory",
        value=st.session_state.output_dir,
        help="Directory where generated files will be saved"
    )
    
    if output_dir != st.session_state.output_dir:
        st.session_state.output_dir = output_dir
        st.session_state.generator.output_dir = output_dir
        st.session_state.generator._ensure_output_dir()
    
    st.divider()
    
    # Default quality settings
    st.subheader("Default Quality Settings")
    default_quality = st.select_slider(
        "Quality Level",
        options=["Low", "Medium", "High", "Ultra"],
        value="High",
        help="Default quality for generated content"
    )
    
    st.divider()
    
    # About section
    st.subheader("ℹ️ About")
    st.markdown("""
    **UNLIMITED IRON CREATOR**
    
    Version: 1.0.0
    
    An extensible AI multimedia generation framework.
    
    [📚 Documentation](https://github.com/americaniron/UNLIMITED-IRON-CREATOR)
    
    [💻 GitHub Repository](https://github.com/americaniron/UNLIMITED-IRON-CREATOR)
    """)
    
    st.divider()
    
    # Statistics
    if st.session_state.history:
        st.subheader("📊 Statistics")
        total_gens = len(st.session_state.history)
        st.metric("Total Generations", total_gens)
        
        # Count by type
        type_counts = {}
        for item in st.session_state.history:
            media_type = item.get('type', 'unknown')
            type_counts[media_type] = type_counts.get(media_type, 0) + 1
        
        for media_type, count in type_counts.items():
            st.metric(f"{media_type.capitalize()}", count)

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Text Generation",
    "🖼️ Image Generation", 
    "🔊 Audio Generation",
    "🎬 Video Generation",
    "🎯 Project Mode",
    "📊 History"
])

# ============================================================================
# TAB 1: TEXT GENERATION
# ============================================================================
with tab1:
    st.header("📝 Text Generation")
    st.markdown("Generate creative text content with AI")
    
    with st.form("text_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            text_prompt = st.text_area(
                "Enter your prompt",
                height=100,
                placeholder="Write a short story about a time-traveling scientist...",
                help="Describe what you want the AI to write"
            )
        
        with col2:
            text_style = st.selectbox(
                "Style",
                options=["creative", "formal", "technical", "narrative", "professional", "inspirational"],
                help="Writing style for the generated text"
            )
            
            text_max_length = st.slider(
                "Max Length",
                min_value=100,
                max_value=2000,
                value=500,
                step=100,
                help="Maximum length of generated text"
            )
            
            text_temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher = more creative, Lower = more focused"
            )
        
        submitted_text = st.form_submit_button("🚀 Generate Text", use_container_width=True)
    
    if submitted_text:
        if not text_prompt:
            st.error("❌ Please enter a prompt")
        else:
            with st.spinner("Generating text..."):
                try:
                    result = st.session_state.generator.generate_text(
                        text_prompt,
                        max_length=text_max_length,
                        temperature=text_temperature,
                        style=text_style
                    )
                    
                    st.success("✅ Text generated successfully!")
                    
                    # Display generated text
                    st.subheader("Generated Text:")
                    generated_display = st.text_area(
                        "Result (editable)",
                        value=result,
                        height=300,
                        label_visibility="collapsed"
                    )
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Text",
                        data=generated_display,
                        file_name=f"text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    
                    # Add to history
                    st.session_state.history.append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'text',
                        'prompt': text_prompt,
                        'status': 'success',
                        'params': {
                            'style': text_style,
                            'max_length': text_max_length,
                            'temperature': text_temperature
                        }
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Example prompts
    with st.expander("💡 Example Prompts"):
        st.markdown("""
        - "Write a short story about a time-traveling scientist"
        - "Create a professional product description for a smart watch"
        - "Generate a motivational speech about creativity"
        - "Write a technical explanation of quantum computing"
        - "Compose a formal business proposal for a new software product"
        - "Create an inspirational message about overcoming challenges"
        """)

# ============================================================================
# TAB 2: IMAGE GENERATION
# ============================================================================
with tab2:
    st.header("🖼️ Image Generation")
    st.markdown("Generate images from text descriptions")
    
    with st.form("image_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            image_prompt = st.text_area(
                "Image Description",
                height=100,
                placeholder="A futuristic cityscape at sunset with flying cars...",
                help="Describe the image you want to generate"
            )
        
        with col2:
            image_size = st.selectbox(
                "Size",
                options=["512x512", "1024x1024", "1920x1080", "2048x2048"],
                index=1,
                help="Image dimensions"
            )
            
            image_style = st.selectbox(
                "Style",
                options=["realistic", "abstract", "cartoon", "photorealistic", "cinematic", "artistic"],
                help="Visual style for the image"
            )
            
            image_format = st.selectbox(
                "Format",
                options=["png", "jpg", "webp"],
                help="Output image format"
            )
        
        submitted_image = st.form_submit_button("🚀 Generate Image", use_container_width=True)
    
    if submitted_image:
        if not image_prompt:
            st.error("❌ Please enter an image description")
        else:
            with st.spinner("Generating image..."):
                try:
                    result = st.session_state.generator.generate_image(
                        image_prompt,
                        size=image_size,
                        style=image_style,
                        format=image_format
                    )
                    
                    st.success("✅ Image generation initiated successfully!")
                    
                    # Display metadata
                    st.subheader("📋 Generation Details:")
                    metadata_file = f"{result}.json"
                    if os.path.exists(metadata_file):
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Size", metadata.get('size', 'N/A'))
                        with col2:
                            st.metric("Style", metadata.get('style', 'N/A'))
                        with col3:
                            st.metric("Format", metadata.get('format', 'N/A'))
                        
                        st.info(f"📁 File path: `{result}`")
                        
                        with st.expander("View Full Metadata"):
                            st.json(metadata)
                    
                    # Add to history
                    st.session_state.history.append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'image',
                        'prompt': image_prompt,
                        'status': 'success',
                        'file_path': result,
                        'params': {
                            'size': image_size,
                            'style': image_style,
                            'format': image_format
                        }
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Example prompts
    with st.expander("💡 Example Prompts"):
        st.markdown("""
        - "A futuristic cityscape at sunset with flying cars"
        - "Abstract representation of AI and human creativity merging"
        - "Photorealistic portrait of a cyberpunk character"
        - "Serene mountain landscape with a crystal clear lake"
        - "Artistic interpretation of music and colors flowing together"
        - "Cinematic shot of a spaceship approaching a distant planet"
        """)

# ============================================================================
# TAB 3: AUDIO GENERATION
# ============================================================================
with tab3:
    st.header("🔊 Audio Generation")
    st.markdown("Generate speech, music, and sound effects")
    
    with st.form("audio_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            audio_prompt = st.text_area(
                "Audio Description",
                height=100,
                placeholder="Epic cinematic orchestral music...",
                help="Describe the audio you want to generate"
            )
        
        with col2:
            audio_type = st.radio(
                "Type",
                options=["speech", "music", "sound_effect"],
                help="Type of audio to generate"
            )
            
            audio_voice = st.selectbox(
                "Voice/Style",
                options=["neutral", "energetic", "calm", "dramatic"],
                help="Voice style for speech or mood for music"
            )
            
            audio_duration = st.slider(
                "Duration (seconds)",
                min_value=5,
                max_value=120,
                value=30,
                help="Length of the audio"
            )
            
            audio_format = st.selectbox(
                "Format",
                options=["mp3", "wav", "ogg"],
                help="Output audio format"
            )
        
        submitted_audio = st.form_submit_button("🚀 Generate Audio", use_container_width=True)
    
    if submitted_audio:
        if not audio_prompt:
            st.error("❌ Please enter an audio description")
        else:
            with st.spinner("Generating audio..."):
                try:
                    result = st.session_state.generator.generate_audio(
                        audio_prompt,
                        type=audio_type,
                        voice=audio_voice,
                        duration=audio_duration,
                        format=audio_format
                    )
                    
                    st.success("✅ Audio generation initiated successfully!")
                    
                    # Display metadata
                    st.subheader("📋 Generation Details:")
                    metadata_file = f"{result}.json"
                    if os.path.exists(metadata_file):
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Type", metadata.get('type', 'N/A'))
                        with col2:
                            st.metric("Voice/Style", metadata.get('voice', 'N/A'))
                        with col3:
                            st.metric("Duration", f"{metadata.get('duration', 'N/A')}s")
                        with col4:
                            st.metric("Format", metadata.get('format', 'N/A'))
                        
                        st.info(f"📁 File path: `{result}`")
                        
                        with st.expander("View Full Metadata"):
                            st.json(metadata)
                    
                    # Add to history
                    st.session_state.history.append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'audio',
                        'prompt': audio_prompt,
                        'status': 'success',
                        'file_path': result,
                        'params': {
                            'type': audio_type,
                            'voice': audio_voice,
                            'duration': audio_duration,
                            'format': audio_format
                        }
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Example prompts
    with st.expander("💡 Example Prompts"):
        st.markdown("""
        - "Epic cinematic orchestral music"
        - "Calm meditation background soundscape"
        - "Energetic motivational speech"
        - "Upbeat electronic dance music"
        - "Nature sounds with birds and flowing water"
        - "Dramatic trailer voiceover"
        """)

# ============================================================================
# TAB 4: VIDEO GENERATION
# ============================================================================
with tab4:
    st.header("🎬 Video Generation")
    st.markdown("Generate video content from text descriptions")
    
    with st.form("video_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            video_prompt = st.text_area(
                "Video Description",
                height=100,
                placeholder="Time-lapse of clouds moving across a mountain landscape...",
                help="Describe the video you want to generate"
            )
        
        with col2:
            video_resolution = st.selectbox(
                "Resolution",
                options=["1280x720", "1920x1080", "2560x1440", "3840x2160"],
                index=1,
                help="Video resolution"
            )
            
            video_fps = st.select_slider(
                "FPS",
                options=[24, 30, 60],
                value=30,
                help="Frames per second"
            )
            
            video_duration = st.slider(
                "Duration (seconds)",
                min_value=5,
                max_value=60,
                value=10,
                help="Length of the video"
            )
            
            video_style = st.selectbox(
                "Style",
                options=["realistic", "abstract", "cinematic", "documentary", "artistic"],
                help="Visual style for the video"
            )
            
            video_format = st.selectbox(
                "Format",
                options=["mp4", "webm", "avi"],
                help="Output video format"
            )
        
        submitted_video = st.form_submit_button("🚀 Generate Video", use_container_width=True)
    
    if submitted_video:
        if not video_prompt:
            st.error("❌ Please enter a video description")
        else:
            with st.spinner("Generating video..."):
                try:
                    result = st.session_state.generator.generate_video(
                        video_prompt,
                        resolution=video_resolution,
                        fps=video_fps,
                        duration=video_duration,
                        style=video_style,
                        format=video_format
                    )
                    
                    st.success("✅ Video generation initiated successfully!")
                    
                    # Display metadata
                    st.subheader("📋 Generation Details:")
                    metadata_file = f"{result}.json"
                    if os.path.exists(metadata_file):
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.metric("Resolution", metadata.get('resolution', 'N/A'))
                        with col2:
                            st.metric("FPS", metadata.get('fps', 'N/A'))
                        with col3:
                            st.metric("Duration", f"{metadata.get('duration', 'N/A')}s")
                        with col4:
                            st.metric("Style", metadata.get('style', 'N/A'))
                        with col5:
                            st.metric("Format", metadata.get('format', 'N/A'))
                        
                        st.info(f"📁 File path: `{result}`")
                        
                        with st.expander("View Full Metadata"):
                            st.json(metadata)
                    
                    # Add to history
                    st.session_state.history.append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'video',
                        'prompt': video_prompt,
                        'status': 'success',
                        'file_path': result,
                        'params': {
                            'resolution': video_resolution,
                            'fps': video_fps,
                            'duration': video_duration,
                            'style': video_style,
                            'format': video_format
                        }
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Example prompts
    with st.expander("💡 Example Prompts"):
        st.markdown("""
        - "Time-lapse of clouds moving across a mountain landscape"
        - "Abstract data visualization with flowing particles"
        - "Journey through space with planets and stars"
        - "Documentary-style footage of a bustling city"
        - "Artistic interpretation of seasons changing"
        - "Cinematic drone shot flying over a forest"
        """)

# ============================================================================
# TAB 5: PROJECT MODE
# ============================================================================
with tab5:
    st.header("🎯 Project Mode")
    st.markdown("Generate multiple media types at once for a complete project")
    
    # Project configuration
    st.subheader("Configure Your Project")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enable_text = st.checkbox("📝 Enable Text Generation", value=True)
        enable_image = st.checkbox("🖼️ Enable Image Generation", value=True)
    
    with col2:
        enable_audio = st.checkbox("🔊 Enable Audio Generation", value=True)
        enable_video = st.checkbox("🎬 Enable Video Generation", value=True)
    
    st.divider()
    
    # Prompts for each enabled type
    prompts = {}
    params = {}
    
    if enable_text:
        with st.expander("📝 Text Generation Settings", expanded=True):
            prompts['text'] = st.text_area(
                "Text Prompt",
                placeholder="Write about the future of AI...",
                key="project_text_prompt"
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                text_style = st.selectbox("Style", ["creative", "formal", "technical", "narrative", "professional", "inspirational"], key="project_text_style")
            with col2:
                text_max_length = st.slider("Max Length", 100, 2000, 500, key="project_text_length")
            with col3:
                text_temperature = st.slider("Temperature", 0.0, 1.0, 0.7, key="project_text_temp")
            
            params['text_params'] = {
                'style': text_style,
                'max_length': text_max_length,
                'temperature': text_temperature
            }
    
    if enable_image:
        with st.expander("🖼️ Image Generation Settings", expanded=True):
            prompts['image'] = st.text_area(
                "Image Prompt",
                placeholder="A futuristic AI visualization...",
                key="project_image_prompt"
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                image_size = st.selectbox("Size", ["512x512", "1024x1024", "1920x1080", "2048x2048"], index=1, key="project_image_size")
            with col2:
                image_style = st.selectbox("Style", ["realistic", "abstract", "cartoon", "photorealistic", "cinematic", "artistic"], key="project_image_style")
            with col3:
                image_format = st.selectbox("Format", ["png", "jpg", "webp"], key="project_image_format")
            
            params['image_params'] = {
                'size': image_size,
                'style': image_style,
                'format': image_format
            }
    
    if enable_audio:
        with st.expander("🔊 Audio Generation Settings", expanded=True):
            prompts['audio'] = st.text_area(
                "Audio Prompt",
                placeholder="Epic background music...",
                key="project_audio_prompt"
            )
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                audio_type = st.radio("Type", ["speech", "music", "sound_effect"], key="project_audio_type")
            with col2:
                audio_voice = st.selectbox("Voice/Style", ["neutral", "energetic", "calm", "dramatic"], key="project_audio_voice")
            with col3:
                audio_duration = st.slider("Duration (s)", 5, 120, 30, key="project_audio_duration")
            with col4:
                audio_format = st.selectbox("Format", ["mp3", "wav", "ogg"], key="project_audio_format")
            
            params['audio_params'] = {
                'type': audio_type,
                'voice': audio_voice,
                'duration': audio_duration,
                'format': audio_format
            }
    
    if enable_video:
        with st.expander("🎬 Video Generation Settings", expanded=True):
            prompts['video'] = st.text_area(
                "Video Prompt",
                placeholder="Journey through digital space...",
                key="project_video_prompt"
            )
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                video_resolution = st.selectbox("Resolution", ["1280x720", "1920x1080", "2560x1440", "3840x2160"], index=1, key="project_video_res")
            with col2:
                video_fps = st.select_slider("FPS", [24, 30, 60], value=30, key="project_video_fps")
            with col3:
                video_duration = st.slider("Duration (s)", 5, 60, 10, key="project_video_duration")
            with col4:
                video_style = st.selectbox("Style", ["realistic", "abstract", "cinematic", "documentary", "artistic"], key="project_video_style")
            with col5:
                video_format = st.selectbox("Format", ["mp4", "webm", "avi"], key="project_video_format")
            
            params['video_params'] = {
                'resolution': video_resolution,
                'fps': video_fps,
                'duration': video_duration,
                'style': video_style,
                'format': video_format
            }
    
    st.divider()
    
    # Configuration save/load
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Save configuration
        if st.button("💾 Save Configuration", use_container_width=True):
            config_data = {
                'prompts': prompts,
                'params': params
            }
            config_json = json.dumps(config_data, indent=2)
            st.download_button(
                label="📥 Download Config JSON",
                data=config_json,
                file_name=f"project_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        # Load configuration
        uploaded_config = st.file_uploader("📤 Load Configuration", type=['json'])
        if uploaded_config is not None:
            try:
                loaded_config = json.load(uploaded_config)
                st.success("✅ Configuration loaded successfully!")
                st.json(loaded_config)
            except Exception as e:
                st.error(f"❌ Error loading config: {str(e)}")
    
    with col3:
        pass
    
    st.divider()
    
    # Generate project button
    if st.button("🚀 Generate Complete Project", type="primary", use_container_width=True):
        if not any([enable_text, enable_image, enable_audio, enable_video]):
            st.error("❌ Please enable at least one media type")
        elif not prompts:
            st.error("❌ Please enter prompts for enabled media types")
        else:
            # Create progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_steps = len(prompts)
            current_step = 0
            
            results = {}
            
            try:
                status_text.text("Starting multimedia project generation...")
                
                if 'text' in prompts and prompts['text']:
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                    status_text.text(f"📝 Generating text content... ({current_step}/{total_steps})")
                    results['text'] = st.session_state.generator.generate_text(
                        prompts['text'],
                        **params.get('text_params', {})
                    )
                
                if 'image' in prompts and prompts['image']:
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                    status_text.text(f"🖼️ Generating image content... ({current_step}/{total_steps})")
                    results['image'] = st.session_state.generator.generate_image(
                        prompts['image'],
                        **params.get('image_params', {})
                    )
                
                if 'audio' in prompts and prompts['audio']:
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                    status_text.text(f"🔊 Generating audio content... ({current_step}/{total_steps})")
                    results['audio'] = st.session_state.generator.generate_audio(
                        prompts['audio'],
                        **params.get('audio_params', {})
                    )
                
                if 'video' in prompts and prompts['video']:
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                    status_text.text(f"🎬 Generating video content... ({current_step}/{total_steps})")
                    results['video'] = st.session_state.generator.generate_video(
                        prompts['video'],
                        **params.get('video_params', {})
                    )
                
                progress_bar.progress(1.0)
                status_text.text("✅ Project generation complete!")
                
                st.success("🎉 Complete multimedia project generated successfully!")
                
                # Display results
                st.subheader("📊 Generation Results")
                
                for media_type, file_path in results.items():
                    with st.expander(f"{media_type.capitalize()} - {file_path}"):
                        if media_type == 'text':
                            if os.path.exists(file_path):
                                with open(file_path, 'r') as f:
                                    st.text_area("Content", f.read(), height=200, key=f"result_{media_type}")
                        else:
                            metadata_file = f"{file_path}.json"
                            if os.path.exists(metadata_file):
                                with open(metadata_file, 'r') as f:
                                    metadata = json.load(f)
                                st.json(metadata)
                
                # Add to history
                st.session_state.history.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'project',
                    'prompt': 'Multimedia Project',
                    'status': 'success',
                    'results': results,
                    'params': params
                })
                
            except Exception as e:
                st.error(f"❌ Error generating project: {str(e)}")
                progress_bar.empty()
                status_text.empty()

# ============================================================================
# TAB 6: HISTORY
# ============================================================================
with tab6:
    st.header("📊 Generation History")
    st.markdown("View and manage your generation history")
    
    if not st.session_state.history:
        st.info("📭 No generation history yet. Start creating content to see it here!")
    else:
        # Filter options
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            filter_type = st.multiselect(
                "Filter by Type",
                options=["text", "image", "audio", "video", "project"],
                default=["text", "image", "audio", "video", "project"]
            )
        
        with col2:
            sort_order = st.radio(
                "Sort Order",
                options=["Newest First", "Oldest First"],
                horizontal=True
            )
        
        with col3:
            if st.button("🗑️ Clear History", type="secondary"):
                st.session_state.history = []
                st.rerun()
        
        st.divider()
        
        # Filter and sort history
        filtered_history = [
            item for item in st.session_state.history
            if item.get('type') in filter_type
        ]
        
        if sort_order == "Oldest First":
            filtered_history = filtered_history
        else:
            filtered_history = list(reversed(filtered_history))
        
        # Display history items
        for idx, item in enumerate(filtered_history):
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 2, 3, 1])
                
                with col1:
                    # Icon based on type
                    icons = {
                        'text': '📝',
                        'image': '🖼️',
                        'audio': '🔊',
                        'video': '🎬',
                        'project': '🎯'
                    }
                    st.markdown(f"### {icons.get(item['type'], '📄')}")
                    st.caption(item['type'].upper())
                
                with col2:
                    timestamp = datetime.fromisoformat(item['timestamp'])
                    st.markdown(f"**{timestamp.strftime('%Y-%m-%d %H:%M:%S')}**")
                    status_emoji = "✅" if item.get('status') == 'success' else "❌"
                    st.caption(f"Status: {status_emoji} {item.get('status', 'unknown')}")
                
                with col3:
                    prompt = item.get('prompt', 'N/A')
                    if len(prompt) > 100:
                        prompt = prompt[:100] + "..."
                    st.markdown(f"**Prompt:** {prompt}")
                    if 'file_path' in item:
                        st.caption(f"📁 {item['file_path']}")
                
                with col4:
                    if st.button("View Details", key=f"view_{idx}"):
                        with st.expander("Details", expanded=True):
                            st.json(item)
                
                st.divider()
        
        # Export history
        st.subheader("💾 Export History")
        history_json = json.dumps(st.session_state.history, indent=2)
        st.download_button(
            label="📥 Download History as JSON",
            data=history_json,
            file_name=f"generation_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #666;'>
    <p><strong>UNLIMITED IRON CREATOR</strong> - AI Multimedia Generator Framework</p>
    <p>Built with ❤️ using Streamlit | No Limits on Creativity 🚀</p>
    <p><em>This is an extensible framework ready to integrate with AI APIs like GPT, DALL-E, Stable Diffusion, ElevenLabs, and more</em></p>
</div>
""", unsafe_allow_html=True)
