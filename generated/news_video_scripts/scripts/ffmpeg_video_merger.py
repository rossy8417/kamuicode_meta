#!/usr/bin/env python3
"""
FFmpegを使用した動画結合・編集スクリプト

このスクリプトは、複数の動画ファイルを結合し、
音声トラックの追加、BGMのミックスなどを行います。

依存関係:
- Python 3.6+
- imageio-ffmpeg または システムのFFmpeg

主な機能:
- 動画の結合
- 音声トラックの追加
- BGMのミックス（音量調整付き）
- 無音トラックの生成
- トランスコーディング
"""

import os
import subprocess
import json
from typing import List, Dict, Optional, Tuple
import tempfile
import shutil


class FFmpegVideoEditor:
    """FFmpegを使用した動画編集クラス"""
    
    def __init__(self, ffmpeg_path: Optional[str] = None):
        """
        Args:
            ffmpeg_path: FFmpegの実行ファイルパス（Noneの場合は自動検出）
        """
        if ffmpeg_path:
            self.ffmpeg = ffmpeg_path
        else:
            self.ffmpeg = self._find_ffmpeg()
        
        # FFmpegの存在確認
        if not self._check_ffmpeg():
            raise RuntimeError("FFmpegが見つかりません。インストールしてください。")
    
    def _find_ffmpeg(self) -> str:
        """FFmpegのパスを自動検出"""
        try:
            import imageio_ffmpeg
            return imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError:
            # システムのFFmpegを使用
            return "ffmpeg"
    
    def _check_ffmpeg(self) -> bool:
        """FFmpegが利用可能か確認"""
        try:
            subprocess.run([self.ffmpeg, "-version"], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def get_video_info(self, video_path: str) -> Dict:
        """
        動画の情報を取得
        
        Args:
            video_path: 動画ファイルパス
        
        Returns:
            動画情報の辞書（duration, fps, resolution等）
        """
        cmd = [
            self.ffmpeg, "-i", video_path, "-hide_banner",
            "-print_format", "json", "-show_streams"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 簡易的な情報抽出
        info = {
            'duration': None,
            'fps': None,
            'resolution': None,
            'has_audio': False
        }
        
        # 出力から情報を抽出
        stderr_lines = result.stderr.split('\n')
        for line in stderr_lines:
            if 'Duration:' in line:
                duration_str = line.split('Duration: ')[1].split(',')[0]
                # HH:MM:SS.ff形式を秒に変換
                parts = duration_str.split(':')
                if len(parts) == 3:
                    h, m, s = parts
                    info['duration'] = int(h) * 3600 + int(m) * 60 + float(s)
            elif 'Stream' in line and 'Video:' in line:
                # 解像度を抽出
                if 'x' in line:
                    for part in line.split(','):
                        if 'x' in part and part.strip()[0].isdigit():
                            info['resolution'] = part.strip().split()[0]
            elif 'Stream' in line and 'Audio:' in line:
                info['has_audio'] = True
        
        return info
    
    def add_silent_audio(self, video_path: str, output_path: str, 
                        duration: Optional[float] = None) -> bool:
        """
        動画に無音の音声トラックを追加
        
        Args:
            video_path: 入力動画パス
            output_path: 出力動画パス
            duration: 無音の長さ（Noneの場合は動画の長さに合わせる）
        
        Returns:
            成功した場合True
        """
        cmd = [
            self.ffmpeg, "-i", video_path,
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-c:v", "copy", "-c:a", "aac",
            "-shortest", output_path, "-y"
        ]
        
        if duration:
            cmd.extend(["-t", str(duration)])
        
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    
    def concatenate_videos(self, video_paths: List[str], output_path: str,
                          reencode: bool = False) -> bool:
        """
        複数の動画を結合
        
        Args:
            video_paths: 結合する動画のパスリスト
            output_path: 出力動画パス
            reencode: 再エンコードするか（False=高速だが互換性に注意）
        
        Returns:
            成功した場合True
        """
        # 一時的な結合リストファイルを作成
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', 
                                        delete=False) as f:
            for video_path in video_paths:
                f.write(f"file '{os.path.abspath(video_path)}'\n")
            concat_file = f.name
        
        try:
            if reencode:
                # 再エンコードして結合（より互換性が高い）
                inputs = []
                for video in video_paths:
                    inputs.extend(["-i", video])
                
                cmd = [self.ffmpeg] + inputs + [
                    "-filter_complex", 
                    f"concat=n={len(video_paths)}:v=1:a=1[outv][outa]",
                    "-map", "[outv]", "-map", "[outa]",
                    "-c:v", "libx264", "-c:a", "aac",
                    output_path, "-y"
                ]
            else:
                # コピーモードで結合（高速）
                cmd = [
                    self.ffmpeg, "-f", "concat", "-safe", "0",
                    "-i", concat_file, "-c", "copy",
                    output_path, "-y"
                ]
            
            result = subprocess.run(cmd, capture_output=True)
            return result.returncode == 0
            
        finally:
            # 一時ファイルを削除
            if os.path.exists(concat_file):
                os.remove(concat_file)
    
    def mix_audio_with_bgm(self, video_path: str, bgm_path: str, 
                          output_path: str, bgm_volume: float = 0.1) -> bool:
        """
        動画にBGMをミックス
        
        Args:
            video_path: 入力動画パス
            bgm_path: BGM音声パス
            output_path: 出力動画パス
            bgm_volume: BGMの音量（0.0-1.0）
        
        Returns:
            成功した場合True
        """
        # 動画の情報を取得
        video_info = self.get_video_info(video_path)
        
        if video_info['has_audio']:
            # 既存の音声とBGMをミックス
            cmd = [
                self.ffmpeg, "-i", video_path,
                "-stream_loop", "-1", "-i", bgm_path,
                "-filter_complex", 
                f"[1:a]volume={bgm_volume}[bgm];"
                f"[0:a][bgm]amerge=inputs=2[mixed]",
                "-map", "0:v", "-map", "[mixed]",
                "-ac", "2", "-c:v", "copy", "-c:a", "aac",
                "-shortest", output_path, "-y"
            ]
        else:
            # BGMのみを追加
            cmd = [
                self.ffmpeg, "-i", video_path,
                "-stream_loop", "-1", "-i", bgm_path,
                "-filter_complex", f"[1:a]volume={bgm_volume}[bgm]",
                "-map", "0:v", "-map", "[bgm]",
                "-c:v", "copy", "-c:a", "aac",
                "-shortest", output_path, "-y"
            ]
        
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    
    def trim_video(self, video_path: str, output_path: str,
                   start_time: float = 0, duration: Optional[float] = None) -> bool:
        """
        動画をトリミング
        
        Args:
            video_path: 入力動画パス
            output_path: 出力動画パス
            start_time: 開始時間（秒）
            duration: 長さ（秒）、Noneの場合は最後まで
        
        Returns:
            成功した場合True
        """
        cmd = [
            self.ffmpeg, "-i", video_path,
            "-ss", str(start_time)
        ]
        
        if duration:
            cmd.extend(["-t", str(duration)])
        
        cmd.extend([
            "-c", "copy", output_path, "-y"
        ])
        
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    
    def create_news_video(self, components: Dict[str, str], 
                         output_path: str) -> bool:
        """
        ニュース動画を作成する統合メソッド
        
        Args:
            components: 動画コンポーネントの辞書
                - title_video: タイトル動画
                - main_video: メイン動画
                - bgm: BGM音声
                - narration: ナレーション音声（オプション）
            output_path: 出力パス
        
        Returns:
            成功した場合True
        """
        temp_files = []
        
        try:
            # 1. タイトルを5秒にトリミング
            if 'title_video' in components:
                title_trimmed = output_path.replace('.mp4', '_title_trim.mp4')
                self.trim_video(components['title_video'], title_trimmed, 
                              duration=5)
                temp_files.append(title_trimmed)
                
                # タイトルに無音を追加
                title_with_audio = output_path.replace('.mp4', '_title_audio.mp4')
                self.add_silent_audio(title_trimmed, title_with_audio)
                temp_files.append(title_with_audio)
            
            # 2. 動画を結合
            videos_to_concat = []
            if 'title_video' in components:
                videos_to_concat.append(title_with_audio)
            if 'main_video' in components:
                videos_to_concat.append(components['main_video'])
            
            if len(videos_to_concat) > 1:
                merged = output_path.replace('.mp4', '_merged.mp4')
                self.concatenate_videos(videos_to_concat, merged)
                temp_files.append(merged)
            else:
                merged = videos_to_concat[0] if videos_to_concat else None
            
            # 3. BGMを追加
            if merged and 'bgm' in components:
                self.mix_audio_with_bgm(merged, components['bgm'], 
                                      output_path, bgm_volume=0.08)
            else:
                # BGMなしでコピー
                shutil.copy2(merged, output_path)
            
            return True
            
        except Exception as e:
            print(f"エラー: {e}")
            return False
            
        finally:
            # 一時ファイルをクリーンアップ
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)


def example_usage():
    """使用例"""
    editor = FFmpegVideoEditor()
    
    # 動画情報を取得
    info = editor.get_video_info("sample.mp4")
    print(f"動画情報: {info}")
    
    # 動画を結合
    videos = ["intro.mp4", "main.mp4", "outro.mp4"]
    editor.concatenate_videos(videos, "combined.mp4")
    
    # BGMを追加
    editor.mix_audio_with_bgm("combined.mp4", "bgm.wav", 
                            "final.mp4", bgm_volume=0.1)
    
    # ニュース動画を作成
    components = {
        'title_video': 'title.mp4',
        'main_video': 'anchor.mp4',
        'bgm': 'news_bgm.wav'
    }
    editor.create_news_video(components, "news_final.mp4")


if __name__ == "__main__":
    example_usage()