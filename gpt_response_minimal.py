#!/usr/bin/env python3
"""
GPT応答最小テスト
OpenAI APIを使用した最小限のGPT応答テストプログラム
要件定義書: 09_001_gpt_response_minimal｜要件定義書.md
"""

# 標準ライブラリ
import os
import sys

# サードパーティライブラリ
from dotenv import load_dotenv
from openai import OpenAI

# 定数
DEFAULT_MODEL = "gpt-5-mini"  # OpenAIの推論モデル
MAX_COMPLETION_TOKENS = 500   # 推論トークン + 応答トークンの合計上限
I2C_TIMEOUT = 10              # API接続タイムアウト（秒）


def initialize_client():
    """
    OpenAI APIクライアントを初期化する

    Returns:
        OpenAI: 初期化されたOpenAIクライアント

    Raises:
        ValueError: APIキーが設定されていない場合
    """
    # .envファイルから環境変数を読み込み
    load_dotenv()

    # APIキーの取得と検証
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEYが設定されていません")

    # OpenAI クライアントを初期化
    client = OpenAI(api_key=api_key)
    return client


def test_chatgpt_api(client):
    """
    ChatGPT APIの動作テストを実行する

    Args:
        client (OpenAI): 初期化済みのOpenAIクライアント
    """
    try:
        print("ChatGPT APIに接続しています...")

        # gpt-5-mini: OpenAIの推論モデル（reasoning model）
        # - 推論プロセスにトークンを消費するため、max_completion_tokensは500以上を推奨
        # - temperatureパラメータはデフォルト値（1）のみサポート
        # - max_tokensは非サポート（max_completion_tokensを使用）
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": "こんにちは！Raspberry Piについて一言で教えてください。"}
            ],
            max_completion_tokens=MAX_COMPLETION_TOKENS  # 推論トークン + 応答トークンの合計
        )

        # 応答内容の取得と表示
        message = response.choices[0].message.content
        print("\nChatGPTからの応答:")
        if message:
            print(message)
        else:
            # 応答が空の場合（max_completion_tokensが不足している可能性）
            print("（応答内容が空です）")
            print("ヒント: max_completion_tokensの値を増やしてください")
        print("\nAPIの接続テストが成功しました！")

        # トークン使用量の表示
        print(f"\n使用トークン数: {response.usage.total_tokens}")
        print(f"入力トークン数: {response.usage.prompt_tokens}")
        print(f"出力トークン数: {response.usage.completion_tokens}")

        # 推論モデル特有の情報（reasoning_tokens）を表示
        # gpt-5-miniは推論プロセスにトークンを消費するため、この値が重要
        if hasattr(response.usage, 'completion_tokens_details'):
            details = response.usage.completion_tokens_details
            if hasattr(details, 'reasoning_tokens'):
                print(f"推論トークン数: {details.reasoning_tokens}")

        # 終了理由の表示
        # - 'stop': 正常に完了
        # - 'length': トークン制限に達して終了（max_completion_tokensを増やす必要あり）
        print(f"終了理由: {response.choices[0].finish_reason}")

    except Exception as e:
        print(f"\n[API呼び出し]エラー: {e}")
        print("\n対処方法:")
        print("1. .envファイルにOPENAI_API_KEYが正しく設定されているか確認")
        print("   例: OPENAI_API_KEY=sk-...")
        print("2. APIキーが有効か確認（OpenAI Platform: https://platform.openai.com/api-keys）")
        print("3. ネットワーク接続を確認")
        print("   ヒント: curl https://api.openai.com/v1/models")
        print("4. 詳細はTROUBLESHOOTING.mdを参照してください")
        sys.exit(1)


def main():
    """
    メイン関数：OpenAI APIクライアントを初期化してテストを実行
    """
    try:
        # OpenAI APIクライアントの初期化
        client = initialize_client()

        # API接続テストの実行
        test_chatgpt_api(client)

    except ValueError as e:
        # APIキー未設定エラー
        print(f"\n[初期化]エラー: {e}")
        print("\n対処方法:")
        print("1. プロジェクトルートに.envファイルを作成")
        print("2. 以下の形式でAPIキーを設定:")
        print("   OPENAI_API_KEY=sk-...")
        print("3. OpenAI Platformでキーを発行: https://platform.openai.com/api-keys")
        sys.exit(1)

    except Exception as e:
        # その他の予期しないエラー
        print(f"\n予期しないエラー: {e}")
        print("詳細はTROUBLESHOOTING.mdを参照してください")
        sys.exit(1)


if __name__ == "__main__":
    main()
