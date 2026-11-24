from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "taiba123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")

def get_reply(text):
    text = text.lower()
    if "سلام" in text or "السلام" in text or "hi" in text or "هلا" in text:
        return "وعليكم السلام، نورت طيبة تكنولجي، أنا طيبة مساعدة مستر إبراهيم الشاذلي ، تحب أساعدك تبدأ مشروعك إزاي؟"
    if "خدمات" in text or "بتقدم" in text or "بتعمل" in text or "ايه هي" in text:
        return "احنا في طيبة تكنولجي بنمكن مشروعك من الخدمات الرقمية، ونخلي مشروعك موجود في العالم الرقمي، وبالذكاء الاصطناعي اللي يدير مشروعك بالكامل . نعملك صفحة، ونربط مكانك على خرائط جوجل، ونربط موقعك ودومينك بكل السوشيال ميديا. تحب نبدأ بإيه؟"
    if "مشروع" in text or "ابدأ" in text or "عاوز" in text:
        return "أهلاً بيك، ابدأ مشروعك معنا. قولي مشروعك إيه؟ محل؟ شركة؟ ولا لسه فكرة؟ وأنا أقولك أول خطوة ليك."
    if "خريطة" in text or "جوجل" in text or "ماب" in text:
        return "أكيد، نعملك مكانك على خرائط جوجل ماب، عشان أي حد يدور عليك يلاقيك على الخريطة. ابعتلي اسم مشروعك وعنوانك."
    if "صفحة" in text or "فيسبوك" in text:
        return "نعملك صفحة زي صفحتنا دي، والذكاء الاصطناعي يرد على عملاءك 24 ساعة. تحب نبدأ في صفحتك؟"
    if "اعلان" in text or "مممول" in text or "اعلانات" in text:
        return "تمام، الإعلانات دي شغلتنا، بنعمل حملات على كل أدوات 【entity-ميتا¦canonical_name=ميتا】. قولي مشروعك إيه، وأنا أجهزلك الفكرة الأولى."
    if "فلوس" in text or "بكام" in text or "سعر" in text or "price" in text:
        return "متشغلش بالك بالفلوس دلوقتي، جرب خدمتنا الأولى مجاناً، ولو حبيتها مستر إبراهيم هيكلمك بنفسه ويعرض عليك اللي يناسبك."
    if "شكرا" in text or "تمام" in text:
        return "العفو، نورتنا، أنا موجودة هنا أي وقت، وابدأ مشروعك معنا."
    return "أنا طيبة من طيبة تكنولجي، أنا هنا عشان أمكن مشروعك رقمياً، قولي مشروعك إيه وأنا أساعدك تبدأ."

def send_message(recipient_id, message_text):
    if not PAGE_ACCESS_TOKEN:
        return
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    requests.post(url, json={"recipient": {"id": recipient_id}, "message": {"text": message_text}})

@app.route("/", methods=["GET"])
def home():
    return "طيبة شغالة"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "غلط", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            sender_id = event["sender"]["id"]
            if "message" in event and "text" in event["message"]:
                reply = get_reply(event["message"]["text"])
                send_message(sender_id, reply)
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
