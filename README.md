# SFAI 2025 - 스마트팜 AI 경진대회

## 프로젝트 개요

이 프로젝트는 2025년 스마트농업 AI 경진대회를 위한 통신 인터페이스 예시입니다. 프로젝트는 Modbus 표준 프로토콜을 사용하는 `KSB7958`과 비표준 인터페이스를 사용하는 `extra` 두 가지 주요 부분으로 나뉩니다.

### KSB7958 (표준 인터페이스)

이 디렉토리의 코드는 `pymodbus` 라이브러리를 사용하여 Modbus TCP를 통해 스마트팜 장비와 통신합니다. 이를 통해 센서 데이터를 읽고 개폐기, 스위치, 양액 공급기와 같은 구동기를 제어합니다.

**주요 파일:**
*   `read_sensor.py`: 다양한 센서(온도, 습도, CO2 등)에서 데이터를 읽는 예제입니다.
*   `nutsupply.py`: 양액 공급 시스템을 제어하는 예제입니다.
*   `retractable.py`: 개폐기를 제어하는 예제입니다.
*   `switch.py`: 스위치를 켜고 끄는 예제입니다.
*   `kstest_cli.py`: `switch`, `retractable`, `nutsupply` 모듈을 테스트하기 위한 명령줄 인터페이스입니다. 대화형 모드 또는 명령줄 인수를 통해 특정 장치를 테스트할 수 있습니다.
*   `ksconstants.py`: Modbus 통신에 사용되는 상수(명령 코드, 상태 코드)를 정의합니다.
*   `conf.json`: Modbus 서버의 IP 주소 및 포트와 같은 설정을 포함합니다.

### extra (비표준 인터페이스)

이 디렉토리의 코드는 `httpx` 라이브러리를 사용하여 외부 웹 API와 통신합니다. 이를 통해 기상 예보와 같은 외부 데이터를 가져오거나, 원격 API에 데이터를 전송할 수 있습니다.

**주요 파일:**
*   `client.py`: 외부 API와 통신하는 비동기 클라이언트입니다. 이미지 가져오기, 기상 예보 가져오기, 하트비트 전송, 제어 목표 전송과 같은 기능을 제공합니다.
*   `sample.py`: `client.py`를 사용하여 `extra` API와 상호 작용하는 방법을 보여주는 예제입니다.
*   `conf.json`: API 엔드포인트 URL 및 API 키와 같은 설정을 포함합니다.

## 설치 및 실행

1.  **가상환경 생성 및 활성화:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **샘플 실행:**
    *   **센서 데이터 읽기:**
        ```bash
        python KSB7958/read_sensor.py
        ```
    *   **양액 공급 테스트:**
        ```bash
        python KSB7958/nutsupply.py
        ```
    *   **외부 API 샘플 실행:**
        ```bash
        python extra/sample.py
        ```
    *   **통합 테스트 CLI 실행:**
        *   **대화형 모드:**
            ```bash
            python KSB7958/kstest_cli.py
            ```
        *   **명령줄 인수 사용:**
            ```bash
            # 스위치 테스트
            python KSB7958/kstest_cli.py switch
            # 특정 개폐기 테스트
            python KSB7958/kstest_cli.py retractable --device 0
            ```

## 설정

*   **KSB7958:** `KSB7958/conf.json` 파일에서 Modbus 서버의 IP 주소(`modbus_ip`)와 포트(`modbus_port`)를 설정할 수 있습니다.
*   **extra:** `extra/conf.json` 파일에서 API의 기본 URL(`url`)과 API 키(`apikey`)를 설정할 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.
