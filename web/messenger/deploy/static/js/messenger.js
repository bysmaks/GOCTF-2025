document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('message-form');
    const search_input = document.getElementById('search-input');
    const messageInput = document.getElementById('message-input');
    const messages = document.getElementById('messages');
    const search_results = document.getElementById('search-results');
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const messageText = messageInput.value;
        if (messageText.trim() === "") {
            return;
        }

        const message = document.createElement('div');
        message.className = 'message user-message';
        message.textContent = messageText;
        messages.appendChild(message);

        messages.scrollTop = messages.scrollHeight;

        messageInput.value = '';

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/send_message', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                let response = JSON.parse(xhr.responseText);
                let incomingMessage = document.createElement('div');
                incomingMessage.className = 'message';
                incomingMessage.textContent = response.message;
                messages.appendChild(incomingMessage);

                messages.scrollTop = messages.scrollHeight;
            }
        };

        xhr.send(JSON.stringify({ message: messageText }));
    });


    search_input.addEventListener('input', function(e) {
        e.preventDefault();

        let search_text = search_input.value;
        console.log(search_text);
        if (search_text.trim() === "") {
            search_results.style.display = "none";
            return;
        }
        let request = new XMLHttpRequest();
        request.open('GET', `/user_search?q=${search_text}`, true);
        request.setRequestHeader('Content-Type', 'application/json')

        request.onreadystatechange = function() {
            if (request.readyState === 4 && request.status === 200) {

                let response = JSON.parse(request.responseText);
                console.log(response);
                if (response.users) {
                    search_results.innerHTML = "";
                    search_results.style.display = "block";
                    for (let user of response.users) {
                        search_results.innerHTML += `<p>${user}</p>`
                    }
                }
                else {
                     search_results.innerHTML = "";

                     search_results.style.display = "none";
                     return;
                }

            }
        }
        request.send();


    })


    const chatItems = document.querySelectorAll('.chat-item');
    chatItems.forEach(item => {
        item.addEventListener('click', function() {
            const chatId = this.getAttribute('data-chat-id');
            this.style.background = '#f0f0f021';

            const selectChatMessage = document.querySelector('.select-chat-message');
            if (selectChatMessage) {
                selectChatMessage.remove();
            }

            messages.innerHTML = '';

            form.style.display = 'flex';
        });
    });
});