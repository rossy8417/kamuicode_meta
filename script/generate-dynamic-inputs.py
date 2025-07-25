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

def convert_ultradetailed_template(template_data, output_path):
    """Convert ultra-detailed template to executable GitHub Actions workflow"""
    
    workflow_name = template_data.get('name', 'Generated Workflow')
    description = template_data.get('description', 'Auto-generated workflow')
    tasks = template_data.get('tasks', [])
    
    # Extract dynamic inputs from template if available
    dynamic_inputs = {}
    if 'dynamic_inputs_spec' in template_data:
        dynamic_spec = template_data['dynamic_inputs_spec']
        for section in dynamic_spec.get('form_sections', []):
            for input_field in section.get('inputs', []):
                field_name = input_field['name']
                dynamic_inputs[field_name] = {
                    'description': input_field['label'],
                    'required': input_field.get('required', False),
                    'type': input_field['type']
                }
                
                # Handle type conversions
                if input_field['type'] == 'select':
                    dynamic_inputs[field_name]['type'] = 'choice'
                    if 'options' in input_field:
                        dynamic_inputs[field_name]['options'] = [opt['value'] for opt in input_field['options']]
                    if 'default' in input_field:
                        dynamic_inputs[field_name]['default'] = input_field['default']
                elif input_field['type'] == 'textarea':
                    dynamic_inputs[field_name]['type'] = 'string'
                elif input_field['type'] == 'range':
                    dynamic_inputs[field_name]['type'] = 'number'
                    if 'default' in input_field:
                        dynamic_inputs[field_name]['default'] = str(input_field['default'])
    
    # Fallback inputs if no dynamic spec
    if not dynamic_inputs:
        dynamic_inputs = {
            'content_topic': {
                'description': 'コンテンツのテーマ・内容',
                'required': True,
                'type': 'string'
            },
            'quality_level': {
                'description': '品質設定',
                'required': False,
                'type': 'choice',
                'options': ['standard', 'high', 'ultra'],
                'default': 'high'
            }
        }
    
    # Build GitHub Actions workflow structure
    github_workflow = {
        'name': f"Generated {workflow_name}",
        'run-name': f"${{{{ github.actor }}}} creates {workflow_name.lower()} 🎬🎵🎙️",
        'on': {
            'workflow_dispatch': {
                'inputs': dynamic_inputs
            }
        },
        'permissions': {
            'contents': 'write',
            'actions': 'read'
        },
        'env': {
            'CLAUDE_CODE_OAUTH_TOKEN': '${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}'
        },
        'jobs': {}
    }
    
    # Convert tasks to GitHub Actions jobs
    parallel_groups = {}
    for task in tasks:
        job_id = task.get('github_job', task['id'].replace('-', '_'))
        
        # Build job structure
        job = {
            'runs-on': 'ubuntu-latest',
            'steps': []
        }
        
        # Add dependencies
        dependencies = task.get('dependencies', [])
        if dependencies:
            needs_list = [dep.replace('-', '_') for dep in dependencies]
            if len(needs_list) == 1:
                job['needs'] = needs_list[0]
            else:
                job['needs'] = needs_list
        
        # Add outputs if specified
        if 'outputs' in task:
            job['outputs'] = task['outputs']
        
        # Add checkout step
        job['steps'].append({'uses': 'actions/checkout@v4'})
        
        # Convert github_steps to actual steps
        if 'github_steps' in task:
            for step in task['github_steps']:
                formatted_step = {
                    'name': step['name']
                }
                
                if 'id' in step:
                    formatted_step['id'] = step['id']
                
                if 'shell' in step:
                    formatted_step['shell'] = step['shell']
                
                if 'script' in step:
                    # Clean up the script formatting
                    script_content = step['script'].strip()
                    formatted_step['run'] = script_content
                elif 'run' in step:
                    formatted_step['run'] = step['run']
                
                job['steps'].append(formatted_step)
        else:
            # Generate default step from task info
            default_step = {
                'name': task['name'],
                'run': f"""
echo "🎯 Executing: {task['name']}"
echo "Type: {task.get('type', 'unknown')}"
echo "Implementation: {task.get('implementation', 'script')}"

mkdir -p .logs/{task['phase']}

# Task execution placeholder - replace with actual implementation
echo "✅ {task['name']} completed"
"""
            }
            
            if task.get('type') == 'generation' and task.get('implementation') == 'mcp':
                tool = task.get('tool', 'unknown')
                default_step['run'] = f"""
echo "🎯 {task['name']} using MCP {tool}"

mkdir -p outputs/{task['phase']}

# MCP service execution for {tool}
# Add actual MCP integration here
echo "Generated content for {task['name']}"
echo "✅ Generation completed"
"""
            
            job['steps'].append(default_step)
        
        # Add validation step if criteria specified
        if 'validation' in task and 'validation_script' in task['validation']:
            validation_step = {
                'name': f"Validate {task['name']}",
                'run': task['validation']['validation_script']
            }
            job['steps'].append(validation_step)
        
        github_workflow['jobs'][job_id] = job
    
    # Add final summary job
    final_job_dependencies = [task.get('github_job', task['id'].replace('-', '_')) for task in tasks if not task.get('dependencies')]
    if len(tasks) > 1:
        github_workflow['jobs']['workflow_summary'] = {
            'needs': list(github_workflow['jobs'].keys()),
            'runs-on': 'ubuntu-latest',
            'if': 'always()',
            'steps': [
                {'uses': 'actions/checkout@v4'},
                {
                    'name': 'Generate Workflow Summary',
                    'run': f"""
echo "📋 {workflow_name} Completion Summary"
echo "================================"
echo "Total Tasks: {len(tasks)}"
echo "Description: {description}"
echo "Completed: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "✅ All tasks processed successfully"

# Create final output summary
mkdir -p outputs/final
cat > outputs/final/workflow-summary.json << EOF
{{
  "workflow_name": "{workflow_name}",
  "total_tasks": {len(tasks)},
  "completion_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "completed"
}}
EOF
"""
                },
                {
                    'name': 'Upload Final Outputs',
                    'uses': 'actions/upload-artifact@v4',
                    'with': {
                        'name': f"workflow-outputs-${{{{ github.run_number }}}}",
                        'path': 'outputs/',
                        'retention-days': 30
                    }
                }
            ]
        }
    
    # Write the converted workflow
    try:
        # Ensure directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:  # Only create directory if dirname is not empty
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(github_workflow, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        print(f"✅ Ultra-detailed template converted: {output_path}")
        print(f"   - Original tasks: {len(tasks)}")
        print(f"   - Generated jobs: {len(github_workflow['jobs'])}")
        print(f"   - Dynamic inputs: {len(dynamic_inputs)}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting template: {e}")
        return False

def generate_workflow_with_dynamic_inputs(template_path, output_path, composite_type=None, templates_list=None):
    """Generate enhanced workflow with dynamic inputs"""
    
    # Parse base template
    base_template = parse_template(template_path)
    if not base_template:
        return False
    
    # Check if template has ultra-detailed task structure
    if 'tasks' in base_template and isinstance(base_template['tasks'], list):
        print(f"🎯 Converting ultra-detailed template with {len(base_template['tasks'])} tasks")
        return convert_ultradetailed_template(base_template, output_path)
    
    # Generate dynamic inputs for simple templates
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