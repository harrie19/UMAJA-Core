#!/bin/bash

###############################################################################
# UMAJA-Core Automated Deployment Script
# Purpose: Comprehensive deployment validation and health checking
# Created: 2026-01-03
# Author: UMAJA Team
###############################################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="https://umaja-core-production.up.railway.app"
BACKEND_HEALTH_URL="${BACKEND_URL}/health"
FRONTEND_URL="https://harrie19.github.io/UMAJA-Core/"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
REPORT_FILE="deployment_report_$(date -u +"%Y%m%d_%H%M%S").md"

# Deployment status tracking
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

###############################################################################
# Utility Functions
###############################################################################

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    ((WARNING_CHECKS++))
    ((TOTAL_CHECKS++))
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

###############################################################################
# Health Check Functions
###############################################################################

check_backend_health() {
    print_header "Backend Health Check"
    
    print_info "Checking backend health at: ${BACKEND_HEALTH_URL}"
    
    # Check if backend is reachable
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${BACKEND_HEALTH_URL}" --max-time 10 || echo "000")
    
    if [ "$HTTP_CODE" = "200" ]; then
        print_success "Backend is responding (HTTP $HTTP_CODE)"
        
        # Get detailed health information
        HEALTH_RESPONSE=$(curl -s "${BACKEND_HEALTH_URL}" --max-time 10)
        
        if [ $? -eq 0 ]; then
            echo "$HEALTH_RESPONSE" | jq . 2>/dev/null || echo "$HEALTH_RESPONSE"
            
            # Check specific health indicators if JSON response
            if echo "$HEALTH_RESPONSE" | jq . >/dev/null 2>&1; then
                STATUS=$(echo "$HEALTH_RESPONSE" | jq -r '.status // "unknown"')
                if [ "$STATUS" = "ok" ] || [ "$STATUS" = "healthy" ]; then
                    print_success "Backend health status: $STATUS"
                else
                    print_warning "Backend health status: $STATUS"
                fi
            fi
        fi
    elif [ "$HTTP_CODE" = "000" ]; then
        print_error "Backend is not reachable (Connection timeout)"
    else
        print_error "Backend health check failed (HTTP $HTTP_CODE)"
    fi
}

check_frontend_availability() {
    print_header "Frontend Availability Check"
    
    print_info "Checking GitHub Pages at: ${FRONTEND_URL}"
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${FRONTEND_URL}" --max-time 10 || echo "000")
    
    if [ "$HTTP_CODE" = "200" ]; then
        print_success "Frontend is accessible (HTTP $HTTP_CODE)"
        
        # Check if the page contains expected content
        PAGE_CONTENT=$(curl -s "${FRONTEND_URL}" --max-time 10)
        
        if echo "$PAGE_CONTENT" | grep -q "UMAJA" || echo "$PAGE_CONTENT" | grep -q "umaja"; then
            print_success "Frontend contains UMAJA branding"
        else
            print_warning "Frontend may not have expected content"
        fi
    elif [ "$HTTP_CODE" = "000" ]; then
        print_error "Frontend is not reachable (Connection timeout)"
    else
        print_error "Frontend is not accessible (HTTP $HTTP_CODE)"
    fi
}

test_api_endpoints() {
    print_header "API Endpoints Testing"
    
    # Test common API endpoints
    declare -a ENDPOINTS=(
        "/health:GET"
        "/api/v1/status:GET"
        "/api/health:GET"
    )
    
    for ENDPOINT_INFO in "${ENDPOINTS[@]}"; do
        IFS=':' read -r ENDPOINT METHOD <<< "$ENDPOINT_INFO"
        
        print_info "Testing ${METHOD} ${BACKEND_URL}${ENDPOINT}"
        
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X "${METHOD}" "${BACKEND_URL}${ENDPOINT}" --max-time 10 || echo "000")
        
        if [ "$HTTP_CODE" = "200" ]; then
            print_success "Endpoint ${ENDPOINT} is operational (HTTP $HTTP_CODE)"
        elif [ "$HTTP_CODE" = "404" ]; then
            print_warning "Endpoint ${ENDPOINT} not found (HTTP $HTTP_CODE)"
        elif [ "$HTTP_CODE" = "000" ]; then
            print_warning "Endpoint ${ENDPOINT} timeout or unreachable"
        else
            print_warning "Endpoint ${ENDPOINT} returned HTTP $HTTP_CODE"
        fi
    done
}

validate_environment_files() {
    print_header "Environment Files Validation"
    
    # Check for required environment files
    declare -a ENV_FILES=(
        ".env.example"
        ".env.production.example"
        ".env.development.example"
    )
    
    for ENV_FILE in "${ENV_FILES[@]}"; do
        if [ -f "$ENV_FILE" ]; then
            print_success "Found: $ENV_FILE"
            
            # Check for required variables
            declare -a REQUIRED_VARS=(
                "DATABASE_URL"
                "API_KEY"
                "NODE_ENV"
            )
            
            for VAR in "${REQUIRED_VARS[@]}"; do
                if grep -q "$VAR" "$ENV_FILE" 2>/dev/null; then
                    print_info "  ✓ $VAR defined in $ENV_FILE"
                fi
            done
        else
            print_warning "Missing: $ENV_FILE (consider creating this file)"
        fi
    done
    
    # Check if actual .env file exists (without exposing content)
    if [ -f ".env" ]; then
        print_success "Production .env file exists"
    else
        print_warning "Production .env file not found in current directory"
    fi
}

check_github_actions() {
    print_header "GitHub Actions Workflows Check"
    
    WORKFLOWS_DIR=".github/workflows"
    
    if [ -d "$WORKFLOWS_DIR" ]; then
        print_success "Workflows directory exists"
        
        WORKFLOW_COUNT=$(find "$WORKFLOWS_DIR" -name "*.yml" -o -name "*.yaml" | wc -l)
        
        if [ "$WORKFLOW_COUNT" -gt 0 ]; then
            print_success "Found $WORKFLOW_COUNT workflow file(s)"
            
            # List all workflows
            while IFS= read -r workflow; do
                WORKFLOW_NAME=$(basename "$workflow")
                print_info "  - $WORKFLOW_NAME"
                
                # Check for common issues in workflow files
                if grep -q "on:" "$workflow" && grep -q "jobs:" "$workflow"; then
                    print_info "    ✓ Valid workflow structure"
                else
                    print_warning "    ⚠ Workflow may have structural issues"
                fi
            done < <(find "$WORKFLOWS_DIR" -name "*.yml" -o -name "*.yaml")
        else
            print_warning "No workflow files found"
        fi
    else
        print_error "Workflows directory does not exist"
    fi
}

check_dependencies() {
    print_header "Dependencies Check"
    
    # Check for package.json
    if [ -f "package.json" ]; then
        print_success "package.json found"
        
        # Check for outdated packages (if npm is available)
        if command -v npm &> /dev/null; then
            print_info "Checking for outdated packages..."
            OUTDATED=$(npm outdated 2>&1 || true)
            if [ -z "$OUTDATED" ]; then
                print_success "All packages are up to date"
            else
                print_warning "Some packages may be outdated"
                echo "$OUTDATED" | head -10
            fi
        fi
    fi
    
    # Check for requirements.txt (Python projects)
    if [ -f "requirements.txt" ]; then
        print_success "requirements.txt found"
    fi
}

check_security() {
    print_header "Security Checks"
    
    # Check SSL/TLS certificate for backend
    print_info "Checking SSL certificate for backend..."
    
    if echo | openssl s_client -connect umaja-core-production.up.railway.app:443 -servername umaja-core-production.up.railway.app 2>/dev/null | grep -q "Verify return code: 0"; then
        print_success "Backend SSL certificate is valid"
    else
        print_warning "Could not verify backend SSL certificate"
    fi
    
    # Check for sensitive files that shouldn't be committed
    declare -a SENSITIVE_FILES=(
        ".env"
        "*.key"
        "*.pem"
        "*.p12"
        "*.pfx"
    )
    
    print_info "Checking for sensitive files in git..."
    FOUND_SENSITIVE=false
    
    for PATTERN in "${SENSITIVE_FILES[@]}"; do
        if git ls-files | grep -q "$PATTERN" 2>/dev/null; then
            print_warning "Found potentially sensitive file matching: $PATTERN"
            FOUND_SENSITIVE=true
        fi
    done
    
    if [ "$FOUND_SENSITIVE" = false ]; then
        print_success "No sensitive files found in git"
    fi
}

generate_deployment_report() {
    print_header "Generating Deployment Report"
    
    cat > "$REPORT_FILE" << EOF
# UMAJA-Core Deployment Report

**Generated:** $TIMESTAMP  
**Report File:** $REPORT_FILE

---

## Executive Summary

| Metric | Count |
|--------|-------|
| Total Checks | $TOTAL_CHECKS |
| ✅ Passed | $PASSED_CHECKS |
| ❌ Failed | $FAILED_CHECKS |
| ⚠️  Warnings | $WARNING_CHECKS |

### Overall Status

EOF

    # Calculate success rate
    if [ $TOTAL_CHECKS -gt 0 ]; then
        SUCCESS_RATE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
        
        if [ $FAILED_CHECKS -eq 0 ]; then
            echo "**🟢 HEALTHY** - All critical checks passed" >> "$REPORT_FILE"
        elif [ $SUCCESS_RATE -ge 80 ]; then
            echo "**🟡 DEGRADED** - Some issues detected but system is operational" >> "$REPORT_FILE"
        else
            echo "**🔴 CRITICAL** - Multiple failures detected, immediate attention required" >> "$REPORT_FILE"
        fi
        
        echo "" >> "$REPORT_FILE"
        echo "**Success Rate:** ${SUCCESS_RATE}%" >> "$REPORT_FILE"
    fi
    
    cat >> "$REPORT_FILE" << EOF

---

## Detailed Results

### 🔍 Backend Health
- **URL:** $BACKEND_URL
- **Health Endpoint:** $BACKEND_HEALTH_URL
- **Status:** Check logs for details

### 🌐 Frontend Availability
- **URL:** $FRONTEND_URL
- **Status:** Check logs for details

### 🔌 API Endpoints
- Health checks completed
- See logs for individual endpoint results

### 📋 Environment Configuration
- Environment files validated
- See logs for missing files or variables

### ⚙️ GitHub Actions
- Workflow files checked
- See logs for workflow details

### 🔒 Security
- SSL certificates validated
- Sensitive file scan completed

---

## Next Steps

EOF

    if [ $FAILED_CHECKS -gt 0 ]; then
        cat >> "$REPORT_FILE" << EOF
### 🚨 Immediate Actions Required

1. **Review Failed Checks** - Address all failed checks immediately
2. **Check Error Logs** - Review Railway and application logs for errors
3. **Verify Configuration** - Ensure all environment variables are set correctly
4. **Test Manually** - Perform manual testing of failed endpoints
5. **Monitor Continuously** - Set up monitoring alerts for critical services

EOF
    else
        cat >> "$REPORT_FILE" << EOF
### ✅ Recommended Actions

1. **Monitor Performance** - Continue monitoring application metrics
2. **Review Warnings** - Address any warnings when convenient
3. **Update Documentation** - Keep deployment docs up to date
4. **Plan Next Release** - System is stable, ready for new features
5. **Backup Data** - Ensure regular backups are configured

EOF
    fi
    
    cat >> "$REPORT_FILE" << EOF
### 📊 Monitoring Recommendations

- Set up uptime monitoring for critical endpoints
- Configure alerting for health check failures
- Review logs regularly for anomalies
- Monitor resource usage (CPU, memory, database)
- Track API response times and error rates

### 🔄 Continuous Improvement

- Automate deployment with CI/CD
- Implement blue-green deployments
- Set up automated rollback procedures
- Create disaster recovery plan
- Document incident response procedures

---

## Resources

- **Backend Dashboard:** https://railway.app
- **Frontend Repository:** https://github.com/harrie19/UMAJA-Core
- **Documentation:** [Add your docs URL]
- **Support:** [Add your support channel]

---

*This report was automatically generated by the UMAJA-Core deployment automation script.*
EOF

    print_success "Report generated: $REPORT_FILE"
    
    echo ""
    cat "$REPORT_FILE"
}

###############################################################################
# Main Execution
###############################################################################

main() {
    clear
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║         UMAJA-Core Automated Deployment Validator           ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo "Started at: $TIMESTAMP"
    echo ""
    
    # Check required commands
    print_info "Checking required dependencies..."
    
    MISSING_DEPS=false
    for cmd in curl jq git openssl; do
        if ! command -v $cmd &> /dev/null; then
            print_warning "$cmd is not installed (some checks may be skipped)"
            MISSING_DEPS=true
        fi
    done
    
    if [ "$MISSING_DEPS" = false ]; then
        print_success "All required dependencies are available"
    fi
    
    echo ""
    
    # Run all checks
    check_backend_health
    check_frontend_availability
    test_api_endpoints
    validate_environment_files
    check_github_actions
    check_dependencies
    check_security
    generate_deployment_report
    
    # Final summary
    print_header "Deployment Validation Complete"
    
    echo ""
    echo "Summary:"
    echo "  Total Checks: $TOTAL_CHECKS"
    echo -e "  ${GREEN}Passed: $PASSED_CHECKS${NC}"
    echo -e "  ${RED}Failed: $FAILED_CHECKS${NC}"
    echo -e "  ${YELLOW}Warnings: $WARNING_CHECKS${NC}"
    echo ""
    
    if [ $FAILED_CHECKS -eq 0 ]; then
        echo -e "${GREEN}✓ Deployment validation passed successfully!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Deployment validation completed with failures.${NC}"
        echo -e "${YELLOW}Please review the report and address the issues.${NC}"
        exit 1
    fi
}

# Run main function
main "$@"
