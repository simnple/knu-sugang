# 국립공주대학교 수강신청 비공식 라이브러리

## Usage
```bash
git clone https://github.com/simnple/knu-sugang.git
```

in python code you need to import **KnuSugang**
```python
from KnuSugang import KnuSugang
```

## Code
[main.py](https://github.com/simnple/knu-sugang/blob/main/main.py)를 참고해주세요.

## Security
해당 사이트에선 다음과 같은 보안 요소들이 들어가 있습니다.
- 매크로 방지를 위한 보안 문자
  - 해당 보안 문자는 4자리 코드로 이미지를 생성하며 이는 ocr로 인식이 가능한 수준입니다.
  - 수강 신청을 50번 실패 시 보안 문자가 등장하게 됩니다.
- body 인증용 해시
  - 수강 신청을 진행할 때, body 부분에 hp라는 이름으로 강의 코드와 분반을 인증하는 과정이 들어가있습니다.
  - 이 hp는 rn value와 강의 코드 분반을 조합하여 생성합니다.
- fake 파라미터
  - 사실 이게 보안 요소에 포함되는지는 모르겠습니다만, 현재 시각을 fake 인자로 넘깁니다.
  - timestamp의 형식은 ms까지 입니다.
- rn name and rn value
  - 수강 신청을 진행하려면 빠지면 안되는 요소입니다.
  - header에 rn name: rn value 형식으로 들어가 있으며, 없다면 요청이 정상적으로 보내지지 않습니다.
  - 이는 서버에서 생성해주기에 생성 로직은 잘 모르겠습니다.

## Endpoints
Endpoint에 해당되는 응답 코드들을 정리했습니다.

허나 코드들을 다 적지 못했기에 PR 해주시면 감사하겠습니다!

### 수강 신청
> **POST** `/d/s/add`

#### request body
```json
{
    "params": "{lecture_code}@{lecture_bunban}@{something (not required)}",
    "hp": "params의 내용을 hp로 변환한 결과 (md5)"
}
```

#### response body
```json
{
    "code": "code",
    "message": "alert에 사용할 메시지"
}
```

|code|desc|
|:---:|:---:|
|118|보안 문자 감지|
|204|정원 초과|
|500|수강 신청 기간 아님|
|999|세션 만료|

코드를 정확하게 확인하진 못했지만, code `200`이 수강 신청 완료일 가능성이 높아보입니다.

### 매크로 init
> **POST** `/d/m/macroInit`

#### response body
```json
{
    "code": "code",
    "failCnt": 0 // failCnt는 입력 시도 가능한 횟수 (기본 10)
}
```

|code|desc|
|:---:|:---:|
|200|정상|

### 보안 문자 이미지
> **GET** `/d/m/macroImg`

### 보안 문자 입력
> **POST** `/d/m/macroCheck`

#### request body
```json
{
    "secNumber": "code"
}
```

#### response body
```json
{
    "code": "code",
    "failCnt": 0, // failCnt는 입력 시도 가능한 횟수 (기본 10)
    "message": "alert에 사용할 메시지"
}
```

|code|desc|
|:---:|:---:|
|200|통과|
|500|잘못된 보안 문자|