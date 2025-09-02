from KnuSugang import KnuSugang
from dotenv import load_dotenv
import os

load_dotenv()
USER_ID = os.environ.get("USER_ID")
USER_PW = os.environ.get("USER_PW")
GEMINI_API = os.environ.get("GEMINI_API")

sugang = KnuSugang()

sugang.login(USER_ID, USER_PW)

result = sugang.add_lecture("2006779", "34")

if result["code"] == 118:
    sugang.get_macro_image()
    sugang.solve_macro_image(GEMINI_API)

# elif result["code"] == 204:
