frappe.ready(function () {
    console.log("HRMS Guide Bot Widget Loading...");
    // Only load if user is logged in
    if (frappe.session.user === 'Guest') return;

    // Check existing
    if ($('#hrms-guide-bot-root').length > 0) return;

    // Create wrapper
    const $wrapper = $(`<div id="hrms-guide-bot-root" class="hrms-bot-widget closed"></div>`).appendTo('body');

    // Create Toggle Button
    const $toggle = $(`
        <button class="hrms-bot-toggle">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-message-circle"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
        </button>
    `).appendTo($wrapper);

    // Create Chat Window
    const $window = $(`
        <div class="hrms-bot-window">
            <div class="hrms-bot-header">
                <h3>HR Assistant</h3>
                <span class="close-bot">&times;</span>
            </div>
            <div class="hrms-bot-messages">
                <div class="hrms-bot-message bot">
                    Hello ${frappe.session.user_fullname}! asking me about HR policies or navigation.
                </div>
            </div>
            <div class="hrms-bot-input">
                <input type="text" placeholder="Type a message..." />
                <button class="send-btn">➤</button>
            </div>
        </div>
    `).appendTo($wrapper);

    // Styles (Injected here for simplicity, ideally in .css)
    const styles = `
        .hrms-bot-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1001;
            font-family: var(--font-stack, sans-serif);
        }
        .hrms-bot-toggle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--primary, #2490ef);
            color: white;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .hrms-bot-widget.open .hrms-bot-window {
            display: flex;
        }
        .hrms-bot-window {
            display: none;
            flex-direction: column;
            position: absolute;
            bottom: 60px;
            right: 0;
            width: 350px;
            height: 500px;
            background: var(--card-bg, #fff);
            border: 1px solid var(--border-color, #e2e6eb);
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            overflow: hidden;
        }
        .hrms-bot-header {
            padding: 12px 16px;
            background: var(--bg-light-gray, #f8f9fa);
            border-bottom: 1px solid var(--border-color, #e2e6eb);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .hrms-bot-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .hrms-bot-message {
            max-width: 80%;
            padding: 8px 12px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.4;
        }
        .hrms-bot-message.bot {
            background: var(--bg-light-gray, #f4f5f6);
            align-self: flex-start;
            border-bottom-left-radius: 2px;
        }
        .hrms-bot-message.user {
            background: var(--primary, #2490ef);
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
        }
        .hrms-bot-input {
            padding: 12px;
            border-top: 1px solid var(--border-color, #e2e6eb);
            display: flex;
            gap: 8px;
        }
        .hrms-bot-input input {
            flex: 1;
            padding: 8px;
            border: 1px solid var(--border-color, #d1d8dd);
            border-radius: 4px;
        }
        .bot-action-link {
            display: inline-block;
            margin-top: 4px;
            color: var(--primary, #2490ef);
            text-decoration: underline;
            cursor: pointer;
        }
    `;

    $('<style>').text(styles).appendTo('head');

    // Logic
    function toggleChat() {
        $wrapper.toggleClass('open');
    }

    $toggle.on('click', toggleChat);
    $window.find('.close-bot').on('click', toggleChat);

    const $input = $window.find('input');
    const $messages = $window.find('.hrms-bot-messages');

    function addMessage(text, sender) {
        const $msg = $(`<div class="hrms-bot-message ${sender}">${text}</div>`);
        $messages.append($msg);
        $messages.scrollTop($messages[0].scrollHeight);
    }

    function addAction(label, url) {
        const $action = $(`<div class="hrms-bot-message bot"><a class="bot-action-link">${label}</a></div>`);
        $action.find('a').on('click', () => frappe.set_route(url));
        $messages.append($action);
        $messages.scrollTop($messages[0].scrollHeight);
    }

    function sendMessage() {
        const text = $input.val().trim();
        if (!text) return;

        addMessage(text, 'user');
        $input.val('');

        // Call API
        frappe.call({
            method: 'hrms_guide_bot.hrms_guide_bot.api.chat',
            args: {
                message: text,
                context: {
                    route: frappe.get_route_str()
                }
            },
            callback: function (r) {
                if (r.message) {
                    const data = r.message;

                    // Handle Payload based on intent
                    if (data.payload.message) {
                        addMessage(data.payload.message, 'bot');
                    }
                    if (data.payload.answer) {
                        addMessage(data.payload.answer, 'bot');
                    }
                    if (data.payload.open_url) {
                        addAction(`Open ${data.payload.path[0]}`, data.payload.open_url);
                        // Auto redirect if confidence is high? No, let user click.
                    }
                }
            }
        });
    }

    $window.find('.send-btn').on('click', sendMessage);
    $input.on('keypress', (e) => {
        if (e.which === 13) sendMessage();
    });
});
