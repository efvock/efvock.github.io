function toggleContent(element) {
    const content = element.nextElementSibling;
    if (content.style.display === "none" || content.style.display === "") {
        content.style.display = "block";
        const tc = element.textContent;
        const sl = tc.trim().slice(2);
        element.textContent = "🔽 " + sl;
    } else {
        content.style.display = "none";
        const tc = element.textContent;
        const sl = tc.trim().slice(2);
        element.textContent = "▶️ " + sl;
    }
}