<button id="copyBtn">JSONをコピー</button>

<script>
    document.getElementById('copyBtn').addEventListener('click', async () => {
        // Jekyllの機能で、YAMLデータを自動的にJSON文字列に変換してここに埋め込む
        const jsonText = '{{ site.data.mydata | jsonify | escape_js }}';

        await navigator.clipboard.writeText(jsonText);
        alert("コピーしました！");
    });
</script>
