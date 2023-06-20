from flask import Flask, request, abort
import re



from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('gl+esNOEr7z+LIRpQarujmD4uPDhHGF4SVtmGK8WjtwSQrsPQONfOdcOpJ2/mpOxA6ZBPhK8xutA88+W59Orz4MH1B5fJihmmhDY8n0KkVXo0uJplGg1tsqJN+NXUPDo4BDLZRA1unMqfkz1upPUsQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1f17d0d837d0e1cfa65930e681790687')

@app.route("/")
def test():
    return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        
        handler.handle(body, signature)
   
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


from time import time
users = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    pattern = r"(\d+)時(\d+)分"

    if event.message.text == "勉強開始":
        reply_text="計測を開始"

        if not userId in users:
            users[userId] = {}
            users[userId]["total"] = 0

        users[userId]["start"] = time()

    elif event.message.text == "勉強終了":
        end = time()
        dif = end - users[userId]["start"]
        users[userId]["total"] += dif

        hour = dif//3600
        minitue = (dif%3600)//60
        second = dif%60

        reply_text="{}時間{}分{}秒経過したよおおお。合計勉強時間は{}秒です".format(int(hour),int(minitue),int(second),int(users[userId]["total"]))

    elif event.message.text == "アラームを設定":
        reply_text="何時に設定する？"

    # 送られてきたメッセージが「〇〇時〇〇分」の形式かどうかを判定
    elif re.search(pattern, event.message.text):
        match = re.search(pattern, event.message.text)

        if match:
            hour = match.group(1)
            minute = match.group(2)
            print("マッチしました")
            print("時:", hour)
            print("分:", minute)
        else:
            print("マッチしませんでした")


    elif event.message.text == "7時30分":
        now = time()
        wakeup = now + 10
        dif = wakeup - now

    else:
        reply_text=event.message.text

    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))


if __name__ == "__main__":
    app.run()