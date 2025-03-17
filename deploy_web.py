#!/usr/bin/env python3
"""
Deployment script for Snakepit game.
This script packages the game for web deployment using Pygbag.
"""

import subprocess
import sys
import webbrowser
import time
import shutil
from pathlib import Path

def check_pygbag():
    """Check if pygbag is installed, install if not."""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "show", "pygbag"],
            stdout=subprocess.DEVNULL
        )
        print("✓ Pygbag is already installed")
        return True
    except subprocess.CalledProcessError:
        print("Pygbag not found. Installing...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "pygbag"]
            )
            print("✓ Pygbag installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Pygbag. Please install manually with:")
            print("   pip install pygbag")
            return False


def deploy_game():
    """Deploy the game using pygbag."""
    print("\n🚀 Deploying Snakepit to web...\n")
    
    # Create the build directory if it doesn't exist
    build_dir = Path("build/web")
    build_dir.parent.mkdir(exist_ok=True)
    build_dir.mkdir(exist_ok=True)
    
    # Run pygbag with auto-start configuration
    print("Starting pygbag build process...")
    process = subprocess.Popen(
        [
            sys.executable, 
            "-m", 
            "pygbag", 
            "--build",
            "--ume_block", "0",  # Disable user media engagement block
            "--can_close", "1",  # Allow closing the game
            "main.py"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Set a timeout (in seconds)
    timeout = 300  # 5 minutes
    start_time = time.time()
    
    # Poll the process until it completes or times out
    while process.poll() is None:
        if time.time() - start_time > timeout:
            process.terminate()
            print("❌ Build process timed out after 5 minutes.")
            return False
        
        # Sleep to avoid high CPU usage
        time.sleep(1)
        print(".", end="", flush=True)
    
    # Check if the build was successful
    if process.returncode == 0:
        print("\n\n✓ Build completed successfully!")
        
        # Check if the necessary files exist
        if (build_dir / "index.html").exists():
            print("✓ Web files generated successfully")
            
            # Also copy files to docs directory for GitHub Pages
            docs_dir = Path("docs")
            docs_dir.mkdir(exist_ok=True)
            
            print("\nCopying files to docs directory for GitHub Pages...")
            for file in build_dir.glob("*"):
                dest_file = docs_dir / file.name
                shutil.copy2(file, dest_file)
            print("✓ Files copied to docs directory")
            
            # Show deployment instructions
            print("\n📋 Free Hosting Options:")
            print("\n1. GitHub Pages (Recommended):")
            print("   - Push your code to GitHub")
            print("   - Go to repository Settings → Pages")
            print("   - Set source to 'Deploy from a branch'")
            print("   - Select 'main' branch and '/docs' folder")
            print("   - Your game will be at: https://[username].github.io/[repo]")
            
            print("\n2. Netlify Drop (Easiest):")
            print("   - Go to app.netlify.com/drop")
            print("   - Drag and drop the build/web or docs directory")
            
            print("\nAll options provide:")
            print("✓ HTTPS security")
            print("✓ Global CDN for fast loading")
            
            return True
        else:
            print("❌ Build completed but web files were not generated.")
            return False
    else:
        print("\n❌ Build failed with error code:", process.returncode)
        print("Error output:", process.stderr.read())
        return False


if __name__ == "__main__":
    if check_pygbag():
        deploy_game() 