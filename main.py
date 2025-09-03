from KnuSugang import KnuSugang
from dotenv import load_dotenv
import os
import time

load_dotenv()
USER_ID = os.environ.get("USER_ID")
USER_PW = os.environ.get("USER_PW")
GEMINI_API = os.environ.get("GEMINI_API")

sugang = KnuSugang()

sugang.login(USER_ID, USER_PW)

while True:
    try:
        result = sugang.add_lecture("2006779", "34")

        if result["code"] == 118:
            print("[*] 보안 문자가 감지되었습니다.")
            result = sugang.get_macro_image()
            if result["failCnt"] < 3:
                print("[-] 현재 보안 문자 인증 횟수가 부족해 사용할 수 없습니다.")
                exit()
            code = sugang.solve_macro_image(GEMINI_API)

            result = sugang.input_code(code)
            if result["code"] == 200:
                print(f"[+] 보안 문자를 해결했습니다. | code: {code} | failCnt: {result['failCnt']}")
            elif result["code"] == 500:
                print(f"[-] 보안 문자를 잘못 입력했습니다. | failCnt: {result['failCnt']}")
            else:
                print(f"[-] 보안 문자 해결을 실패했습니다. | result: {result}")

        elif result["code"] == 204:
            print(f"[-] 해당 강의는 정원 초과 상태입니다.")

        elif result["code"] == 500:
            print(f"[-] 수강신청 기간이 끝났습니다.")
            exit()

        elif result["code"] == 999:
            print(f"[-] 로그인을 재시도합니다.")
            sugang.login(USER_ID, USER_PW)

        else:
            print(f"[+] {result}")
            exit()

    except:
        sugang.login(USER_ID, USER_PW)

    time.sleep(1)
