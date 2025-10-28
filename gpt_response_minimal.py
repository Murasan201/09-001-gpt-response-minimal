
import os
from dotenv import load_dotenv
from openai import OpenAI

# 環境変数を読み込み
load_dotenv()

# OpenAI クライアントを初期化
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def test_chatgpt_api():
    """ChatGPT APIの動作テスト"""
    try:
        print("ChatGPT APIに接続しています...")

        # 簡単なプロンプトでテスト
        # gpt-5-miniは推論モデルのため、reasoning_tokensを含めた十分なトークン数が必要
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": "こんにちは！Raspberry Piについて一言で教えてください。"}
            ],
            max_completion_tokens=500  # 推論モデルのため、推論トークン + 応答トークンの合計を考慮
        )

        # レスポンスを表示
        message = response.choices[0].message.content
        print("\nChatGPTからの応答:")
        if message:
            print(message)
        else:
            print("（応答内容が空です）")
        print("\nAPIの接続テストが成功しました！")

        # 利用料金情報を表示
        print(f"使用トークン数: {response.usage.total_tokens}")
        print(f"入力トークン数: {response.usage.prompt_tokens}")
        print(f"出力トークン数: {response.usage.completion_tokens}")

        # 推論モデルの詳細情報
        if hasattr(response.usage, 'completion_tokens_details'):
            details = response.usage.completion_tokens_details
            if hasattr(details, 'reasoning_tokens'):
                print(f"推論トークン数: {details.reasoning_tokens}")

        print(f"終了理由: {response.choices[0].finish_reason}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("APIキーや設定を確認してください。")

if __name__ == "__main__":
    test_chatgpt_api()
