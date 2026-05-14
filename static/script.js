const input = document.getElementById("input");
const chat = document.getElementById("chat");

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    input.value = "";
    chat.scrollTop = chat.scrollHeight;

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });
    const data = await res.json();
    typeWriterMarkdown(data.reply, "ai");
}

function appendMessage(text, role) {
    const div = document.createElement("div");
    div.className = `message ${role}`;
    div.textContent = text;
    chat.appendChild(div);
}

// AI 打字 + Markdown
function typeWriterMarkdown(text, role, i = 0) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;
    chat.appendChild(messageDiv);

    function type() {
        if (i < text.length) {
            messageDiv.innerHTML += text.charAt(i);
            i++;
            chat.scrollTop = chat.scrollHeight;
            setTimeout(type, 20);
        } else {
            // 渲染 Markdown 高亮
            if (window.Prism) Prism.highlightAll();
        }
    }
    type();
}