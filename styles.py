css = '''
<style>

.avatar img {
    max-width: 60px;
    max-height: 60px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}

/* -------------------------------------------- BOT --------------------------------------------*/
.chat-message.bot {
    background-color: #475063;
    color: #fff;
}

.chat-message.bot .message {
    margin-left: 10px;
    margin-right: 20px;
    text-align: justify;
}

.chat-message.bot .avatar{
    margin-left: 10px;
}

/* -------------------------------------------- USER --------------------------------------------*/
.chat-message.user {
    background-color: #2b313e;
    color: #fff;
    display: flex;
    justify-content: flex-end;
}

.chat-message.user .message {
    margin-left: 20px;
    margin-right: 10px;
    text-align: justify;
}

.chat-message.user .avatar{
    margin-right: 10px;
}

/* -------------------------------------------- SIDE PANEL --------------------------------------------*/
.st-emotion-cache-16txtl3 h2 {
    font-weight: bold;
    font-size: 2.3rem;
}

.st-emotion-cache-hc3laj {
    width: 100%;
}

.st-emotion-cache-183lzff {
    font-family: sans-serif;
    margin-left: 2.5rem;
    font-size: 0.8rem;
    font-weight: 500;
    text-align: center;
    font-style: italic;
    color: #5A5A5A;
    line-height: 1;
}

</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/KN1TVrX/bot.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
    <div class="avatar">
        <img src="https://i.ibb.co/gjPHppH/human.jpg">
    </div>
</div>
'''