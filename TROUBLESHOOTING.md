# トラブルシューティング

本ドキュメントでは、`09-001-gpt-response-minimal` プロジェクトで発生したエラーとその対策を記録します。

---

## 目次

1. [APIパラメータ関連のエラー](#apiパラメータ関連のエラー)
2. [応答内容が空の問題](#応答内容が空の問題)
3. [環境・依存関係の問題](#環境依存関係の問題)
4. [認証・ネットワークの問題](#認証ネットワークの問題)

---

## APIパラメータ関連のエラー

### エラー1: `max_tokens` パラメータがサポートされていない

**エラーメッセージ:**
```
Error code: 400 - {'error': {'message': "Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.", 'type': 'invalid_request_error', 'param': 'max_tokens', 'code': 'unsupported_parameter'}}
```

**原因:**
- `gpt-5-mini` モデルでは、`max_tokens` パラメータが廃止され、`max_completion_tokens` に変更されました
- GPT-4系からGPT-5系への移行に伴うAPI仕様の変更

**対策:**
```python
# 修正前（エラー）
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[...],
    max_tokens=100  # ❌ 古いパラメータ
)

# 修正後（正常）
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[...],
    max_completion_tokens=100  # ✅ 新しいパラメータ
)
```

**参考:**
- OpenAI公式ドキュメント: https://platform.openai.com/docs/guides/latest-model
- GPT-5系モデルでは `max_completion_tokens` の使用が必須

---

### エラー2: `temperature` パラメータの値がサポートされていない

**エラーメッセージ:**
```
Error code: 400 - {'error': {'message': "Unsupported value: 'temperature' does not support 0.7 with this model. Only the default (1) value is supported.", 'type': 'invalid_request_error', 'param': 'temperature', 'code': 'unsupported_value'}}
```

**原因:**
- `gpt-5-mini` モデルでは `temperature` パラメータがデフォルト値（1）のみサポート
- カスタム値（0.7など）は使用できない

**対策:**
```python
# 修正前（エラー）
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[...],
    temperature=0.7  # ❌ カスタム値は未サポート
)

# 修正後（正常）
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[...]
    # temperature パラメータを削除（デフォルト値1が使用される）
)
```

**注意:**
- GPT-5系モデルでは、推論モデルの特性上、temperatureのカスタマイズが制限されています
- 必要に応じてGPT-4系モデルの使用を検討してください

---

## 応答内容が空の問題

### 問題3: API応答は成功するが、応答テキストが空（推論モデル特有の問題）

**症状:**
```
ChatGPT APIに接続しています...
ChatGPTからの応答:


APIの接続テストが成功しました！
使用トークン数: 134
入力トークン数: 34
出力トークン数: 100
```

応答テキストが表示されない（空行のみ）

**デバッグログの確認:**
```
Response object: ChatCompletion(...)
Message: ChatCompletionMessage(content='', refusal=None, role='assistant', ...)
CompletionUsage(..., reasoning_tokens=100, ...)
finish_reason='length'
```

**原因:**
- **`gpt-5-mini` は推論モデル（reasoning model）** であり、推論プロセス自体にトークンを消費する
- `max_completion_tokens=100` では、**推論トークン（reasoning_tokens）だけで全て消費**され、最終的な応答テキストを生成する前にトークン制限に達している
- `finish_reason='length'` は、トークン制限により応答が途中で終了したことを示す
- `content=''` が空なのは、推論は完了したが応答テキストを出力する前にトークン制限に達したため

**推論モデルの特徴:**
- GPT-5系の一部モデル（`gpt-5-mini` など）は、内部で推論プロセスを実行してから応答を生成する
- `reasoning_tokens` には推論プロセスで使用されたトークン数が記録される
- `max_completion_tokens` は **推論トークン + 応答トークンの合計** に対する上限

**対策:**
```python
# 修正前（応答が空になる）
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[...],
    max_completion_tokens=100  # ❌ 推論だけで消費され、応答が生成されない
)

# 修正後（正常に応答が生成される）
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[...],
    max_completion_tokens=500  # ✅ 推論トークン + 応答トークンの合計を考慮
)
```

**推奨設定:**
- シンプルな質問: `max_completion_tokens=300〜500`
- 複雑な質問: `max_completion_tokens=1000〜2000`
- 長文生成: `max_completion_tokens=2000以上`

**デバッグ方法:**
```python
# レスポンス全体を確認
print(f"Response object: {response}")
print(f"Message: {response.choices[0].message}")
print(f"Content: '{response.choices[0].message.content}'")
print(f"Finish reason: {response.choices[0].finish_reason}")

# 推論トークンの確認
if hasattr(response.usage, 'completion_tokens_details'):
    details = response.usage.completion_tokens_details
    if hasattr(details, 'reasoning_tokens'):
        print(f"Reasoning tokens: {details.reasoning_tokens}")
```

**重要な確認ポイント:**
- `finish_reason='length'` → トークン制限で終了（`max_completion_tokens` を増やす）
- `finish_reason='stop'` → 正常に完了
- `reasoning_tokens` の値 → 推論にどれだけトークンを使用したか
- `content` が空 → 推論後の応答生成前にトークン制限に達した

**参考:**
- OpenAI推論モデル公式ドキュメント: https://platform.openai.com/docs/guides/reasoning

---

## 環境・依存関係の問題

### 問題4: Pylanceの import 警告

**警告メッセージ:**
```
⚠ [Line 3:6] インポート "dotenv" を解決できませんでした (Pylance)
⚠ [Line 4:6] インポート "openai" を解決できませんでした (Pylance)
```

**原因:**
- VS CodeのPylanceが仮想環境のパッケージを認識していない
- IDEの設定問題（実行には影響なし）

**対策:**
1. **VS Codeで仮想環境を選択:**
   - `Ctrl+Shift+P` → "Python: Select Interpreter"
   - `./env/bin/python` を選択

2. **仮想環境の確認:**
   ```bash
   which python3  # 仮想環境のパスが表示されるか確認
   pip list       # インストール済みパッケージの確認
   ```

3. **それでも解決しない場合:**
   - VS Codeを再起動
   - `.vscode/settings.json` に以下を追加:
     ```json
     {
       "python.defaultInterpreterPath": "${workspaceFolder}/env/bin/python"
     }
     ```

---

## 認証・ネットワークの問題

### エラー5: API キーが無効

**エラーメッセージ:**
```
Error code: 401 - {'error': {'message': 'Incorrect API key provided', 'type': 'invalid_request_error'}}
```

**原因:**
- `.env` ファイルにAPIキーが正しく設定されていない
- APIキーの有効期限切れ、または無効化されている

**対策:**
1. `.env` ファイルの確認:
   ```bash
   cat .env
   # OPENAI_API_KEY=sk-... が正しく設定されているか確認
   ```

2. APIキーの再発行:
   - OpenAI Platform (https://platform.openai.com/api-keys) にアクセス
   - 新しいAPIキーを生成
   - `.env` ファイルを更新

3. 環境変数の読み込み確認:
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()
   api_key = os.environ.get("OPENAI_API_KEY")
   print(f"API Key loaded: {api_key[:10]}..." if api_key else "API Key not found")
   ```

---

### エラー6: ネットワーク接続エラー

**エラーメッセージ:**
```
ConnectionError: Failed to establish a connection
```

**原因:**
- インターネット接続の問題
- ファイアウォールやプロキシの制限
- OpenAI APIサーバーの一時的な障害

**対策:**
1. **ネットワーク接続の確認:**
   ```bash
   ping 8.8.8.8
   curl https://api.openai.com/v1/models
   ```

2. **プロキシ設定（必要な場合）:**
   ```bash
   export https_proxy=http://proxy.example.com:8080
   export http_proxy=http://proxy.example.com:8080
   ```

3. **OpenAI ステータスページの確認:**
   - https://status.openai.com/

---

## 一般的なデバッグ手順

### 基本的な確認項目

1. **環境の確認:**
   ```bash
   python3 --version  # Python 3.9以上か確認
   which python3      # 仮想環境のPythonを使用しているか確認
   pip list           # 必要なパッケージがインストールされているか
   ```

2. **.env ファイルの確認:**
   ```bash
   ls -la .env        # ファイルが存在するか
   cat .env           # 内容の確認（APIキーは部分的に隠す）
   ```

3. **依存関係の再インストール:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

4. **詳細なエラーログの取得:**
   ```python
   import traceback

   try:
       # API呼び出し
   except Exception as e:
       print(f"エラー: {e}")
       traceback.print_exc()  # 詳細なスタックトレース
   ```

---

## よくある質問（FAQ）

### Q1: 仮想環境を使わずにシステム全体にインストールできますか？

**A:** 可能ですが推奨しません。仮想環境を使用することで：
- プロジェクト間の依存関係の競合を防げる
- 環境の再現性が高まる
- システムのPython環境を汚染しない

### Q2: Raspberry Pi以外（Windows/Mac）でも動作しますか？

**A:** はい、動作します。Raspberry Pi専用の機能は使用していないため、Python 3.9以上が動作する環境であればどこでも実行可能です。

### Q3: gpt-4o-miniの方が安定していますか？

**A:** GPT-4系（gpt-4o-mini）の方が現時点では多くのパラメータをサポートしており、安定しています。GPT-5系はまだ新しいモデルのため、制約が多い可能性があります。要件定義書では `gpt-5-mini` を指定していますが、動作確認にはGPT-4系の使用も検討できます。

---

## 記録の更新について

このドキュメントは継続的に更新されます。新しいエラーや解決策が見つかった場合は、以下の形式で追記してください：

```markdown
### エラーX: [エラーの簡潔な説明]

**エラーメッセージ:**
```
[実際のエラーメッセージ]
```

**原因:**
- [原因の説明]

**対策:**
[解決方法のコードや手順]

**参考:**
- [関連するドキュメントやリンク]
```

---

**最終更新:** 2025-10-28
**プロジェクト:** 09-001-gpt-response-minimal
**対象モデル:** gpt-5-mini, gpt-4o-mini
