#!/usr/bin/env python3
"""
Dynamic Inputs Generator for Meta Workflow System
動的モーダル入力仕様からGitHub Actions workflow inputsを生成

Usage:
    python3 generate-dynamic-inputs.py --template meta/examples/image-generation.yml --output generated.yml
"""

import yaml
import argparse
import sys
from pathlib import Path

def load_template_spec(template_path):
    """テンプレートファイルから動的inputs仕様を読み込み"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = yaml.safe_load(f)
        
        if 'dynamic_inputs_spec' not in template_data:
            print(f"⚠️ No dynamic_inputs_spec found in {template_path}")
            return None, template_data
            
        return template_data['dynamic_inputs_spec'], template_data
    except Exception as e:
        print(f"❌ Error loading template: {e}")
        return None, None

def convert_input_type(input_spec):
    """動的input仕様をGitHub Actions input形式に変換"""
    github_input = {}
    
    # 基本情報
    github_input['description'] = input_spec.get('description', input_spec.get('label', ''))
    github_input['required'] = input_spec.get('required', False)
    
    # 型変換
    input_type = input_spec.get('type', 'string')
    if input_type in ['textarea', 'text']:
        github_input['type'] = 'string'
    elif input_type == 'select':
        github_input['type'] = 'choice'
        if 'options' in input_spec:
            github_input['options'] = [opt['value'] for opt in input_spec['options']]
    elif input_type in ['number', 'range']:
        github_input['type'] = 'number'
    else:
        github_input['type'] = 'string'
    
    # デフォルト値
    if 'default' in input_spec:
        github_input['default'] = input_spec['default']
    
    return github_input

def generate_github_actions_inputs(dynamic_spec):
    """動的inputs仕様からGitHub Actions workflow inputs定義を生成"""
    if not dynamic_spec or 'form_sections' not in dynamic_spec:
        return {}
    
    github_inputs = {}
    
    for section in dynamic_spec['form_sections']:
        if 'inputs' not in section:
            continue
            
        for input_spec in section['inputs']:
            input_name = input_spec.get('name')
            if not input_name:
                continue
                
            github_inputs[input_name] = convert_input_type(input_spec)
    
    return github_inputs

def generate_workflow_file(template_data, github_inputs, output_path):
    """GitHub Actions workflowファイルを生成"""
    
    # 基本的なワークフロー構造を作成
    workflow = {
        'name': f"Generated {template_data.get('name', 'Workflow')} - Dynamic Interface",
        'on': {
            'workflow_dispatch': {
                'inputs': github_inputs
            }
        },
        'permissions': {
            'contents': 'write',
            'issues': 'write',
            'actions': 'read'
        },
        'jobs': {
            'setup-dynamic-execution': {
                'runs-on': 'ubuntu-latest',
                'outputs': {
                    'optimized-prompt': '${{ steps.optimize.outputs.prompt }}',
                    'execution-plan': '${{ steps.plan.outputs.plan }}'
                },
                'steps': [
                    {
                        'name': 'Checkout repository',
                        'uses': 'actions/checkout@v4'
                    },
                    {
                        'name': 'Setup dynamic inputs processing',
                        'id': 'setup',
                        'run': '''
echo "🎯 Processing dynamic inputs..."
mkdir -p .logs/dynamic-inputs

# ユーザー入力を記録
cat > .logs/dynamic-inputs/user-inputs.json << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "inputs": {''' + ''.join([f'''
    "{name}": "${{{{ github.event.inputs.{name} }}}}"{"," if i < len(github_inputs)-1 else ""}''' 
                           for i, name in enumerate(github_inputs.keys())]) + '''
  }
}
EOF

echo "✅ Dynamic inputs recorded"
                        '''
                    },
                    {
                        'name': 'Optimize prompt from user input',
                        'id': 'optimize', 
                        'run': '''
echo "🚀 Optimizing prompt based on user inputs..."

# メインプロンプトを取得
MAIN_PROMPT="${{ github.event.inputs.main_prompt || 'high quality image' }}"
ART_STYLE="${{ github.event.inputs.art_style || 'photorealistic' }}"
QUALITY_LEVEL="${{ github.event.inputs.quality_level || '8' }}"

# プロンプト最適化
OPTIMIZED_PROMPT="$MAIN_PROMPT"

# アートスタイル追加
case "$ART_STYLE" in
  "photorealistic") OPTIMIZED_PROMPT="$OPTIMIZED_PROMPT, photorealistic, high detail, professional photography" ;;
  "anime") OPTIMIZED_PROMPT="$OPTIMIZED_PROMPT, anime style, manga art, cel shading, vibrant colors" ;;
  "oil_painting") OPTIMIZED_PROMPT="$OPTIMIZED_PROMPT, oil painting, classical art, brush strokes, artistic" ;;
  "digital_art") OPTIMIZED_PROMPT="$OPTIMIZED_PROMPT, digital art, concept art, detailed, modern" ;;
  "watercolor") OPTIMIZED_PROMPT="$OPTIMIZED_PROMPT, watercolor painting, soft colors, artistic, flowing" ;;
esac

# 品質レベル追加
if [ "$QUALITY_LEVEL" -ge 8 ]; then
  OPTIMIZED_PROMPT="$OPTIMIZED_PROMPT, ultra high quality, masterpiece, best quality"
elif [ "$QUALITY_LEVEL" -ge 6 ]; then
  OPTIMIZED_PROMPT="$OPTIMIZED_PROMPT, high quality, detailed"
fi

echo "prompt=$OPTIMIZED_PROMPT" >> $GITHUB_OUTPUT
echo "✅ Optimized prompt: $OPTIMIZED_PROMPT"
                        '''
                    },
                    {
                        'name': 'Create execution plan',
                        'id': 'plan',
                        'run': '''
echo "📋 Creating execution plan..."

# MCPサービス優先度を決定
MCP_PRIORITY="${{ github.event.inputs.mcp_service_priority || 'balanced' }}"
IMAGE_COUNT="${{ github.event.inputs.image_count || '4' }}"

case "$MCP_PRIORITY" in
  "ultra_quality") MCP_SERVICES="t2i-fal-imagen4-ultra,t2i-fal-imagen4-fast,t2i-google-imagen3" ;;
  "balanced") MCP_SERVICES="t2i-fal-imagen4-fast,t2i-fal-imagen4-ultra,t2i-google-imagen3" ;;
  "speed_priority") MCP_SERVICES="t2i-fal-imagen4-fast,t2i-google-imagen3,t2i-fal-imagen4-ultra" ;;
  "google_only") MCP_SERVICES="t2i-google-imagen3" ;;
  *) MCP_SERVICES="t2i-fal-imagen4-fast,t2i-google-imagen3" ;;
esac

# 実行プラン作成
cat > .logs/dynamic-inputs/execution-plan.json << EOF
{
  "mcp_services": "$MCP_SERVICES",
  "image_count": $IMAGE_COUNT,
  "parallel_execution": true,
  "retry_strategy": "fallback_service"
}
EOF

echo "plan=$MCP_SERVICES" >> $GITHUB_OUTPUT
echo "✅ Execution plan created with services: $MCP_SERVICES"
                        '''
                    }
                ]
            },
            'execute-image-generation': {
                'needs': 'setup-dynamic-execution',
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {
                        'name': 'Checkout repository',
                        'uses': 'actions/checkout@v4'
                    },
                    {
                        'name': 'Setup MCP configuration and scripts',
                        'run': '''
echo "🔧 Setting up MCP configuration and script dependencies..."
mkdir -p ~/.claude

# スクリプトの実行権限確認・設定
if [ -f "script/content-download-manager.sh" ]; then
  chmod +x script/content-download-manager.sh
  echo "✅ content-download-manager.sh executable"
else
  echo "⚠️ content-download-manager.sh not found"
fi

if [ -f "script/enhance-content-quality.py" ]; then
  echo "✅ enhance-content-quality.py found"
else
  echo "⚠️ enhance-content-quality.py not found"
fi

# Python依存関係インストール
if [ -f "requirements.txt" ]; then
  echo "📦 Installing Python dependencies..."
  pip3 install -r requirements.txt --quiet || echo "⚠️ Some dependencies may not be available"
fi

# MCP設定をセットアップ（既存ファイル参照）
if [ -f "${HOME}/.claude/mcp-kamuicode.json" ]; then
  echo "✅ Using existing MCP configuration at ~/.claude/mcp-kamuicode.json"
elif [ -f "mcp-kamuicode.json" ]; then
  echo "📋 Copying MCP config from repository"
  cp mcp-kamuicode.json ~/.claude/mcp-kamuicode.json
else
  echo "⚠️ MCP configuration not found"
  echo "Please ensure mcp-kamuicode.json exists in repository or ~/.claude/"
  echo "AI generation services may not work without proper MCP configuration"
fi
                        '''
                    },
                    {
                        'name': 'Generate and enhance content with 3-iteration quality process',
                        'run': '''
echo "🎨 Starting AI content generation with 3-iteration quality enhancement..."

OPTIMIZED_PROMPT="${{ needs.setup-dynamic-execution.outputs.optimized-prompt }}"
MCP_SERVICES="${{ needs.setup-dynamic-execution.outputs.execution-plan }}"
IMAGE_COUNT="${{ github.event.inputs.image_count || '4' }}"
CONTENT_CATEGORY="${{ github.event.inputs.art_style || 'general' }}"

mkdir -p .logs/image-generation .logs/content-processing

echo "Using prompt: $OPTIMIZED_PROMPT"
echo "MCP services: $MCP_SERVICES"
echo "Content category: $CONTENT_CATEGORY"

# MCPサービスを順番に試行
IFS=',' read -ra SERVICES <<< "$MCP_SERVICES"
SUCCESS=false

for service in "${SERVICES[@]}"; do
  echo "🔄 Trying MCP service: $service"
  
  if timeout 180 claude --mcp-config ~/.claude/mcp-kamuicode.json --mcp "$service" --prompt "$OPTIMIZED_PROMPT" > ".logs/image-generation/${service}-result.json" 2>&1; then
    echo "✅ Success with $service"
    SUCCESS=true
    
    # 結果からフルURLを抽出（省略・短縮しない）
    FULL_URL=$(jq -r '.image_url // .url // .file_path // "none"' ".logs/image-generation/${service}-result.json" 2>/dev/null || echo "none")
    
    if [ "$FULL_URL" != "none" ]; then
      echo "🔗 Generated content URL: ${FULL_URL:0:100}..."
      echo "CONTENT_URL=$FULL_URL" >> $GITHUB_ENV
      echo "USED_SERVICE=$service" >> $GITHUB_ENV
      break
    fi
  else
    echo "❌ Failed with $service, trying next..."
    continue
  fi
done

if [ "$SUCCESS" = false ]; then
  echo "❌ All MCP services failed"
  exit 1
fi

# 3イテレーション品質向上プロセス開始
echo ""
echo "🚀 Starting 3-iteration quality enhancement process..."

for ITERATION in 1 2 3; do
  echo ""
  echo "═══════════════════════════════════════"
  echo "🔄 ITERATION $ITERATION/3"
  echo "═══════════════════════════════════════"
  
  # 統合ダウンロード・品質向上処理
  if ./script/content-download-manager.sh \\
    --url "$CONTENT_URL" \\
    --type image \\
    --iteration "$ITERATION" \\
    --category "$CONTENT_CATEGORY" \\
    --working-dir "$(pwd)"; then
    
    echo "✅ Iteration $ITERATION completed successfully"
    
    # 品質チェック結果を確認
    if [ -f "quality_enhancement_iter${ITERATION}.json" ]; then
      QUALITY_SCORE=$(python3 -c "
import json
try:
    with open('quality_enhancement_iter${ITERATION}.json', 'r') as f:
        data = json.load(f)
    print(f\\"{data['quality_check']['score']:.1f}\\")
except:
    print('0')
")
      
      echo "📊 Quality Score: $QUALITY_SCORE/100"
      
      # 品質閾値チェック (70点以上で完了)
      if (( $(echo "$QUALITY_SCORE >= 70" | bc -l) )); then
        echo "🎉 Quality threshold met! Process completed at iteration $ITERATION"
        
        # 最終ファイルパスを記録
        ENHANCED_FILE=$(ls *_enhanced_iter${ITERATION}.* 2>/dev/null | head -1 || echo "")
        if [ -n "$ENHANCED_FILE" ]; then
          FINAL_PATH="$(pwd)/$ENHANCED_FILE"
          FINAL_HOME_PATH="${FINAL_PATH/#$HOME/~}"
          echo "FINAL_IMAGE_PATH=$FINAL_HOME_PATH" >> $GITHUB_ENV
          echo "QUALITY_SCORE=$QUALITY_SCORE" >> $GITHUB_ENV
          echo "ITERATIONS_COMPLETED=$ITERATION" >> $GITHUB_ENV
        fi
        break
      else
        echo "⚠️ Quality score below threshold (70). Continuing to next iteration..."
      fi
    else
      echo "⚠️ Quality check file not found, continuing..."
    fi
  else
    echo "❌ Iteration $ITERATION failed"
    if [ "$ITERATION" -eq 3 ]; then
      echo "❌ All 3 iterations failed"
      exit 1
    fi
  fi
done

echo ""
echo "🎯 3-Iteration Quality Process Summary:"
echo "   - Original URL: ${CONTENT_URL:0:60}..."
echo "   - MCP Service: $USED_SERVICE"
echo "   - Final Quality: ${QUALITY_SCORE:-'Unknown'}/100"
echo "   - Iterations: ${ITERATIONS_COMPLETED:-3}/3"
echo "   - Final Path: ${FINAL_IMAGE_PATH:--}"

echo ""
echo "✅ AI content generation with quality enhancement completed!"
                        '''
                    },
                    {
                        'name': 'Upload generated images',
                        'uses': 'actions/upload-artifact@v4',
                        'with': {
                            'name': 'generated-images-${{ github.run_number }}',
                            'path': '.logs/image-generation/',
                            'retention-days': 14
                        }
                    },
                    {
                        'name': 'Create summary report',
                        'run': '''
echo "📋 Creating generation summary..."

cat > image-generation-report.md << EOF
# 🎨 AI画像生成レポート

## 生成設定
- **プロンプト**: ${{ github.event.inputs.main_prompt }}
- **アートスタイル**: ${{ github.event.inputs.art_style }}
- **品質レベル**: ${{ github.event.inputs.quality_level }}
- **縦横比**: ${{ github.event.inputs.aspect_ratio }}
- **生成枚数**: ${{ github.event.inputs.image_count }}

## 実行結果
- **使用MCPサービス**: $USED_SERVICE
- **最適化プロンプト**: ${{ needs.setup-dynamic-execution.outputs.optimized-prompt }}
- **生成画像パス**: $IMAGE_PATH
- **実行時刻**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## 生成された画像
画像は上記のArtifactsからダウンロードできます。

---
🤖 Generated by Dynamic Modal Image Generation System
EOF

echo "✅ Report created: image-generation-report.md"
                        '''
                    }
                ]
            }
        }
    }
    
    # YAMLファイルとして出力
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(workflow, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"✅ Generated workflow file: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate dynamic inputs for workflow')
    parser.add_argument('--template', required=True, help='Template file path')
    parser.add_argument('--output', required=True, help='Output workflow file path')
    
    args = parser.parse_args()
    
    # テンプレート読み込み
    dynamic_spec, template_data = load_template_spec(args.template)
    
    if not dynamic_spec or not template_data:
        print("❌ Failed to load template specification")
        sys.exit(1)
    
    # GitHub Actions inputs生成
    github_inputs = generate_github_actions_inputs(dynamic_spec)
    
    if not github_inputs:
        print("⚠️ No dynamic inputs found, creating basic workflow")
        github_inputs = {
            'basic_prompt': {
                'description': 'Basic prompt for generation',
                'required': True,
                'type': 'string',
                'default': 'high quality image'
            }
        }
    
    print(f"🎯 Generated {len(github_inputs)} dynamic inputs:")
    for name, spec in github_inputs.items():
        print(f"  - {name}: {spec.get('type', 'string')}")
    
    # ワークフローファイル生成
    generate_workflow_file(template_data, github_inputs, args.output)
    
    print("🎉 Dynamic inputs generation completed!")

if __name__ == '__main__':
    main()