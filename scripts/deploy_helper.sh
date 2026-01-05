#!/bin/bash
set -e

echo "=========================================="
echo "  UMAJA World Tour - Deployment Helper"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo "→ $1"
}

# Check prerequisites
echo "Checking prerequisites..."
echo ""

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    print_success "GitHub CLI (gh) installed"
    
    # Check if authenticated
    if gh auth status &> /dev/null; then
        print_success "GitHub CLI authenticated"
        GH_AUTHENTICATED=true
    else
        print_warning "GitHub CLI not authenticated"
        print_info "Run: gh auth login"
        GH_AUTHENTICATED=false
    fi
else
    print_warning "GitHub CLI (gh) not installed"
    print_info "Install from: https://cli.github.com/"
    GH_AUTHENTICATED=false
fi

# Check if Railway CLI is installed
if command -v railway &> /dev/null; then
    print_success "Railway CLI installed"
    RAILWAY_INSTALLED=true
else
    print_warning "Railway CLI not installed"
    print_info "Install: npm install -g @railway/cli"
    RAILWAY_INSTALLED=false
fi

echo ""
echo "=========================================="
echo "  Deployment Options"
echo "=========================================="
echo ""

echo "This script can help you deploy UMAJA World Tour:"
echo ""
echo "1. 📄 Deploy GitHub Pages (Dashboard)"
echo "2. 🚂 Deploy to Railway (Backend API)"
echo "3. 🌐 Deploy to Render (Alternative Backend)"
echo "4. 📊 Check deployment status"
echo "5. 🧪 Run local server for testing"
echo "6. ❌ Exit"
echo ""

read -p "Select option (1-6): " option

case $option in
    1)
        echo ""
        echo "=========================================="
        echo "  GitHub Pages Deployment"
        echo "=========================================="
        echo ""
        
        if [ "$GH_AUTHENTICATED" = true ]; then
            echo "To deploy GitHub Pages:"
            echo ""
            echo "1. Enable GitHub Pages in repository settings:"
            print_info "Visit: https://github.com/harrie19/UMAJA-Core/settings/pages"
            print_info "Source: Deploy from branch 'main', folder '/docs'"
            echo ""
            
            echo "2. The PR must be merged to main branch first"
            print_info "Current branch: $(git branch --show-current)"
            echo ""
            
            read -p "Would you like to check if GitHub Pages is enabled? (y/n): " check_pages
            if [ "$check_pages" = "y" ]; then
                print_info "Checking GitHub Pages status..."
                gh api repos/harrie19/UMAJA-Core/pages 2>&1 || print_warning "GitHub Pages not configured yet"
            fi
            
            echo ""
            print_info "After merging to main, GitHub Pages will auto-deploy"
            print_info "Workflow: .github/workflows/pages-deploy.yml"
        else
            print_error "GitHub CLI authentication required"
            print_info "Run: gh auth login"
        fi
        ;;
        
    2)
        echo ""
        echo "=========================================="
        echo "  Railway Deployment"
        echo "=========================================="
        echo ""
        
        if [ "$RAILWAY_INSTALLED" = true ]; then
            echo "Deploying to Railway..."
            echo ""
            
            # Check if logged in to Railway
            if railway whoami &> /dev/null; then
                print_success "Railway CLI authenticated"
                
                echo ""
                print_info "Checking Railway project..."
                
                if railway status &> /dev/null; then
                    print_success "Railway project linked"
                    
                    echo ""
                    read -p "Deploy to Railway now? (y/n): " deploy_railway
                    
                    if [ "$deploy_railway" = "y" ]; then
                        print_info "Deploying..."
                        railway up || print_error "Deployment failed"
                        
                        echo ""
                        print_info "Getting deployment URL..."
                        railway domain || print_warning "Could not retrieve domain"
                    fi
                else
                    print_warning "No Railway project linked"
                    echo ""
                    echo "To link a Railway project:"
                    print_info "1. Create project at https://railway.app"
                    print_info "2. Run: railway link"
                    print_info "3. Run this script again"
                fi
            else
                print_warning "Railway CLI not authenticated"
                print_info "Run: railway login"
            fi
        else
            print_error "Railway CLI not installed"
            print_info "Install: npm install -g @railway/cli"
        fi
        ;;
        
    3)
        echo ""
        echo "=========================================="
        echo "  Render Deployment"
        echo "=========================================="
        echo ""
        
        echo "To deploy to Render:"
        echo ""
        echo "1. Visit: https://render.com"
        echo "2. Create New → Web Service"
        echo "3. Connect to GitHub repo: harrie19/UMAJA-Core"
        echo "4. Render will auto-detect render.yaml"
        echo "5. Click 'Create Web Service'"
        echo ""
        print_info "Configuration file: render.yaml (already in repo)"
        print_info "Health check: /health"
        print_info "Start command: python api/simple_server.py"
        ;;
        
    4)
        echo ""
        echo "=========================================="
        echo "  Deployment Status Check"
        echo "=========================================="
        echo ""
        
        echo "Checking deployment status..."
        echo ""
        
        # Check GitHub Pages
        print_info "GitHub Pages (Dashboard):"
        echo "   URL: https://harrie19.github.io/UMAJA-Core/"
        if curl -s --max-time 5 https://harrie19.github.io/UMAJA-Core/ > /dev/null 2>&1; then
            print_success "   ONLINE"
        else
            print_warning "   NOT ACCESSIBLE"
        fi
        echo ""
        
        # Check Railway
        print_info "Railway Backend:"
        echo "   URL: https://web-production-6ec45.up.railway.app"
        if curl -s --max-time 5 https://web-production-6ec45.up.railway.app/health > /dev/null 2>&1; then
            print_success "   ONLINE"
            health_response=$(curl -s https://web-production-6ec45.up.railway.app/health | jq -r '.status' 2>/dev/null || echo "unknown")
            echo "   Health: $health_response"
        else
            print_warning "   NOT ACCESSIBLE"
        fi
        echo ""
        
        # Local files check
        print_info "Local files ready:"
        [ -f "docs/index.html" ] && print_success "   docs/index.html" || print_error "   docs/index.html MISSING"
        [ -f "docs/sitemap.xml" ] && print_success "   docs/sitemap.xml" || print_error "   docs/sitemap.xml MISSING"
        [ -f "docs/robots.txt" ] && print_success "   docs/robots.txt" || print_error "   docs/robots.txt MISSING"
        [ -f "api/simple_server.py" ] && print_success "   api/simple_server.py" || print_error "   api/simple_server.py MISSING"
        [ -f "railway.json" ] && print_success "   railway.json" || print_error "   railway.json MISSING"
        [ -f "render.yaml" ] && print_success "   render.yaml" || print_error "   render.yaml MISSING"
        ;;
        
    5)
        echo ""
        echo "=========================================="
        echo "  Local Server Testing"
        echo "=========================================="
        echo ""
        
        print_info "Starting local server..."
        echo ""
        
        # Check if dependencies are installed
        if python3 -c "import flask" 2>/dev/null; then
            print_success "Flask installed"
        else
            print_warning "Installing dependencies..."
            pip install -q -r requirements.txt
        fi
        
        echo ""
        print_success "Starting server on http://localhost:5000"
        print_info "Press Ctrl+C to stop"
        echo ""
        print_info "Test endpoints:"
        echo "   - http://localhost:5000/health"
        echo "   - http://localhost:5000/api/ai-agents"
        echo "   - http://localhost:5000/worldtour/status"
        echo "   - http://localhost:5000/sitemap.xml"
        echo ""
        
        python3 api/simple_server.py
        ;;
        
    6)
        echo ""
        print_info "Exiting deployment helper"
        exit 0
        ;;
        
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "  Deployment Helper Complete"
echo "=========================================="
echo ""
