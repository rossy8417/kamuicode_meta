#!/bin/bash

# Test local success pattern with Claude Code SDK
echo "🧪 Testing local success pattern with Claude Code SDK..."

# Create test image info (simulating scene_1_image_info.json)
cat > scene_1_image_info.json << 'EOF'
{
  "scene_number": 1,
  "image_url": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
  "prompt_used": "A futuristic AI robot in a modern office setting",
  "generation_time": "2025-07-28T07:20:00Z",
  "description": "Scene 1: AI robot introduction"
}
EOF

echo "📋 Created test image info:"
cat scene_1_image_info.json | jq '.'

# Test Claude Code SDK with our improved prompt
echo "🎬 Testing Claude Code SDK execution..."

claude -p "TEST: Video generation with mandatory download pattern

CRITICAL: Follow LOCAL SUCCESS PATTERN that works:
'For images/videos/3D generation: After generation completes, ALWAYS do URL download and open. Download to current directory. Always use full authenticated URL path (long for Google, short for FAL). No abbreviations. For I2V/I2I inputs use Google URLs, no abbreviations (not file paths!). Show saved file location with full path from ~.'

TASK: Test video generation for scene 1

STEP 1: Read image info and simulate video generation
1. Read scene_1_image_info.json
2. Extract image_url
3. Show that you would use i2v-fal-hailuo-02-pro with this URL
4. Simulate getting a video URL result

STEP 2: DEMONSTRATE DOWNLOAD PATTERN
5. Show exactly how you would download the video
6. Demonstrate: curl -o 'scene_1_video.mp4' '<FULL_VIDEO_URL>'
7. Show verification: ls -la scene_1_video.mp4

REQUIREMENTS:
- Show the complete workflow process
- Demonstrate proper URL handling (no abbreviations)
- Show file verification steps" \
--mcp-config .claude/mcp-kamuicode.json \
--output-format json > test_response.json

echo "📋 Claude Code SDK response:"
cat test_response.json | jq '.'

echo "✅ Test completed. Check response for proper pattern execution."