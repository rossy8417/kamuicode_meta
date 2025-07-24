#!/bin/bash

# Claude Code Workflow Monitoring Script
# Usage: ./monitor-workflows.sh [duration_minutes] [check_interval_seconds]

set -e

# Configuration
DURATION_MINUTES=${1:-30}
CHECK_INTERVAL=${2:-30}
ALERT_THRESHOLD=50

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Starting Claude Code Workflow Monitor${NC}"
echo -e "${BLUE}Duration: ${DURATION_MINUTES} minutes${NC}"
echo -e "${BLUE}Check Interval: ${CHECK_INTERVAL} seconds${NC}"
echo "=================================================="

# Create monitoring directory
mkdir -p .monitoring/{logs,alerts}

START_TIME=$(date +%s)
END_TIME=$((START_TIME + DURATION_MINUTES * 60))
CHECK_COUNT=0

# Real-time monitoring loop
while [ $(date +%s) -lt $END_TIME ]; do
    CHECK_COUNT=$((CHECK_COUNT + 1))
    CURRENT_TIME=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    
    echo -e "\n${YELLOW}📋 Check #${CHECK_COUNT} - ${CURRENT_TIME}${NC}"
    
    # Check workflow status using GitHub CLI
    if command -v gh &> /dev/null; then
        echo "🔄 Fetching recent workflow runs..."
        
        # Get recent runs of meta workflow
        RUNS_JSON=$(gh run list --workflow="kamuicode-meta-generator.yml" --limit 10 --json status,conclusion,createdAt,displayTitle,databaseId 2>/dev/null || echo "[]")
        
        if [ "$RUNS_JSON" != "[]" ]; then
            # Parse results
            TOTAL_RUNS=$(echo "$RUNS_JSON" | jq 'length')
            FAILED_RUNS=$(echo "$RUNS_JSON" | jq '[.[] | select(.conclusion == "failure")] | length')
            IN_PROGRESS=$(echo "$RUNS_JSON" | jq '[.[] | select(.status == "in_progress")] | length')
            SUCCESS_RUNS=$(echo "$RUNS_JSON" | jq '[.[] | select(.conclusion == "success")] | length')
            
            # Calculate failure rate
            if [ "$TOTAL_RUNS" -gt 0 ]; then
                FAILURE_RATE=$(echo "scale=2; $FAILED_RUNS * 100 / $TOTAL_RUNS" | bc 2>/dev/null || echo "0")
                SUCCESS_RATE=$(echo "scale=2; $SUCCESS_RUNS * 100 / $TOTAL_RUNS" | bc 2>/dev/null || echo "0")
            else
                FAILURE_RATE=0
                SUCCESS_RATE=0
            fi
            
            # Display status
            echo -e "📊 ${GREEN}Status Summary:${NC}"
            echo -e "  Total Runs: ${TOTAL_RUNS}"
            echo -e "  ✅ Success: ${SUCCESS_RUNS} (${SUCCESS_RATE}%)"
            echo -e "  ❌ Failed: ${FAILED_RUNS} (${FAILURE_RATE}%)"
            echo -e "  🔄 In Progress: ${IN_PROGRESS}"
            
            # Check for active runs
            if [ "$IN_PROGRESS" -gt 0 ]; then
                echo -e "${BLUE}🔄 Active workflows detected:${NC}"
                echo "$RUNS_JSON" | jq -r '.[] | select(.status == "in_progress") | "  - \(.displayTitle) (ID: \(.databaseId))"'
                
                # Monitor active runs in detail
                ACTIVE_IDS=$(echo "$RUNS_JSON" | jq -r '.[] | select(.status == "in_progress") | .databaseId')
                for run_id in $ACTIVE_IDS; do
                    echo -e "${BLUE}📋 Monitoring Run ID: ${run_id}${NC}"
                    
                    # Get detailed job status
                    JOB_STATUS=$(gh run view "$run_id" --json jobs 2>/dev/null || echo '{"jobs":[]}')
                    
                    if [ "$JOB_STATUS" != '{"jobs":[]}' ]; then
                        echo "$JOB_STATUS" | jq -r '.jobs[] | "  📝 \(.name): \(.status) (\(.conclusion // "running"))"'
                    fi
                done
            fi
            
            # Alert on high failure rate
            if (( $(echo "$FAILURE_RATE > $ALERT_THRESHOLD" | bc -l 2>/dev/null || echo "0") )); then
                echo -e "${RED}🚨 ALERT: High failure rate detected (${FAILURE_RATE}%)${NC}"
                
                # Create alert log
                cat > ".monitoring/alerts/alert-$(date +%Y%m%d-%H%M%S).json" << EOF
{
    "timestamp": "${CURRENT_TIME}",
    "check_number": ${CHECK_COUNT},
    "failure_rate": ${FAILURE_RATE},
    "threshold": ${ALERT_THRESHOLD},
    "total_runs": ${TOTAL_RUNS},
    "failed_runs": ${FAILED_RUNS},
    "alert_level": "high"
}
EOF
                
                # Show recent failures
                echo -e "${RED}Recent failures:${NC}"
                echo "$RUNS_JSON" | jq -r '.[] | select(.conclusion == "failure") | "  ❌ \(.displayTitle) - \(.createdAt)"' | head -3
                
            elif [ "$FAILURE_RATE" != "0" ]; then
                echo -e "${YELLOW}⚠️ Some failures detected (${FAILURE_RATE}%), monitoring...${NC}"
            else
                echo -e "${GREEN}✅ All recent workflows successful${NC}"
            fi
            
        else
            echo -e "${YELLOW}ℹ️ No recent workflow runs found${NC}"
        fi
        
    else
        echo -e "${RED}❌ GitHub CLI not available${NC}"
    fi
    
    # Log this check
    cat > ".monitoring/logs/check-$(date +%Y%m%d-%H%M%S).json" << EOF
{
    "check_number": ${CHECK_COUNT},
    "timestamp": "${CURRENT_TIME}",
    "total_runs": ${TOTAL_RUNS:-0},
    "failed_runs": ${FAILED_RUNS:-0},
    "in_progress": ${IN_PROGRESS:-0},
    "failure_rate": ${FAILURE_RATE:-0}
}
EOF
    
    # Wait for next check
    REMAINING_TIME=$(( (END_TIME - $(date +%s)) / 60 ))
    if [ $REMAINING_TIME -gt 0 ]; then
        echo -e "${BLUE}⏰ Next check in ${CHECK_INTERVAL}s (${REMAINING_TIME} minutes remaining)${NC}"
        sleep $CHECK_INTERVAL
    fi
done

# Final summary
echo -e "\n${GREEN}=================================================="
echo -e "🏁 Monitoring Session Complete"
echo -e "Total Checks: ${CHECK_COUNT}"
echo -e "Duration: ${DURATION_MINUTES} minutes"
echo -e "==================================================${NC}"

# Generate summary report
cat > ".monitoring/session-summary.json" << EOF
{
    "session": {
        "start_time": "$(date -d @$START_TIME -u +"%Y-%m-%d %H:%M:%S UTC")",
        "end_time": "$(date -u +"%Y-%m-%d %H:%M:%S UTC")",
        "duration_minutes": ${DURATION_MINUTES},
        "total_checks": ${CHECK_COUNT},
        "check_interval_seconds": ${CHECK_INTERVAL}
    }
}
EOF

echo -e "${BLUE}📄 Monitoring data saved to .monitoring/${NC}"
echo -e "${BLUE}Run summary: .monitoring/session-summary.json${NC}"