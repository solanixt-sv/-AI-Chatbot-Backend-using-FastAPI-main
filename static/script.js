document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const promptInput = document.getElementById("prompt-input");
    const sendBtn = document.getElementById("send-btn");
    const chatBox = document.getElementById("chat-box");

    function appendMessage(role, content, isStreaming = false) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${role}-message`;
        
        const contentDiv = document.createElement("div");
        contentDiv.className = "message-content";
        
        if (isStreaming) {
            contentDiv.innerHTML = '<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>';
        } else {
            // Parse Markdown and sanitize HTML
            const rawMarkup = marked.parse(content);
            const cleanMarkup = DOMPurify.sanitize(rawMarkup);
            contentDiv.innerHTML = cleanMarkup;
        }

        msgDiv.appendChild(contentDiv);
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        
        return { msgDiv, contentDiv };
    }

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const prompt = promptInput.value.trim();
        if (!prompt) return;

        // Add user message
        appendMessage("user", prompt);
        promptInput.value = "";
        
        // Disable input while generating
        promptInput.disabled = true;
        sendBtn.disabled = true;

        // Add placeholder for assistant
        const { msgDiv, contentDiv } = appendMessage("assistant", "", true);

        try {
            const response = await fetch("/chat/stream", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: prompt })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Server error");
            }

            contentDiv.innerHTML = ""; // Remove typing indicator
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let fullText = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                fullText += chunk;
                
                // Parse incrementally
                const rawMarkup = marked.parse(fullText);
                contentDiv.innerHTML = DOMPurify.sanitize(rawMarkup);
                
                // Keep scrolled to bottom
                chatBox.scrollTop = chatBox.scrollHeight;
            }

        } catch (error) {
            contentDiv.innerHTML = `<span style="color: #ef4444;">Error: ${error.message}</span>`;
        } finally {
            promptInput.disabled = false;
            sendBtn.disabled = false;
            promptInput.focus();
        }
    });
});
