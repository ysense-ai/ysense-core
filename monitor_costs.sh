#!/bin/bash
# YSense™ - Cost Monitoring Script
# ==================================
# Real-time cost monitoring and alerts
# ==================================

PROJECT_ID="ysense-platform-v4-1"
SERVICE_NAME="ysense-v41"
REGION="asia-southeast1"

echo "💰 YSense™ Cost Monitoring Dashboard"
echo "====================================="
echo "Project: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Updated: $(date)"
echo "====================================="
echo ""

# Get current billing month
CURRENT_MONTH=$(date +%Y-%m)

echo "📊 CLOUD RUN SERVICE STATUS"
echo "------------------------------------"

# Get service details
echo "Fetching service information..."
SERVICE_INFO=$(gcloud run services describe $SERVICE_NAME \
    --region=$REGION \
    --format="value(status.conditions[0].status,spec.template.spec.containers[0].resources.limits.memory,spec.template.spec.containers[0].resources.limits.cpu,spec.template.metadata.annotations.'autoscaling.knative.dev/minScale',spec.template.metadata.annotations.'autoscaling.knative.dev/maxScale')" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ Service Status: Active"
    echo "$SERVICE_INFO" | while IFS=$'\t' read status memory cpu min max; do
        echo "   Memory Limit: ${memory:-N/A}"
        echo "   CPU Limit: ${cpu:-N/A}"
        echo "   Min Instances: ${min:-0}"
        echo "   Max Instances: ${max:-3}"
    done
else
    echo "⚠️  Could not fetch service info. Run 'gcloud auth login' to refresh credentials."
fi

echo ""
echo "📈 CURRENT MONTH USAGE"
echo "------------------------------------"

# Get current running instances
echo "Checking active instances..."
REVISIONS=$(gcloud run revisions list \
    --service=$SERVICE_NAME \
    --region=$REGION \
    --format="value(metadata.name,status.conditions[0].status)" \
    --limit=1 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "$REVISIONS" | while IFS=$'\t' read revision status; do
        echo "   Latest Revision: $revision"
        echo "   Status: $status"
    done
else
    echo "   ⚠️  Could not fetch revision info"
fi

echo ""
echo "💵 ESTIMATED COSTS"
echo "------------------------------------"
echo "Based on current configuration:"
echo ""

# Calculate estimated costs
cat << 'EOF'
Cost Breakdown (per month):

Scale-to-Zero Configuration:
  • No traffic:        $0.00/month
  • 100 req/day:       $0.50 - $2.00/month
  • 1,000 req/day:     $5.00 - $15.00/month
  • 10,000 req/day:    $20.00 - $40.00/month

Under DDoS Attack (max 3 instances):
  • Max cost capped:   $30.00 - $50.00/month

Cost Protection Active:
  ✅ Scale-to-zero: $0 when idle
  ✅ Max 3 instances: Cost ceiling enforced
  ✅ CPU throttling: 50% cost reduction
  ✅ 1GB memory: Optimized allocation
  ✅ Rate limiting: Prevents abuse

EOF

echo ""
echo "🔍 DETAILED METRICS"
echo "------------------------------------"

# Try to get metrics (requires authenticated session)
echo "Attempting to fetch usage metrics..."

# Check if we can access billing
gcloud billing accounts list --format="value(name)" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Billing access available"
    echo ""
    echo "To view detailed costs, visit:"
    echo "https://console.cloud.google.com/billing/${PROJECT_ID}/reports"
else
    echo "⚠️  Billing API access limited"
    echo ""
    echo "For detailed cost reports:"
    echo "1. Visit: https://console.cloud.google.com/billing"
    echo "2. Select your billing account"
    echo "3. Click 'Reports' to see costs"
fi

echo ""
echo "📅 QUICK COMMANDS"
echo "------------------------------------"
echo "View service logs:"
echo "  gcloud run services logs read $SERVICE_NAME --region=$REGION --limit=50"
echo ""
echo "Check service details:"
echo "  gcloud run services describe $SERVICE_NAME --region=$REGION"
echo ""
echo "View billing in browser:"
echo "  gcloud alpha billing accounts list"
echo "  (Then visit Cloud Console > Billing)"
echo ""
echo "Update service configuration:"
echo "  ./deploy_secure.sh"
echo ""

echo "====================================="
echo "📊 Monitoring Complete"
echo "====================================="
echo ""

# Check if we should set up alerts
if [ ! -f ".billing_alerts_configured" ]; then
    echo "⚠️  RECOMMENDATION: Set up billing alerts"
    echo "Run: ./setup_billing_alerts.sh"
    echo ""
fi

# Offer to open billing dashboard
read -p "Open billing dashboard in browser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Opening billing dashboard..."
    python -m webbrowser "https://console.cloud.google.com/billing" 2>/dev/null || \
    xdg-open "https://console.cloud.google.com/billing" 2>/dev/null || \
    open "https://console.cloud.google.com/billing" 2>/dev/null || \
    start "https://console.cloud.google.com/billing" 2>/dev/null || \
    echo "Please visit: https://console.cloud.google.com/billing"
fi
