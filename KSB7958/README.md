# KSTEST - Modbus 장치 제어 CLI

이 도구는 스위치, 개폐 장치, 양액 공급 시스템 등 다양한 Modbus 장치를 테스트하고 제어하기 위한 명령줄 인터페이스입니다.

## 사용법

스크립트는 두 가지 모드로 실행할 수 있습니다: 명령줄 인자 모드와 대화형 모드.

### 1. 명령줄 인자 모드

장치 유형과 특정 장치 인덱스를 직접 지정하여 테스트를 즉시 실행할 수 있습니다.

**구문:**
```bash
python3 kstest_cli.py [type] [--device DEVICE_INDEX]
```

**인자:**
*   `type`: 테스트할 장치의 유형입니다.
    *   `switch`: 팬, 순환 펌프, CO2 등과 같은 장치.
    *   `retractable`: 천창, 스크린, 보온 커튼과 같은 개폐 장치.
    *   `nutsupply`: 양액 공급 시스템.
*   `--device DEVICE_INDEX` (선택 사항): 테스트할 특정 장치의 인덱스입니다. 생략하면 지정된 유형의 모든 장치가 테스트됩니다. (`switch` 및 `retractable` 유형에 적용 가능)

**예시:**

*   **모든 `switch` 장치 테스트:**
    ```bash
    python3 kstest_cli.py switch
    ```

*   **두 번째 `retractable` 장치(인덱스 1) 테스트:**
    ```bash
    python3 kstest_cli.py retractable --device 1
    ```

*   **`nutsupply` 시스템 테스트:**
    ```bash
    python3 kstest_cli.py nutsupply
    ```

### 2. 대화형 모드

인자 없이 스크립트를 실행하면 대화형 모드로 진입합니다. 도구가 사용 가능한 옵션을 안내합니다.

**시작 방법:**
```bash
python3 kstest_cli.py
```

실행 후, 도구는 다음을 안내합니다:
1.  장치 유형(`switch`, `retractable`, `nutsupply`) 선택.
2.  인덱스로 특정 장치를 선택하거나 모든 장치를 테스트하도록 선택.

테스트가 완료된 후, 다른 테스트를 수행할지 묻는 메시지가 표시되어 연속적인 작업이 가능합니다.
