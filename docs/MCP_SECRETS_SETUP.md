# MCP URLsをGitHub Secretsで管理する方法

## 概要
MCPサーバーのURLをワークフローファイルに直接記載する代わりに、GitHub Secretsを使用して隠蔽します。

## 設定方法

### 1. GitHub Secretsの追加

リポジトリの Settings → Secrets and variables → Actions から以下のSecretsを追加：

```
MCP_BASE_URL = https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app

MCP_T2I_GOOGLE_URL = https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/t2i/google/imagen

MCP_I2V_FAL_URL = https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/i2v/fal/minimax/hailuo-02/pro

MCP_T2M_GOOGLE_URL = https://mcp-creatify-lipsync-20250719-010824-a071b7b8-820994673238.us-central1.run.app/t2m/google/lyria
```

### 2. 推奨される方法

#### 方法1: リポジトリの設定ファイルを使用（最も簡単）
```yaml
- name: Test with repo config
  uses: anthropics/claude-code-base-action@beta
  with:
    mcp_config: ".claude/mcp-kamuicode.json"  # 既存の設定を使用
```

#### 方法2: Secretsから動的生成（URLを完全に隠蔽）
```yaml
- name: Create MCP config from secrets
  run: |
    cat > .claude/mcp-config.json << EOF
    {
      "mcpServers": {
        "t2i-google-imagen3": {
          "type": "http",
          "url": "${{ secrets.MCP_T2I_GOOGLE_URL }}"
        }
      }
    }
    EOF
```

#### 方法3: ベースURLのみSecrets化
```yaml
env:
  MCP_BASE_URL: ${{ secrets.MCP_BASE_URL }}
  
- name: Create config
  run: |
    echo '{"mcpServers": {"t2i": {"url": "'$MCP_BASE_URL'/t2i/google/imagen"}}}' > config.json
```

## セキュリティ上の注意

1. **Secretsは暗号化されて保存**されます
2. **ログには表示されません**（自動的にマスクされます）
3. **フォークされたリポジトリ**からはアクセスできません
4. **Pull Request**からのワークフローではアクセス制限があります

## メンテナンス

URLが変更された場合は、GitHub Secretsのみを更新すれば、全てのワークフローに反映されます。