#!/usr/bin/env python3
"""
UMAJA WORLDTOUR - Setup Script
One-command setup for the multimedia system
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}→ {text}{Colors.ENDC}")

def check_python_version():
    """Check if Python version is 3.11+"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print_info(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Python 3.8 or higher required!")
        return False
    
    if version.major == 3 and version.minor < 11:
        print_warning("Python 3.11+ recommended for best performance")
    
    print_success("Python version OK")
    return True

def install_dependencies():
    """Install all required dependencies"""
    print_header("Installing Dependencies")
    
    try:
        print_info("Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                      check=True, capture_output=True)
        print_success("Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directory Structure")
    
    directories = [
        "data",
        "static/audio",
        "static/images",
        "static/videos",
        "static/purchases",
        "static/samples/john_cleese",
        "static/samples/c3po",
        "static/samples/robin_williams",
        "static/css",
        "static/js",
        "templates",
        "api"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print_success(f"Created {dir_path}/")
    
    return True

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    print_header("Setting Up Environment")
    
    if Path(".env").exists():
        print_warning(".env file already exists, skipping")
        return True
    
    if not Path(".env.example").exists():
        print_error(".env.example not found!")
        return False
    
    try:
        import shutil
        shutil.copy(".env.example", ".env")
        print_success("Created .env file")
        print_info("Edit .env to add your API keys")
        return True
    except Exception as e:
        print_error(f"Failed to create .env: {e}")
        return False

def generate_demo_samples(quick=False):
    """Generate demo samples for each personality"""
    print_header("Generating Demo Samples")
    
    if quick:
        print_warning("Quick mode: Skipping demo generation")
        return True
    
    try:
        # Import modules
        sys.path.insert(0, 'src')
        from personality_engine import PersonalityEngine
        from voice_synthesizer import VoiceSynthesizer
        from image_generator import ImageGenerator
        
        personality_engine = PersonalityEngine()
        voice_synthesizer = VoiceSynthesizer()
        image_generator = ImageGenerator()
        
        topics = {
            'john_cleese': 'British tea etiquette',
            'c3po': 'Protocol analysis',
            'robin_williams': 'Stand-up comedy'
        }
        
        for personality, topic in topics.items():
            print_info(f"Generating samples for {personality}...")
            
            # Generate text
            text_result = personality_engine.generate_text(
                topic=topic,
                personality=personality,
                length='short',
                style_intensity=0.8
            )
            
            # Save text
            text_path = Path(f"static/samples/{personality}/{topic.replace(' ', '_')}.txt")
            with open(text_path, 'w') as f:
                f.write(text_result['text'])
            
            # Generate image (quote card)
            quote = text_result['text'][:150] + "..."
            image_result = image_generator.generate_quote_card(
                quote=quote,
                personality=personality
            )
            
            print_success(f"Generated {personality} samples")
        
        print_success("Demo samples generated")
        return True
        
    except Exception as e:
        print_warning(f"Demo generation skipped: {e}")
        print_info("You can generate samples later using the API")
        return True

def test_modules():
    """Test that core modules can be imported"""
    print_header("Testing Core Modules")
    
    modules = [
        'personality_engine',
        'voice_synthesizer',
        'image_generator',
        'video_generator',
        'worldtour_generator',
        'bundle_builder',
        'multimedia_text_seller'
    ]
    
    sys.path.insert(0, 'src')
    
    for module in modules:
        try:
            __import__(module)
            print_success(f"{module} imported OK")
        except Exception as e:
            print_error(f"{module} import failed: {e}")
            return False
    
    return True

def check_optional_dependencies():
    """Check for optional dependencies and report status"""
    print_header("Checking Optional Dependencies")
    
    optional = {
        'elevenlabs': 'ElevenLabs TTS (premium voice synthesis)',
        'diffusers': 'Stable Diffusion (AI image generation)',
        'torch': 'PyTorch (required for AI models)',
        'moviepy': 'MoviePy (video generation)',
        'cv2': 'OpenCV (video processing)'
    }
    
    for module, description in optional.items():
        try:
            if module == 'cv2':
                __import__('cv2')
            else:
                __import__(module)
            print_success(f"{module}: {description}")
        except ImportError:
            print_warning(f"{module} not available: {description}")
    
    print_info("\nNote: Some features require optional dependencies")
    print_info("Install them with: pip install elevenlabs torch diffusers moviepy opencv-python")

def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete! 🎉")
    
    print(f"""
{Colors.OKGREEN}✓ UMAJA Worldtour is ready!{Colors.ENDC}

{Colors.BOLD}Next Steps:{Colors.ENDC}

1. {Colors.OKCYAN}Configure API Keys{Colors.ENDC}
   Edit .env and add your API keys (optional):
   - ELEVENLABS_API_KEY for premium voice synthesis
   - Other API keys as needed

2. {Colors.OKCYAN}Start the Server{Colors.ENDC}
   python api/simple_server.py
   
   Then visit: http://localhost:5000

3. {Colors.OKCYAN}Test the System{Colors.ENDC}
   Visit these pages:
   - http://localhost:5000/ - Landing page
   - http://localhost:5000/worldtour - Interactive map
   - http://localhost:5000/bundle-builder - Create content
   - http://localhost:5000/gallery - View samples

4. {Colors.OKCYAN}Generate Content{Colors.ENDC}
   Use the bundle builder to create your first comedy package!

{Colors.BOLD}Quick Test:{Colors.ENDC}
   python -c "from src.personality_engine import PersonalityEngine; e = PersonalityEngine(); print(e.generate_text('pizza', 'john_cleese', 'short')['text'])"

{Colors.BOLD}Documentation:{Colors.ENDC}
   Check the docs/ folder for detailed guides (coming soon)

{Colors.OKGREEN}Happy creating! 🎭🌍{Colors.ENDC}
""")

def main():
    """Main setup function"""
    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              UMAJA WORLDTOUR - Setup Script                  ║
║                                                              ║
║      Complete Autonomous Multimedia Comedy System           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
""")
    
    # Parse arguments
    quick_mode = '--quick' in sys.argv
    
    if quick_mode:
        print_info("Running in quick mode (skipping demo generation)")
    
    # Run setup steps
    steps = [
        ("Python version check", check_python_version),
        ("Directory creation", create_directories),
        ("Environment setup", create_env_file),
        ("Dependency installation", install_dependencies),
        ("Module testing", test_modules),
        ("Optional dependencies check", check_optional_dependencies),
    ]
    
    if not quick_mode:
        steps.append(("Demo sample generation", lambda: generate_demo_samples(quick_mode)))
    
    failed_steps = []
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print_error(f"{step_name} failed: {e}")
            failed_steps.append(step_name)
    
    if failed_steps:
        print(f"\n{Colors.WARNING}Setup completed with warnings:{Colors.ENDC}")
        for step in failed_steps:
            print(f"  - {step}")
        print(f"\n{Colors.WARNING}Some features may not work correctly{Colors.ENDC}")
    
    print_next_steps()
    
    return 0 if not failed_steps else 1

if __name__ == "__main__":
    sys.exit(main())
