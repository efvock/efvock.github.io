---
layout: null
---
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSONコピー</title>
</head>

<body>

    <div class="container">
        <button id="copyBtn" class="btn-responsive">JSONをコピー</button>
    </div>

    <script>
        // 💡 データの埋め込みだけは、Jekyllが処理できるこのHTML内で行う
        // グローバル変数としてブラウザに記憶させます（クォートは不要）
        window.jekyllSiteData = {{ site.data | jsonify }};
    </script>

    <script src="{{ site.baseurl }}/assets/js/copy-json.js"></script>
</body>

</html>
