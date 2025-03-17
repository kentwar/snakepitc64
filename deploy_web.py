#!/usr/bin/env python3
"""
Deployment script for Snakepit game.
This script packages the game for web deployment using Pygbag.
"""

import os
import subprocess
import sys
import webbrowser
from pathlib import Path

def check_pygbag():
    """Check if pygbag is installed, install if not."""
    try:
        import pygbag
        print("✓ Pygbag is already installed")
        return True
    except ImportError:
        print("Pygbag not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygbag"])
            print("✓ Pygbag installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Pygbag. Please install manually with:")
            print("   pip install pygbag")
            return False

def deploy_game():
    """Deploy the game using pygbag."""
    print("\n🚀 Deploying Snakepit to web...\n")
    
    # Run pygbag on main.py
    result = subprocess.run(
        [sys.executable, "-m", "pygbag", "main.py"], 
        capture_output=True, 
        text=True
    )
    
    # Check if deployment was successful
    if result.returncode == 0:
        # Extract the local URL from the output
        for line in result.stdout.split('\n'):
            if "http://localhost:" in line:
                url = line.strip()
                print(f"\n✓ Deployment successful! Your game is available at: {url}")
                
                # Ask if user wants to open the URL
                open_browser = input("\nOpen in browser? (y/n): ").lower() == 'y'
                if open_browser:
                    webbrowser.open(url)
                
                # Show deployment instructions
                build_path = Path("build/web")
                if build_path.exists():
                    print("\n📋 Free Hosting Options:")
                    print("\n1. GitHub Pages (Recommended):")
                    print("   - Create a GitHub repository")
                    print("   - Push your code including the build/web directory")
                    print("   - Enable GitHub Pages in repository settings")
                    print("   - Set source to the branch with build/web files")
                    print("   - Your game will be at: https://[username].github.io/[repo-name]")
                    
                    print("\n2. Netlify Drop (Easiest):")
                    print("   - Go to app.netlify.com/drop")
                    print("   - Drag and drop the build/web directory")
                    print("   - Get a URL instantly")
                    
                    print("\n3. Vercel:")
                    print("   - Create a Vercel account")
                    print("   - Install Vercel CLI: npm i -g vercel")
                    print("   - Run 'vercel' in the build/web directory")
                    
                    print("\n4. Cloudflare Pages:")
                    print("   - Create a Cloudflare account")
                    print("   - Go to Pages → Create a project")
                    print("   - Connect your GitHub repository")
                    print("   - Set build directory to build/web")
                    
                    print("\nAll options provide:")
                    print("✓ HTTPS security")
                    print("✓ Global CDN for fast loading")
                    print("✓ Automatic updates")
                    print("✓ Custom domain support (optional)")
                
                return True
    
    # If we get here, something went wrong
    print("\n❌ Deployment failed. Check the error messages above.")
    print("Full output:", result.stdout)
    print("Error:", result.stderr)
    return False

if __name__ == "__main__":
    if check_pygbag():
        deploy_game() 