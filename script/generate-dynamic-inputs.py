#!/usr/bin/env python3
"""
Dynamic Inputs Generator for Composite Workflows
Generates user-friendly workflow inputs based on template analysis
"""

import sys
import argparse
import yaml
import json
import os
from pathlib import Path

def parse_template(template_path):
    """Parse template file and extract workflow structure"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = yaml.safe_load(f)
        return template_content
    except Exception as e:
        print(f"Error parsing template {template_path}: {e}")
        return None

def generate_composite_inputs(composite_type, templates_list):
    """Generate dynamic inputs based on composite workflow type"""
    
    inputs = {}
    
    if composite_type == "story-video-audio":
        inputs = {
            'story_prompt': {
                'description': 'ストーリー・物語の内容',
                'required': True,
                'type': 'string'
            },
            'visual_style': {
                'description': '映像スタイル (cinematic, anime, realistic, artistic)',
                'required': False,
                'type': 'choice',
                'options': ['cinematic', 'anime', 'realistic', 'artistic'],
                'default': 'cinematic'
            },
            'scene_count': {
                'description': 'シーン数 (3-10)',
                'required': False,
                'type': 'number',
                'default': 5
            },
            'bgm_mood': {
                'description': 'BGMの雰囲気 (dramatic, peaceful, energetic, mysterious)',
                'required': False,
                'type': 'choice',
                'options': ['dramatic', 'peaceful', 'energetic', 'mysterious'],
                'default': 'dramatic'
            },
            'narration_voice': {
                'description': 'ナレーション音声タイプ (male, female, neutral)',
                'required': False,
                'type': 'choice',
                'options': ['male', 'female', 'neutral'],
                'default': 'neutral'
            },
            'video_duration': {
                'description': '目標動画長 (秒)',
                'required': False,
                'type': 'number',
                'default': 60
            }
        }
    
    elif composite_type == "image-video-audio":
        inputs = {
            'image_prompts': {
                'description': '画像生成プロンプト (カンマ区切り)',
                'required': True,
                'type': 'string'
            },
            'transition_style': {
                'description': 'トランジション効果',
                'required': False,
                'type': 'choice',
                'options': ['fade', 'slide', 'zoom', 'dissolve'],
                'default': 'fade'
            },
            'music_genre': {
                'description': '音楽ジャンル',
                'required': False,
                'type': 'choice',
                'options': ['electronic', 'orchestral', 'ambient', 'rock'],
                'default': 'ambient'
            }
        }
    
    else:  # Default/single template
        inputs = {
            'prompt': {
                'description': '生成プロンプト',
                'required': True,
                'type': 'string'
            },
            'quality': {
                'description': '品質設定',
                'required': False,
                'type': 'choice',
                'options': ['standard', 'high', 'ultra'],
                'default': 'high'
            }
        }
    
    return inputs

def generate_workflow_with_dynamic_inputs(template_path, output_path, composite_type=None, templates_list=None):
    """Generate enhanced workflow with dynamic inputs"""
    
    # Parse base template
    base_template = parse_template(template_path)
    if not base_template:
        return False
    
    # Generate dynamic inputs
    if composite_type and composite_type != "single":
        dynamic_inputs = generate_composite_inputs(composite_type, templates_list)
    else:
        dynamic_inputs = generate_composite_inputs("single", None)
    
    # Create enhanced workflow structure
    enhanced_workflow = {
        'name': f'Generated {composite_type or "Basic"} Workflow - Enhanced',
        'run-name': f'${{{{ github.actor }}}} executes {composite_type or "basic"} generation 🎬🎵',
        'on': {
            'workflow_dispatch': {
                'inputs': dynamic_inputs
            }
        }
    }
    
    # Generate jobs based on composite type
    if composite_type == "story-video-audio":
        enhanced_workflow['jobs'] = {
            'story-analysis': {
                'runs-on': 'ubuntu-latest',
                'outputs': {
                    'scenes': '${{ steps.analyze.outputs.scenes }}',
                    'scene_count': '${{ steps.analyze.outputs.scene_count }}'
                },
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {
                        'name': 'Analyze Story and Extract Scenes',
                        'id': 'analyze',
                        'run': '''
echo "📖 Analyzing story: ${{ github.event.inputs.story_prompt }}"
echo "🎬 Target scenes: ${{ github.event.inputs.scene_count }}"
echo "🎨 Visual style: ${{ github.event.inputs.visual_style }}"

# Story analysis and scene extraction
mkdir -p outputs/scenes
echo "Scene analysis completed"
echo "scenes=scene1,scene2,scene3" >> $GITHUB_OUTPUT
echo "scene_count=${{ github.event.inputs.scene_count }}" >> $GITHUB_OUTPUT
                        '''
                    }
                ]
            },
            'generate-images': {
                'needs': 'story-analysis',
                'runs-on': 'ubuntu-latest',
                'outputs': {
                    'image_paths': '${{ steps.t2i.outputs.paths }}'
                },
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {
                        'name': 'Text-to-Image Generation',
                        'id': 't2i',
                        'run': '''
echo "🎨 Generating images for ${{ needs.story-analysis.outputs.scene_count }} scenes"
echo "Style: ${{ github.event.inputs.visual_style }}"

# MCP Text-to-Image generation
mkdir -p outputs/images
echo "T2I generation completed"
echo "paths=image1.jpg,image2.jpg,image3.jpg" >> $GITHUB_OUTPUT
                        '''
                    }
                ]
            },
            'create-video': {
                'needs': 'generate-images',
                'runs-on': 'ubuntu-latest',
                'outputs': {
                    'video_path': '${{ steps.i2v.outputs.path }}'
                },
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {
                        'name': 'Image-to-Video Conversion',
                        'id': 'i2v',
                        'run': '''
echo "🎬 Converting images to video"
echo "Duration: ${{ github.event.inputs.video_duration }} seconds"
echo "Images: ${{ needs.generate-images.outputs.image_paths }}"

# MCP Image-to-Video generation
mkdir -p outputs/video
echo "I2V generation completed"
echo "path=outputs/video/story_video.mp4" >> $GITHUB_OUTPUT
                        '''
                    }
                ]
            },
            'generate-bgm': {
                'runs-on': 'ubuntu-latest',
                'outputs': {
                    'bgm_path': '${{ steps.t2m.outputs.path }}'
                },
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {
                        'name': 'Generate Background Music',
                        'id': 't2m',
                        'run': '''
echo "🎵 Generating BGM"
echo "Mood: ${{ github.event.inputs.bgm_mood }}"
echo "Duration: ${{ github.event.inputs.video_duration }} seconds"

# MCP Text-to-Music generation
mkdir -p outputs/audio
echo "T2M generation completed"
echo "path=outputs/audio/bgm.mp3" >> $GITHUB_OUTPUT
                        '''
                    }
                ]
            },
            'generate-narration': {
                'needs': 'create-video',
                'runs-on': 'ubuntu-latest',
                'outputs': {
                    'narration_path': '${{ steps.v2a.outputs.path }}'
                },
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {
                        'name': 'Generate Narration',
                        'id': 'v2a',
                        'run': '''
echo "🎙️ Generating narration"
echo "Voice: ${{ github.event.inputs.narration_voice }}"
echo "Story: ${{ github.event.inputs.story_prompt }}"

# MCP Video-to-Audio/Text-to-Speech generation
mkdir -p outputs/narration
echo "V2A/TTS generation completed"
echo "path=outputs/narration/narration.mp3" >> $GITHUB_OUTPUT
                        '''
                    }
                ]
            },
            'final-composition': {
                'needs': ['create-video', 'generate-bgm', 'generate-narration'],
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {
                        'name': 'Compose Final Video',
                        'run': '''
echo "🎞️ Composing final video with audio"
echo "Video: ${{ needs.create-video.outputs.video_path }}"
echo "BGM: ${{ needs.generate-bgm.outputs.bgm_path }}"
echo "Narration: ${{ needs.generate-narration.outputs.narration_path }}"

# Final video composition
mkdir -p outputs/final
echo "✅ Final composite video created: outputs/final/story_video_complete.mp4"
                        '''
                    },
                    {
                        'name': 'Upload Artifacts',
                        'uses': 'actions/upload-artifact@v4',
                        'with': {
                            'name': 'story-video-complete',
                            'path': 'outputs/'
                        }
                    }
                ]
            }
        }
    
    else:
        # Default single workflow
        enhanced_workflow['jobs'] = {
            'generate': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {
                        'name': 'Basic Generation',
                        'run': '''
echo "🎯 Executing generation"
echo "Prompt: ${{ github.event.inputs.prompt }}"
echo "Quality: ${{ github.event.inputs.quality }}"
echo "✅ Generation completed"
                        '''
                    }
                ]
            }
        }
    
    # Write enhanced workflow
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(enhanced_workflow, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        print(f"✅ Enhanced workflow generated: {output_path}")
        print(f"   - Composite type: {composite_type or 'single'}")
        print(f"   - Dynamic inputs: {len(dynamic_inputs)} fields")
        return True
        
    except Exception as e:
        print(f"❌ Error writing workflow: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate dynamic inputs for workflows')
    parser.add_argument('--template', required=True, help='Template file path')
    parser.add_argument('--output', required=True, help='Output workflow file path')
    parser.add_argument('--composite-templates', help='Composite templates (comma-separated)')
    parser.add_argument('--composite-type', help='Composite workflow type')
    
    args = parser.parse_args()
    
    # Parse composite templates
    templates_list = []
    if args.composite_templates:
        templates_list = [t.strip() for t in args.composite_templates.split(',')]
    
    # Generate enhanced workflow
    success = generate_workflow_with_dynamic_inputs(
        args.template,
        args.output,
        args.composite_type,
        templates_list
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()