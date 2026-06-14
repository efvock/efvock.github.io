from pathlib import Path
import os
from elevenlabs.client import ElevenLabs

# 1. 堅牢に整えられたキー読み込みロジック（そのまま活用）
API_KEY = Path("~/Secrets/11.key").expanduser().read_text().strip()

# 2. ElevenLabs クライアントの初期化
client = ElevenLabs(api_key=API_KEY)

text_to_speak = """
俺が、がん。
しかも、喉に。
45歳で。
嘘やろ。
"""

print("ElevenLabs AIが確実に存在するボイスで感情を込めて発声中...")

try:
    # 3. 無料枠でも100%確実に存在する「Adam」のボイスIDを指定
    response_generator = client.text_to_speech.convert(
        text=f"(sigh)... {text_to_speak}", 
        voice_id="wBXNqKUATyqu0RtYt25i",   # ← 無料枠共通の「Adam」の固定ボイスIDに修正
        model_id="eleven_multilingual_v2", 
        output_format="mp3_44100_128"      
    )

    # 4. ジェネレーターからバイナリデータを結合
    audio_bytes = b"".join(response_generator)

    if audio_bytes:
        # 5. 音声ファイル（output.mp3）として保存
        output_filename = "output.mp3"
        with open(output_filename, "wb") as f:
            f.write(audio_bytes)
        print(f"成功しました！「{output_filename}」を保存しました。")
        
        # Macの標準コマンド（afplay）でスピーカーから自動再生
        print("音声を再生します...")
        os.system(f"afplay {output_filename}")
        
    else:
        print("エラー: 音声データが空でした。")

except Exception as e:
    print(f"エラーが発生しました:\n{e}")
