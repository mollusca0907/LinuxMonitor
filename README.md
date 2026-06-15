# Raspberry Pi System Monitor

라즈베리 파이 환경에 최적화된 실시간 리소스 모니터링 대시보드입니다. 저사양 SBC(Single Board Computer) 환경에서 발생할 수 있는 발열 문제와 백그라운드 프로세스의 자원 독점 문제를 해결하기 위해 제작되었습니다.

## 1. 주요 기능
- **실시간 리소스 시각화**: Socket.io를 활용해 1초 단위로 CPU 사용량, RAM 점유율을 그래프로 출력
- **하드웨어 온도 모니터링**: `/sys/class/thermal` 시스템 파일을 직접 참조하여 정밀한 CPU 온도 측정 및 75도 이상 시 시각적 경보 제공
- **프로세스 프로파일링**: 시스템 자원을 가장 많이 소모하는 상위 3개 프로세스를 실시간으로 식별

## 2. 기술 스택
- **Backend**: Python 3.x, Flask, Flask-SocketIO, psutil
- **Frontend**: Vanilla JS, Chart.js, Tailwind CSS
- **Performance**: Eventlet을 통한 비동기 I/O 처리 최적화

## 3. 트러블슈팅 사례: 리소스 병목 현상 진단 및 최적화

프로젝트 초기 가동 중 CPU 점유율 350% 초과 및 온도 83°C 급증 현상을 발견하여 이를 해결한 과정입니다.

- **문제 진단**: 직접 구현한 'Top Processes' 모니터링 기능을 통해 VS Code Remote-SSH 서버의 파일 인덱싱 프로세스인 `rg(ripgrep)`가 쿼드코어 자원 전체를 점유하고 있음을 실시간으로 파악했습니다.
- **원인 분석**: 저사양 SBC 환경에서는 대규모 라이브러리(venv 등)에 대한 자동 인덱싱 작업이 하드웨어 스로틀링(Throttling) 및 과열을 유발하는 병목 지점임을 식별했습니다.
- **해결 방안**: 일반적인 설정 변경만으로는 프로세스가 재발하는 특성을 고려하여, 해당 바이너리에 대한 실행 권한을 제어(`chmod -x`)하는 공격적인 최적화를 수행했습니다.
- **결과**: **CPU 점유율을 10% 미만으로, 시스템 온도를 약 30°C 하향 안정화** 시켰으며, 모니터링 도구가 실제 시스템 안정화에 기여하는 유효성을 검증했습니다.

## 4. 설치 및 실행 방법

### 의존성 설치
가상환경 활성화 후 필요한 라이브러리를 설치합니다.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
