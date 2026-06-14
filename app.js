async function generateSpeech() {
  const apiKey = document.getElementById("apiKey").value.trim();
  const statusDiv = document.getElementById("status");
  const playBtn = document.getElementById("playBtn");

  if (!apiKey) {
    statusDiv.innerText = "GeminiのAPIキーを入力してください。";
    return;
  }

  statusDiv.innerText = "Geminiが感情を込めて声を生成中...";
  playBtn.disabled = true;

  // AI Studioに送るプロンプト（セリフと、あの空気感を再現するための演技指導）
  const promptText = `
以下のセリフを、45歳でがんを告知された男の、生々しい絶望に満ちた声で喋ってください。
ショックで声は掠れ、消え入りそうな「ささやき声（ウィスパーボイス）」で、言葉と言葉の間に深い絶望の「ため」や「間（ま）」をたっぷり設けて、ぽつり、ぽつりと呟くように演じてください。絶対にハキハキと読まないでください。

セリフ：
俺が、がん。
しかも、喉に。
45歳で。
嘘やろ。
  `.trim();

  // Gemini API (v1beta) のマルチモーダル音声生成エンドポイント
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;

  const requestBody = {
    contents: [
      {
        parts: [{ text: promptText }],
      },
    ],
    generationConfig: {
      // 応答に「AUDIO（音声）」を指定するのが最大のポイントです
      responseModalities: ["AUDIO"],
      speechConfig: {
        voiceConfig: {
          // prebuiltVoiceConfigで男性の声を指定（Aoede:女性, Charon:男性, Fenrir:男性, Puck:男性など）
          prebuiltVoiceConfig: {
            voiceName: "Puck",
          },
        },
      },
    },
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.error?.message || "Gemini APIエラーが発生しました。"
      );
    }

    const data = await response.json();

    // レスポンスから音声のBase64データを抽出
    const candidate = data.candidates?.[0];
    const audioPart = candidate?.content?.parts?.find(
      (part) => part.inlineData && part.inlineData.mimeType.startsWith("audio/")
    );

    if (!audioPart) {
      throw new Error("音声データが返されませんでした。プロンプトを見直してください。");
    }

    statusDiv.innerText = "";

    // 取得したBase64（通常はaudio/mp3またはaudio/aac）をブラウザで再生
    const base64Audio = audioPart.inlineData.data;
    const mimeType = audioPart.inlineData.mimeType;
    const audioUrl = `data:${mimeType};base64,${base64Audio}`;
    
    const audio = new Audio(audioUrl);
    audio.play();
  } catch (error) {
    console.error(error);
    statusDiv.innerText = `エラー: ${error.message}`;
  } finally {
    playBtn.disabled = false;
  }
}
