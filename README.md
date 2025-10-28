# 09-001-gpt-response-minimal

Minimal quickstart to call OpenAI's ChatGPT once and print the reply (Python + .env). This is a preparatory step for a Raspberry Pi news board project.

**Model:** `gpt-5-mini` (OpenAI's latest reasoning model)

## Setup
```bash
# Create virtual environment
python3 -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=sk-...
```
(Optional) Secure the file on Unix-like systems:
```bash
chmod 600 .env
```

## Run
```bash
python3 gpt_response_minimal.py
```

## Expected Output
```
ChatGPT APIに接続しています...

ChatGPTからの応答:
Raspberry Piは、教育やホビー向けの低価格で小型なシングルボードコンピュータです。

APIの接続テストが成功しました！
使用トークン数: 400
入力トークン数: 34
出力トークン数: 366
推論トークン数: 320
終了理由: stop
```

## Notes on gpt-5-mini (Reasoning Model)
- `gpt-5-mini` is a reasoning model that uses tokens for internal reasoning processes
- `max_completion_tokens` must account for both reasoning tokens and response tokens
- Recommended: `max_completion_tokens=500` or higher for simple queries
- `reasoning_tokens` in the output shows how many tokens were used for reasoning

## Troubleshooting
If you encounter any errors, please refer to `TROUBLESHOOTING.md` for solutions.
