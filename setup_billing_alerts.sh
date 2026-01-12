#!/bin/bash
# YSense™ - Billing Alert Setup Script
# =====================================
# Creates budget alerts to protect against unexpected costs
# =====================================

set -e

PROJECT_ID="ysense-platform-v4-1"
BILLING_ACCOUNT_ID=$(gcloud billing projects describe $PROJECT_ID --format="value(billingAccountName)" | sed 's/billingAccounts\///')

echo "🚨 YSense™ - Setting Up Billing Alerts"
echo "======================================="
echo "Project: $PROJECT_ID"
echo "Billing Account: $BILLING_ACCOUNT_ID"
echo ""

# Check if billing account is found
if [ -z "$BILLING_ACCOUNT_ID" ]; then
    echo "❌ Error: Could not find billing account for project $PROJECT_ID"
    echo ""
    echo "Please run this command to see your billing accounts:"
    echo "  gcloud billing accounts list"
    echo ""
    echo "Then set the BILLING_ACCOUNT_ID manually in this script."
    exit 1
fi

# Create budget with alerts
echo "📊 Creating budget with alert thresholds..."

cat > budget_config.json << EOF
{
  "displayName": "YSense v4.1 Budget Protection",
  "budgetFilter": {
    "projects": ["projects/$PROJECT_ID"]
  },
  "amount": {
    "specifiedAmount": {
      "currencyCode": "USD",
      "units": "50"
    }
  },
  "thresholdRules": [
    {
      "thresholdPercent": 0.2,
      "spendBasis": "CURRENT_SPEND"
    },
    {
      "thresholdPercent": 0.5,
      "spendBasis": "CURRENT_SPEND"
    },
    {
      "thresholdPercent": 0.9,
      "spendBasis": "CURRENT_SPEND"
    },
    {
      "thresholdPercent": 1.0,
      "spendBasis": "CURRENT_SPEND"
    }
  ],
  "notificationsRule": {
    "pubsubTopic": "projects/$PROJECT_ID/topics/budget-alerts",
    "schemaVersion": "1.0"
  }
}
EOF

# Create Pub/Sub topic for alerts
echo "📢 Creating Pub/Sub topic for alerts..."
gcloud pubsub topics create budget-alerts --project=$PROJECT_ID 2>/dev/null || echo "Topic already exists"

# Note: Creating budgets requires using the REST API or Cloud Console
# The gcloud CLI doesn't support budget creation directly

echo ""
echo "======================================="
echo "⚠️  MANUAL STEP REQUIRED"
echo "======================================="
echo ""
echo "Budget configuration has been prepared in: budget_config.json"
echo ""
echo "To complete setup, you need to create the budget manually:"
echo ""
echo "1. Go to: https://console.cloud.google.com/billing/$BILLING_ACCOUNT_ID/budgets"
echo "2. Click 'CREATE BUDGET'"
echo "3. Enter these settings:"
echo ""
echo "   Budget Name: YSense v4.1 Protection"
echo "   Projects: ysense-platform-v4-1"
echo "   Budget Amount: \$50 per month"
echo ""
echo "   Alert Thresholds:"
echo "   • 20% (\$10) - First warning"
echo "   • 50% (\$25) - Critical warning"
echo "   • 90% (\$45) - Emergency alert"
echo "   • 100% (\$50) - Maximum budget"
echo ""
echo "   Notification Email: alton@ysenseai.org"
echo ""
echo "4. Click 'FINISH'"
echo ""
echo "======================================="
echo ""
echo "📧 You will receive emails at these thresholds:"
echo "  • \$10 - 'Your costs are rising'"
echo "  • \$25 - 'Critical: Review your usage'"
echo "  • \$45 - 'Emergency: Near budget limit'"
echo "  • \$50 - 'Budget limit reached'"
echo ""
echo "🛡️  With our deployment protections, you should never hit these limits!"
echo "======================================="

# Clean up
rm -f budget_config.json
