// ===============================
// DELETE CONFIRMATION
// ===============================
function confirmDelete() {
    return confirm("⚠ Are you sure you want to delete this account?\nThis action cannot be undone!");
}


// ===============================
// TOGGLE CHAT (Smooth Animation)
// ===============================
function toggleChat() {
    const bot = document.getElementById("chatbot");

    bot.classList.toggle("active");

    // Greeting only first time opening
    if (bot.classList.contains("active") && !bot.dataset.greeted) {
        setTimeout(() => {
            addBotMessage("Hello 👋 Welcome to Smart Gullak!");
            addBotMessage("How can I help you today?");
        }, 400);

        bot.dataset.greeted = "true";
    }
}


// ===============================
// SEND MESSAGE (Button + Enter)
// ===============================
function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();

    if (message === "") return;

    addUserMessage(message);
    input.value = "";

    showTyping();

    setTimeout(() => {
        removeTyping();
        botReply(message);
    }, 800);
}

// Press Enter to send
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("userInput").addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});


// ===============================
// ADD USER MESSAGE
// ===============================
function addUserMessage(text) {
    const chat = document.getElementById("chatBody");
    chat.innerHTML += `<div class="message user">${text}</div>`;
    chat.scrollTop = chat.scrollHeight;
}


// ===============================
// ADD BOT MESSAGE
// ===============================
function addBotMessage(text) {
    const chat = document.getElementById("chatBody");
    chat.innerHTML += `<div class="message bot">${text}</div>`;
    chat.scrollTop = chat.scrollHeight;
}


// ===============================
// TYPING EFFECT
// ===============================
function showTyping() {
    const chat = document.getElementById("chatBody");
    chat.innerHTML += `<div class="message bot typing" id="typing">Typing...</div>`;
    chat.scrollTop = chat.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
}


// ===============================
// SIMPLE AI LOGIC
// ===============================
function botReply(msg) {
    msg = msg.toLowerCase();

    if (msg.includes("balance")) {
        addBotMessage("You can see your balance in the Total Savings section 💰");
    }
    else if (msg.includes("deposit")) {
        addBotMessage("Use the Deposit card to add money to your gullak.");
    }
    else if (msg.includes("withdraw")) {
        addBotMessage("Use the Withdraw card to take money from your savings.");
    }
    else if (msg.includes("delete")) {
        addBotMessage("Be careful! Deleting your account will remove all data permanently.");
    }
    else if (msg.includes("hi") || msg.includes("hello")) {
        addBotMessage("Hello there! 😊 How can I assist you?");
    }
    else {
        addBotMessage("I'm still learning 🤖 Try asking about balance, deposit, withdraw or delete.");
    }
}