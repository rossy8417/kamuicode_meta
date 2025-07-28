#!/usr/bin/env python3
"""
FAL.ai アップロードヘルパー
ローカルファイルをFAL.aiにアップロードするための共通機能
"""

import os
import sys
import requests
import json
from pathlib import Path

def setup_fal_client():
    """
    FAL APIクライアントの設定を確認
    """
    fal_key = os.environ.get('FAL_KEY')
    if not fal_key:
        print("❌ FAL_KEY環境変数が設定されていません")
        return False
    
    print(f"✅ FAL APIキーが設定されています")
    return True

def upload_file(file_path):
    """
    ファイルをFAL.aiにアップロード
    
    Args:
        file_path (str): アップロードするファイルのパス
        
    Returns:
        str: アップロードされたファイルのURL、失敗時はNone
    """
    fal_key = os.environ.get('FAL_KEY')
    if not fal_key:
        print("❌ FAL_KEY環境変数が設定されていません")
        return None
    
    try:
        # ファイルサイズ確認
        file_size = os.path.getsize(file_path)
        print(f"📁 ファイルサイズ: {file_size / (1024 * 1024):.2f} MB")
        
        # FAL.ai Upload API エンドポイント
        upload_url = "https://api.fal.ai/storage/upload"
        
        headers = {
            'Authorization': f'Key {fal_key}',
        }
        
        # ファイルアップロード
        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f, 'application/octet-stream')
            }
            
            print(f"🚀 FAL.aiにアップロード中...")
            response = requests.post(upload_url, headers=headers, files=files)
        
        if response.status_code == 200:
            result = response.json()
            uploaded_url = result.get('url')
            print(f"✅ アップロード成功: {uploaded_url}")
            return uploaded_url
        else:
            print(f"❌ アップロード失敗: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ アップロードエラー: {str(e)}")
        return None

def download_file(url, local_path):
    """
    URLからファイルをダウンロード
    
    Args:
        url (str): ダウンロード元URL
        local_path (str): 保存先パス
        
    Returns:
        bool: 成功時True、失敗時False
    """
    try:
        print(f"📥 ダウンロード中: {url}")
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(local_path)
            print(f"✅ ダウンロード完了: {local_path} ({file_size} bytes)")
            return True
        else:
            print(f"❌ ダウンロード失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ダウンロードエラー: {str(e)}")
        return False

if __name__ == "__main__":
    # テスト実行
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        if setup_fal_client():
            result = upload_file(test_file)
            if result:
                print(f"テストアップロード成功: {result}")
            else:
                print("テストアップロード失敗")
    else:
        print("Usage: python3 fal_upload_helper.py <test_file_path>")