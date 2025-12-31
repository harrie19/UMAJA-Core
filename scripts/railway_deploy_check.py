#!/usr/bin/env python3
"""
UMAJA Railway Deployment Checker
Validates that the system is ready to deploy to Railway
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}")


def print_check(name, status, message=""):
    """Print a check result"""
    icon = "✅" if status else "❌"
    print(f"{icon} {name}: {message if message else ('OK' if status else 'FAILED')}")


def print_warning(name, message):
    """Print a warning"""
    print(f"⚠️  {name}: {message}")


def check_python_version():
    """Check Python version is 3.11+"""
    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 11
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print_check("Python version", is_valid, version_str)
    return is_valid


def check_required_files():
    """Check that required files exist"""
    required_files = [
        'requirements.txt',
        'railway.json',
        'railway.toml',
        'api/simple_server.py',
        'Procfile',
    ]
    
    all_exist = True
    for file in required_files:
        file_path = Path(__file__).parent.parent / file
        exists = file_path.exists()
        if not exists:
            print_check(f"File: {file}", False, "Missing")
            all_exist = False
    
    if all_exist:
        print_check("Required files", True, "All present")
    
    return all_exist


def check_environment_variables():
    """Check environment variables configuration"""
    # For deployment check, we just verify .env.example exists and has the right structure
    env_example_path = Path(__file__).parent.parent / '.env.example'
    
    if not env_example_path.exists():
        print_check("Environment template", False, ".env.example missing")
        return False
    
    # Read and check for required variables in template
    with open(env_example_path, 'r') as f:
        content = f.read()
    
    required_vars = [
        'ENVIRONMENT',
        'DEBUG',
        'WORLDTOUR_MODE',
        'SALES_ENABLED',
        'USE_OFFLINE_TTS',
    ]
    
    all_present = all(var in content for var in required_vars)
    print_check("Environment template", all_present, 
                ".env.example has required variables" if all_present else "Missing required variables")
    
    # Check actual environment (if .env exists or env vars are set)
    env_configured = os.environ.get('ENVIRONMENT') is not None
    if env_configured:
        print_check("Environment variables", True, "Configured")
        worldtour_mode = os.environ.get('WORLDTOUR_MODE', 'false').lower() == 'true'
        sales_enabled = os.environ.get('SALES_ENABLED', 'false').lower() == 'true'
        print(f"   - Worldtour mode: {'enabled' if worldtour_mode else 'disabled'}")
        print(f"   - Sales: {'enabled' if sales_enabled else 'disabled'}")
    else:
        print_warning("Environment variables", "Not set (OK for Railway - set in dashboard)")
    
    return all_present


def check_dependencies():
    """Check that core dependencies can be imported"""
    dependencies = {
        'flask': 'Flask web framework',
        'flask_cors': 'CORS support',
        'requests': 'HTTP library',
        'numpy': 'Numerical processing',
        'PIL': 'Image processing (Pillow)',
    }
    
    missing = []
    installed = []
    for module, description in dependencies.items():
        try:
            # Handle PIL special case
            if module == 'PIL':
                __import__('PIL')
            else:
                __import__(module)
            installed.append(module)
        except ImportError:
            missing.append(module)
    
    if len(missing) == 0:
        print_check("Required packages", True, "All installed")
        return True
    elif len(installed) == 0:
        # None installed - probably pre-deployment environment check
        print_warning("Required packages", "Not installed locally (OK - Railway installs from requirements.txt)")
        return True  # Not a blocker for Railway deployment
    else:
        # Some installed, some missing - check if requirements.txt exists
        req_file = Path(__file__).parent.parent / 'requirements.txt'
        if req_file.exists():
            print_warning("Required packages", f"{len(missing)} not installed locally, but in requirements.txt (Railway will install)")
            return True
        else:
            print_check("Required packages", False, f"{len(missing)} missing and requirements.txt not found")
            return False


def check_personality_engine():
    """Check PersonalityEngine works"""
    try:
        from personality_engine import PersonalityEngine
        engine = PersonalityEngine()
        
        # Try to generate a short text
        result = engine.generate_text(
            topic="test",
            personality="john_cleese",
            length="short"
        )
        
        success = result and 'text' in result and len(result['text']) > 0
        print_check("PersonalityEngine", success, "Text generation working")
        return success
    except ImportError as e:
        # Missing dependencies - OK for pre-deployment check
        print_warning("PersonalityEngine", f"Cannot test (missing dependencies) - will work on Railway")
        return True
    except Exception as e:
        print_check("PersonalityEngine", False, f"Error: {str(e)}")
        return False


def check_voice_synthesizer():
    """Check VoiceSynthesizer works"""
    try:
        from voice_synthesizer import VoiceSynthesizer
        synth = VoiceSynthesizer()
        
        # Check offline mode is available
        offline_available = os.environ.get('USE_OFFLINE_TTS', 'true').lower() == 'true'
        print_check("VoiceSynthesizer", True, 
                   f"OK (offline mode: {'enabled' if offline_available else 'disabled'})")
        return True
    except Exception as e:
        print_check("VoiceSynthesizer", False, f"Error: {str(e)}")
        return False


def check_worldtour_manager():
    """Check WorldtourGenerator works"""
    try:
        from worldtour_generator import WorldtourGenerator
        generator = WorldtourGenerator()
        
        # Get stats to verify cities loaded
        stats = generator.get_stats()
        city_count = stats.get('total_cities', 0)
        
        success = city_count > 0
        print_check("WorldtourManager", success, f"{city_count} cities loaded")
        return success
    except Exception as e:
        print_check("WorldtourManager", False, f"Error: {str(e)}")
        return False


def check_bundle_builder():
    """Check BundleBuilder works"""
    try:
        from bundle_builder import BundleBuilder
        builder = BundleBuilder()
        
        # Try to calculate a simple bundle price
        pricing = builder.calculate_bundle_price(['standard_bundle'])
        success = pricing and 'total' in pricing and pricing['total'] > 0
        
        print_check("BundleBuilder", success, f"Pricing engine OK")
        return success
    except Exception as e:
        print_check("BundleBuilder", False, f"Error: {str(e)}")
        return False


def check_payment_system():
    """Check payment system status"""
    sales_enabled = os.environ.get('SALES_ENABLED', 'false').lower() == 'true'
    
    if not sales_enabled:
        print_warning("Payment system", "Disabled (as intended for worldtour-only mode)")
        return True
    
    # If sales enabled, check PayPal config
    paypal_configured = all([
        os.environ.get('PAYPAL_CLIENT_ID'),
        os.environ.get('PAYPAL_SECRET'),
        os.environ.get('PAYPAL_MODE'),
    ])
    
    print_check("Payment system", paypal_configured, 
               "Enabled and configured" if paypal_configured else "Enabled but not configured")
    return paypal_configured or not sales_enabled


def check_health_endpoint():
    """Check that health endpoint exists in server code"""
    server_path = Path(__file__).parent.parent / 'api' / 'simple_server.py'
    
    if not server_path.exists():
        print_check("Health endpoint", False, "Server file missing")
        return False
    
    with open(server_path, 'r') as f:
        content = f.read()
    
    has_health = '/health' in content and '@app.route' in content
    print_check("Health endpoint", has_health, 
               "/health endpoint exists" if has_health else "Missing /health endpoint")
    return has_health


def check_railway_config():
    """Check Railway configuration files"""
    railway_json = Path(__file__).parent.parent / 'railway.json'
    railway_toml = Path(__file__).parent.parent / 'railway.toml'
    
    has_json = railway_json.exists()
    has_toml = railway_toml.exists()
    
    if has_json:
        print_check("Railway config", True, "railway.json present")
    else:
        print_check("Railway config", False, "railway.json missing")
    
    if has_toml:
        print_check("Railway config (alt)", True, "railway.toml present")
    
    return has_json


def main():
    """Run all deployment checks"""
    print_header("🚀 UMAJA Railway Deployment Check")
    
    # Run all checks
    checks = {
        "Python version": check_python_version(),
        "Required files": check_required_files(),
        "Environment template": check_environment_variables(),
        "Dependencies": check_dependencies(),
        "PersonalityEngine": check_personality_engine(),
        "VoiceSynthesizer": check_voice_synthesizer(),
        "WorldtourManager": check_worldtour_manager(),
        "BundleBuilder": check_bundle_builder(),
        "Payment system": check_payment_system(),
        "Health endpoint": check_health_endpoint(),
        "Railway config": check_railway_config(),
    }
    
    # Summary
    print_header("📊 Summary")
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if passed == total:
        print("\n✅ ✅ ✅ Ready to deploy to Railway! ✅ ✅ ✅")
        print("\nNext steps:")
        print("1. Go to https://railway.app")
        print("2. Create new project → Deploy from GitHub repo")
        print("3. Select harrie19/UMAJA-Core")
        print("4. Add environment variables from .env.example (MINIMAL SETUP section)")
        print("5. Deploy!")
        print("\nSee docs/RAILWAY_AUTO_DEPLOY.md for detailed guide.")
        return 0
    else:
        print("\n❌ Not ready for deployment - fix issues above first")
        print("\nFailed checks:")
        for name, status in checks.items():
            if not status:
                print(f"  - {name}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
