const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const typingIndicator = document.getElementById("typing-indicator");
const historyBox = document.getElementById("history-box");

userInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function appendMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `message ${sender}-message`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function updateHistory(historyArray) {
    historyBox.innerHTML = ""; // Clear existing
    historyArray.forEach(item => {
        const div = document.createElement("div");
        div.className = "history-item";
        div.innerHTML = `<div class="history-user">You: ${item.user}</div>
                         <div class="history-bot">Bot: ${item.bot}</div>`;
        historyBox.appendChild(div);
    });
    historyBox.scrollTop = historyBox.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // Show user message
    appendMessage(text, "user");
    userInput.value = "";

    // Show typing...
    typingIndicator.style.display = "block";
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();

        // Hide typing...
        typingIndicator.style.display = "none";

        // Show bot reply
        appendMessage(data.reply, "bot");

        // Update Sidebar history
        updateHistory(data.history);

    } catch (error) {
        typingIndicator.style.display = "none";
        appendMessage("Error: Could not connect to the server.", "bot");
    }
}
