#!/usr/bin/env python3
"""
UMAJA Flutter App Structure Validator

This script validates that all required files for the Flutter app are present
and properly structured.
"""

import os
import sys
from pathlib import Path

def check_file_exists(path, description):
    """Check if a file exists and print status."""
    exists = os.path.isfile(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_dir_exists(path, description):
    """Check if a directory exists and print status."""
    exists = os.path.isdir(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def validate_flutter_structure():
    """Validate the Flutter app structure."""
    print("🔍 UMAJA Flutter App Structure Validation")
    print("=" * 60)
    
    base_dir = Path(__file__).parent
    all_checks = []
    
    print("\n📁 Directory Structure:")
    print("-" * 60)
    all_checks.append(check_dir_exists(base_dir / "lib", "Main lib directory"))
    all_checks.append(check_dir_exists(base_dir / "lib/screens", "Screens directory"))
    all_checks.append(check_dir_exists(base_dir / "lib/widgets", "Widgets directory"))
    all_checks.append(check_dir_exists(base_dir / "lib/models", "Models directory"))
    all_checks.append(check_dir_exists(base_dir / "lib/services", "Services directory"))
    all_checks.append(check_dir_exists(base_dir / "test", "Test directory"))
    
    print("\n📄 Core Files:")
    print("-" * 60)
    all_checks.append(check_file_exists(base_dir / "pubspec.yaml", "Package config"))
    all_checks.append(check_file_exists(base_dir / "analysis_options.yaml", "Linting config"))
    all_checks.append(check_file_exists(base_dir / ".metadata", "Flutter metadata"))
    all_checks.append(check_file_exists(base_dir / ".gitignore", "Git ignore"))
    all_checks.append(check_file_exists(base_dir / "README.md", "Main README"))
    all_checks.append(check_file_exists(base_dir / "STRUCTURE.md", "Structure docs"))
    all_checks.append(check_file_exists(base_dir / "QUICKSTART.md", "Quick start guide"))
    
    print("\n🎯 Main Application:")
    print("-" * 60)
    all_checks.append(check_file_exists(base_dir / "lib/main.dart", "App entry point"))
    
    print("\n📱 Screens:")
    print("-" * 60)
    all_checks.append(check_file_exists(base_dir / "lib/screens/home_screen.dart", "Home screen"))
    all_checks.append(check_file_exists(base_dir / "lib/screens/personalities_screen.dart", "Personalities screen"))
    all_checks.append(check_file_exists(base_dir / "lib/screens/settings_screen.dart", "Settings screen"))
    
    print("\n🧩 Widgets:")
    print("-" * 60)
    all_checks.append(check_file_exists(base_dir / "lib/widgets/smile_card.dart", "Smile card widget"))
    all_checks.append(check_file_exists(base_dir / "lib/widgets/personality_card.dart", "Personality card widget"))
    
    print("\n📊 Models:")
    print("-" * 60)
    all_checks.append(check_file_exists(base_dir / "lib/models/personality.dart", "Personality model"))
    all_checks.append(check_file_exists(base_dir / "lib/models/daily_smile.dart", "Daily smile model"))
    
    print("\n🔧 Services:")
    print("-" * 60)
    all_checks.append(check_file_exists(base_dir / "lib/services/content_service.dart", "Content service"))
    
    print("\n🧪 Tests:")
    print("-" * 60)
    all_checks.append(check_file_exists(base_dir / "test/widget_test.dart", "Widget test"))
    
    print("\n" + "=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"✨ Results: {passed}/{total} checks passed ({percentage:.1f}%)")
    
    if passed == total:
        print("🎉 SUCCESS: Flutter app structure is complete!")
        return 0
    else:
        print(f"⚠️  WARNING: {total - passed} file(s) missing")
        return 1

def main():
    """Main entry point."""
    try:
        exit_code = validate_flutter_structure()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Error during validation: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
