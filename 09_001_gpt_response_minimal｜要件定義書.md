# 09-001-gpt-response-minimal｜要件定義書

## 0. メタ情報
- **リポジトリ名**: `09-001-gpt-response-minimal`
- **概要（英語）**: Chapter 9 pre-step: minimal GPT response test—call the API once and print output; groundwork for the news bulletin system.
- **目的**: ニュース掲示板システムの前段階として、**OpenAI API からの応答を 1 回取得して標準出力に表示できること**を最小要件として検証する。
- **想定読者**: Raspberry Pi と Python の超初学者、書籍読者、レビュー担当者。

---

## 1. スコープ
### 1.1 本プロジェクトで実施すること（In Scope）
- `.env` から **OPENAI_API_KEY** を読み込み、OpenAI ChatGPT (例: `gpt-5-mini`) に 1 回問い合わせる Python スクリプトを実装。
- 応答テキストを **標準出力に表示**。
- 失敗時に **エラーメッセージをユーザーに分かる形で表示**。
- **トークン使用量**（取得可能な範囲）を表示。
- 実行手順（セットアップ～実行まで）の Markdown 掲載。

### 1.2 スコープ外（Out of Scope）
- ニュース API 連携、要約ロジック、キュー/スケジューリング、自動実行（cron/systemd）。
- LCD 表示、GUI、Web UI、DB 保存、キャッシュ。
- 複数回呼び出し、ストリーミング出力、マルチモーダル（音声/画像）対応。
- 高度な例外処理やリトライ・レート制御の最適化。

---

## 2. 成果物
- **Python スクリプト**: `api_test.py`（または `main.py` の別名を許容）
- **環境設定ファイル**: `.env`（`.gitignore` で除外）
- **要件定義書**（本ドキュメント）
- **README.md（簡易）**: セットアップと実行手順、トラブルシュートの最小記載

---

## 3. 利用者ストーリー
- **初学者として**、API キーを安全に設定し、1 回のリクエストで応答を得られることを確認したい。
- **著者/レビュワーとして**、読者が手順通りに実行すれば再現できることを確認したい。

---

## 4. 機能要件（FR）
- **FR-1**: `.env` から `OPENAI_API_KEY` を読み込む（`python-dotenv` を使用）。
- **FR-2**: OpenAI Chat Completions API を呼び出し、**1 回**メッセージを送信する。
  - モデルは **`gpt-5-mini`** を既定（将来変更容易な構造）。
  - 入力メッセージ: 簡易な挨拶または説明（例: 「Raspberry Pi について一言で」）。
- **FR-3**: 応答メッセージ本文を標準出力に表示する。
- **FR-4**: 可能であれば `usage` 情報（total/prompt/completion tokens）を表示する。
- **FR-5**: 例外発生時は **例外種別とヒント**（API キー、ネットワーク、モデル名など）を表示する。

---

## 5. 非機能要件（NFR）
- **NFR-1（可搬性）**: Raspberry Pi OS（Bookworm 相当）と一般的な Linux/Windows/macOS で動作。
- **NFR-2（セキュリティ）**: API キーをソースコードにベタ書きしない。`.env` を `.gitignore` に登録。
- **NFR-3（シンプルさ）**: 初学者向けに依存関係を最小化（`openai`, `python-dotenv`, `requests` 程度）。
- **NFR-4（再現性）**: `requirements.txt` を提供。
- **NFR-5（可読性）**: コードは 100 行未満、関数/Docstring を付与。

---

## 6. 前提条件・依存関係
- Raspberry Pi（または任意の PC）に **Python 3.9+**。
- OpenAI アカウント・有効な **API キー**。
- ネットワーク接続（443/TLS）。

---

## 7. 環境構築・実行手順（最小）
```bash
# 任意の作業ディレクトリで
python3 -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install openai python-dotenv requests

# .env を作成
printf "OPENAI_API_KEY=sk-..." > .env
chmod 600 .env  # Linux/macOS 推奨

# 実行
python3 api_test.py
```

---

## 8. エラーハンドリング方針
- API キー未設定/無効 → 「`.env`/環境変数の確認」を案内。
- ネットワーク障害 → DNS/プロキシ/ファイアウォール確認のヒントを表示。
- モデル名エラー → 利用可能モデルへの変更提案（例: `gpt-4.1-mini` など）。
- レート制限/支払い設定 → ダッシュボードの Billing/Usage を案内。

---

## 9. 受け入れ基準（DoD）
- **AC-1**: `.env` の API キー設定のみで、**1 回の応答を標準出力に表示**できる。
- **AC-2**: 例外時に **利用者が自己解決を試みられるヒント**が表示される。
- **AC-3**: `README.md` の手順通りに **初学者が 10 分以内**に実行できる。
- **AC-4**: `.env` が Git 管理対象外である。

---

## 10. リポジトリ構成（案）
```
09-001-gpt-response-minimal/
├── api_test.py
├── README.md
├── requirements.txt
├── .gitignore
└── docs/
    └── requirements.md  # 本ドキュメント（生成物）
```

---

## 11. セキュリティ・運用ガイド（最小）
- `.env` は **ローカル限定**。チーム共有時は **秘密情報管理ツール**（例: 1Password, Bitwarden）推奨。
- 公開リポジトリでは **絶対に API キーをコミットしない**（Git 履歴も含む）。
- 万一漏洩の疑いがある場合は **速やかにキーをローテーション**。

---

## 12. ライセンス
- 書籍付随サンプルとして **MIT** を推奨（必要に応じて調整）。

---

## 13. 将来拡張への接続（参考・非スコープ）
- ニュース API 連携、要約テンプレート化、LCD 出力、タスクスケジューラ連携。
- 例外パターンごとのリトライ/バックオフ、ストリーミング出力対応。

---

## 付録 A: `api_test.py` 仕様（最小）
- **引数**: なし（ハードコードの 1 プロンプト）。
- **処理**:
  1. `.env` 読み込み → `OPENAI_API_KEY` 検証。
  2. `gpt-5-mini` に **system + user** の 2 メッセージで問い合わせ。
  3. 応答を標準出力に表示。`usage` が取得できる場合は併せて表示。
  4. 例外時は要因別メッセージを表示し、終了コード ≠ 0 を返す。
- **終了コード**: 正常 `0`、異常 `1`。

---

## 付録 B: `.gitignore` 例
```
# Python
__pycache__/
*.pyc
.env
.env.*
.env.local
venv/
env/
.idea/
.vscode/
```

