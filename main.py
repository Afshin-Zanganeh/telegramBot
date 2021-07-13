import json
import requests
from flask import Flask, request, Response
import matplotlib.pyplot as plt


token = "1716372110:AAEso-coFs5_JJbzqSGmtzgSkzBCOohkt_Q"
url = "https://api.telegram.org/bot" + token + "/"

program = Flask(__name__)


def doPlot(kharj, dakhl, chat_id):
    plt.pie((kharj, dakhl), labels=["kharj", "dakhl"])
    plt.savefig(f"{chat_id}.jpg")


def send_message(user, text, keyboard=None):
    global token
    if keyboard is not None:
        requests.post(
            "https://api.telegram.org/bot" + token + "/sendMessage",
            {"text": text, "chat_id": user, "reply_markup": keyboard},
        )
    else:
        requests.post(
            "https://api.telegram.org/bot" + token + "/sendMessage",
            {"text": text, "chat_id": user},
        )


def keyboard_maker(text_list):
    button = []
    for text in text_list:
        button.append([{"text": text}])

    keyboard = json.dumps({"resize_keyboard": True, "keyboard": button})
    return keyboard


def write_json(data):
    with open("data.json", "w") as target:
        json.dump(data, target, indent=4, ensure_ascii=False)


def read_json():
    with open("data.json", "r") as target:
        data = json.load(target)
    return data


@program.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return Response("<h1>Working :))</h1>", status=200)
    try:
        db = read_json()
    except FileNotFoundError:
        write_json({})
        db = read_json()
    telegram_data = request.get_json()
    chat_id = telegram_data["message"]["chat"]["id"]
    chat_id_str = str(chat_id)
    text = telegram_data["message"].get("text", "")
    step = db.get(chat_id_str, None)
    if step is None:
        db[chat_id_str] = {"dakhl": [], "kharj": [], "step": ""}
        step = ""
    else:
        step = db[chat_id_str]["step"]
    if text == "/start" or text == "برگشت به منوی اصلی":
        db[chat_id_str]["step"] = ""
        send_message(
            chat_id,
            "‫‬سلام به ربات مدیریت دخل و خرج ما خوش اومدی\n\nتوسعه دهنده های ربات : فاطمه لطفی 99462014 و احسان رهجو 99451298",
            keyboard_maker(
                [
                    "درباره ربات",
                    "معرفی ربات به دوستان",
                    "اطلاعات مورد نیاز",
                    "مثال",
                    "شروع مدیریت",
                    "ویرایش دخل یا خرج",
                ]
            ),
        )
    elif text == "درباره ربات" and step == "":
        requests.post(
            f"https://api.telegram.org/bot" + token + "/sendDocument",
            {
                "chat_id": chat_id,
                "document": "BQACAgQAAxkBAAMNYOWm92m7zJcWXnNFdoM-q8jJRQkAAp0LAAIjfihT5euEUOS2sMwgBA",
                "caption": "بفرمایید اینم توضیحات ربات",
            },
        )
    elif text == "معرفی ربات به دوستان" and step == "":
        send_message(
            chat_id, "با فوروارد کردن پیام ریز بات دخل و خرج رو به دوستات معرفی کن"
        )
        send_message(
            chat_id,
            "اگر مدیریت دخل و خرج برایتان دشوار است وارد ربات شوید تا در کمترین زمان ممکن گزارش و نمودار های مربوط به دخل خرجتان را دریافت کنید\n@ModiriatMakharejBot",
        )
    elif text == "اطلاعات مورد نیاز" and step == "":
        send_message(
            chat_id,
            "اطلاعات مورد نیاز برای کار با ربات :\n1. دخل یا خرج جدید\n2. مقدار دخل یا خرج",
        )
    elif text == "مثال" and step == "":
        try:
            picture = open("example.jpg", "r")
            picture.close()
        except:
            plt.pie((10, 10), labels=["kharj", "dakhl"])
            plt.savefig("example.jpg")

        requests.post(
            url + "sendPhoto",
            {
                "chat_id": chat_id,
            },
            files={
                "photo": (
                    "example.jpg",
                    open("example.jpg", "rb"),
                    "multipart/form-data",
                ),
            },
        )
    elif text == "شروع مدیریت" and step == "":
        send_message(
            chat_id,
            "از کیبورد زیر استفاده کنید",
            keyboard_maker(["دخل", "خرج", "نمودار", "برگشت"]),
        )
        db[chat_id_str]["step"] = "new"
    elif text == "ویرایش دخل یا خرج":
        send_message(
            chat_id,
            "دخل یا خرج رو میخوایی ویرایش کنی؟",
            keyboard_maker(["دخل", "خرج", "برگشت به منوی اصلی"]),
        )
        db[chat_id_str]["step"] = "edit"
    elif step == "new":
        if text == "دخل":
            db[chat_id_str]["step"] = "new dakhl"
            send_message(
                chat_id,
                "‫‬مبلغ دخل خود را وارد کنید و یا با دکمه بازگشت به منوی اصلی به منوی اصلی بازگردید",
                keyboard_maker(["برگشت به منوی اصلی"]),
            )
        elif text == "خرج":
            db[chat_id_str]["step"] = "new kharj"
            send_message(
                chat_id,
                "‫‬مبلغ خرج خود را وارد کنید و یا با دکمه بازگشت به منوی اصلی به منوی اصلی بازگردید",
                keyboard_maker(["برگشت به منوی اصلی"]),
            )
        elif text == "برگشت":
            db[chat_id_str]["step"] = ""
            send_message(
                chat_id,
                "‫‬سلام به ربات مدیریت دخل و خرج ما خوش اومدی\n\nتوسعه دهنده های ربات : فاطمه لطفی 99462014 و احسان رهجو 99451298",
                keyboard_maker(
                    [
                        "درباره ربات",
                        "معرفی ربات به دوستان",
                        "اطلاعات مورد نیاز",
                        "مثال",
                        "شروع مدیریت",
                        "ویرایش دخل یا خرج",
                    ]
                ),
            )
        elif text == "نمودار":
            kharj = sum(db[chat_id_str]["kharj"])
            dakhl = sum(db[chat_id_str]["dakhl"])
            kharj = 1 if kharj == 0 else kharj
            dakhl = 1 if dakhl == 0 else dakhl
            doPlot(kharj, dakhl, chat_id)
            requests.post(
                url + "sendPhoto",
                {
                    "chat_id": chat_id,
                },
                files={
                    "photo": (
                        f"{chat_id}.jpg",
                        open(f"{chat_id}.jpg", "rb"),
                        "multipart/form-data",
                    ),
                },
            )
        else:
            send_message(
                chat_id,
                "از کیبورد پایین استفاده کنید",
                keyboard_maker(["دخل", "خرج", "نمودار", "برگشت"]),
            )
    elif step == "new kharj" or step == "new dakhl":
        if text.isnumeric():
            persian_word = "خرج" if step == "new kharj" else "دخل"
            db[chat_id_str]["step"] = step + f" {text}"
            send_message(
                chat_id,
                f"{persian_word} جدید با قیمت {text} اضافه خواهد شد آیا اطمینان دارید؟",
                keyboard_maker(["بله", "برگشت به منوی اصلی"]),
            )
        else:
            send_message(chat_id, "لطفا عدد وارد کنید")
    elif (
        step.split()[:2] == ["new", "dakhl"] or step.split()[:2] == ["new", "kharj"]
    ) and text == "بله":
        step_split = step.split()
        dakhl_or_kharj = step_split[1]
        if dakhl_or_kharj == "kharj":
            db[chat_id_str]["kharj"].append(int(step_split[2]))
            word = "خرج"
            code = len(db[chat_id_str]["kharj"]) - 1
        else:
            db[chat_id_str]["dakhl"].append(int(step_split[2]))
            word = "دخل"
            code = len(db[chat_id_str]["dakhl"]) - 1
        send_message(
            chat_id, f"{word} با موفقیت ثبت شد\nکد پیگیری برای ویرایش : {code}"
        )
        db[chat_id_str]["step"] = ""
        send_message(
            chat_id,
            "‫‬سلام به ربات مدیریت دخل و خرج ما خوش اومدی\n\nتوسعه دهنده های ربات : فاطمه لطفی 99462014 و احسان رهجو 99451298",
            keyboard_maker(
                [
                    "درباره ربات",
                    "معرفی ربات به دوستان",
                    "اطلاعات مورد نیاز",
                    "مثال",
                    "شروع مدیریت",
                    "ویرایش دخل یا خرج",
                ]
            ),
        )
    elif step == "edit":
        if text == "دخل":
            send_message(
                chat_id,
                "ایدی دخلی ک میخوایید تغییر بدید رو بنویسید",
                keyboard_maker(["برگشت به منوی اصلی"]),
            )
            db[chat_id_str]["step"] = "edit dakhl"
        elif text == "خرج":
            send_message(
                chat_id,
                "ایدی خرجی ک میخوایید تغییر بدید رو بنویسید",
                keyboard_maker(["برگشت به منوی اصلی"]),
            )
            db[chat_id_str]["step"] = "edit kharj"
        else:
            send_message(
                chat_id,
                "از کیبورد استفاده کنید",
                keyboard_maker(["دخل", "خرج", "برگشت به منوی اصلی"]),
            )
    elif step == "edit dakhl" or step == "edit kharj":
        if not text.isnumeric():
            send_message(chat_id, "ایدی باید عددی باشد", ["برگشت به منوی اصلی"])
        else:
            index = "dakhl" if step == "edit dakhl" else "kharj"
            try:
                check = db[chat_id_str][index][int(text)]
                db[chat_id_str]["step"] = f"edit {index} {text}"
                send_message(
                    chat_id,
                    f"مبلغ مورد نظر رو وارد کنید\nمبلغ فعلی {check}",
                    keyboard_maker(["برگشت به منوی اصلی"]),
                )
            except:
                send_message(
                    chat_id,
                    f"ایدی {text} وجود ندارد !",
                    keyboard_maker(["برگشت به منوی اصلی"]),
                )
    elif step.split()[:2] == ["edit", "dakhl"] or step.split()[:2] == ["edit", "kharj"]:
        step_split = step.split()
        if text.isnumeric():
            try:
                db[chat_id_str][step_split[1]][int(step_split[2])] = int(text)
                send_message(
                    chat_id,
                    "با موفقیت تغییر کرد",
                )
                db[chat_id_str]["step"] = ""
                send_message(
                    chat_id,
                    "‫‬سلام به ربات مدیریت دخل و خرج ما خوش اومدی\n\nتوسعه دهنده های ربات : فاطمه لطفی 99462014 و احسان رهجو 99461298",
                    keyboard_maker(
                        [
                            "درباره ربات",
                            "معرفی ربات به دوستان",
                            "اطلاعات مورد نیاز",
                            "مثال",
                            "شروع مدیریت",
                            "ویرایش دخل یا خرج",
                        ]
                    ),
                )
            except:
                send_message(
                    chat_id,
                    "مشکلی به وجود اومده",
                    keyboard_maker(["برگشت به منوی اصلی"]),
                )
    write_json(db)
    return Response("Done", status=200)


program.run(host='0.0.0.0', port=5000)
