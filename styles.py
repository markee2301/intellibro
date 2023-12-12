css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
    padding-right: 0;
}

.chat-message.user .message{
    float: right;
    text-align: right;
}

.chat-message.bot {
    background-color: #475063;
    padding-left: 3rem;
}

.chat-message.user .avatar {
    width: 15%;
    display: flex;
    align-items: center;
}

.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
    text-align: left;
}

.box {
    position: fixed;
    bottom: 0;
    width: 100%;
}

.st-emotion-cache-16txtl3 h2 {
    font-weight: bold;
    font-size: 2.3rem;
}

.st-emotion-cache-hc3laj{
    width: 100%;
}

.st-emotion-cache-183lzff{
    font-family:sans-serif;
    margin-left: 3rem;
    font-size: 0.8rem;
    font-weight: 500;
    text-align: center;
    font-style: italic;
    color: #5A5A5A;
}

</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar" style="float: left;">
        <img src="https://i.ibb.co/KN1TVrX/bot.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message" style="float: left;">{{MSG}}</div>
    <div class="avatar" style="float: right;">
        <img src="https://i.ibb.co/2tBGL8d/human.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
</div>
'''

user_question = '''
<div class="box">
  <input type="text">
</div>
'''