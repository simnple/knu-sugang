# from ResponseCode import AddLectureStatus

from bs4 import BeautifulSoup
from google import genai
import requests
import hashlib
import base64
import time

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

SUGANG_URL = "https://sugang.kongju.ac.kr"
ENDPOINT = {
    "LOGIN": "/loginCheck",
    "SUGANG_PAGE": "/p/s/sugangMain",
    "ADD_LECTURE": "/d/s/add",
    "MACRO_INIT": "/d/m/macroInit",
    "MACRO_IMG": "/d/m/macroImg",
    "MACRO_CHECK": "/d/m/macroCheck"
}

class KnuSugang():
    def __init__(self):
        self.cookies = ""
        self.headers = {}

    def login(self, user_id, user_pw):
        self.cookies = ""

        session = requests.session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        }

        payload = {
            "lang": "ko",
            "txtUserID": user_id,
            "txtPwd": user_pw,
            "lang": "ko"
        }

        response = requests.post(SUGANG_URL + ENDPOINT["LOGIN"] + f"?fake={self.current_time()}", data=payload)

        for cookie in response.cookies:
            self.cookies += f"{cookie.name}={cookie.value}; "

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Referer": SUGANG_URL,
            "Cookie": self.cookies
        }

        response = requests.get(SUGANG_URL + ENDPOINT["SUGANG_PAGE"], headers=self.headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        divider = soup.select_one("#divider")

        self.rn_name = base64.b64decode(divider.get_attribute_list("data-rn")[0].encode()).decode()
        self.rn_value = base64.b64decode(divider.get_attribute_list("data-rv")[0].encode()).decode()

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Referer": SUGANG_URL,
            "Cookie": self.cookies,
            self.rn_name: self.rn_value
        }

    def get_hp(self, value):
        return hashlib.md5(f"{value}@{self.rn_value}".encode()).hexdigest()

    def current_time(self):
        return int(time.time() * 1000)

    def add_lecture(self, lecture_code, lecture_bunban):
        payload = {
            "params": f"{lecture_code}@{lecture_bunban}",
            "hp": self.get_hp(f"{lecture_code}@{lecture_bunban}")
        }

        response = requests.post(SUGANG_URL + ENDPOINT["ADD_LECTURE"] + f"?fake={self.current_time()}", headers=self.headers, data=payload)

        return {"code": int(response.json()["code"]), "message": response.json()["message"]}

    def get_macro_image(self):
        response = requests.post(SUGANG_URL + ENDPOINT["MACRO_INIT"] + f"?fake={self.current_time()}", headers=self.headers)

        result = response.json()
        if result["code"] != "200":
            raise ValueError("invalid code")
        
        response = requests.get(SUGANG_URL + ENDPOINT["MACRO_IMG"] + f"?fake={self.current_time()}", headers=self.headers)

        open("image.png", "wb").write(response.content)
        return result

    def solve_macro_image(self, api_key):
        client = genai.Client(api_key=api_key)

        contents=['이미지에 적혀있는 4자리 코드를 말해, 출력 예시는 다음과 같아.\nABCD', client.files.upload(file="image.png")]

        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents
        )

        return response.text

    def input_code(self, code):
        payload = {
            "secNumber": code
        }

        response = requests.post(SUGANG_URL + ENDPOINT["MACRO_CHECK"] + f"?fake={self.current_time()}", headers=self.headers, data=payload)

        return {"code": int(response.json()["code"]), "failCnt": int(response.json()["failCnt"]), "message": response.json()["message"]}
