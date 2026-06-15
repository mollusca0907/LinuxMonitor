Raspberry Pi System Monitor

라즈베리 파이 전용 실시간 리소스 모니터링 대시보드입니다. SBC(Single Board Computer) 환경의 특성상 발열과 자원 관리가 필수적이기 때문에, 실시간 온도 추적과 리소스를 과다 점유하는 프로세스를 식별하는 데 중점을 두었습니다.
핵심 기능

    실시간 데이터 스트리밍: Socket.io를 이용해 1초 단위로 CPU, RAM, 온도 데이터 전송

    프로세스 추적: 현재 시스템 자원 점유 상위 3개 프로세스 정보 제공

    고온 경보: CPU 온도 75도 이상 시 UI 강조를 통한 하드웨어 보호 알림

기술 스택

    Backend: Python, Flask, Flask-SocketIO, psutil

    Frontend: Vanilla JS, Chart.js, Tailwind CSS

    Server: Eventlet (비동기 처리 최적화)

트러블슈팅: VS Code 인덱싱 부하 해결

프로젝트 초기 구동 시 CPU 사용량이 350%를 초과하고 온도가 83°C까지 급상승하는 현상이 발생했습니다.

    원인 파악: 개발한 'Top Processes' 모니터링 기능을 통해 VS Code Remote-SSH의 파일 인덱싱 프로세스(rg)가 모든 코어 자원을 점유하고 있음을 확인했습니다.

    조치: .gitignore 설정만으로 해결되지 않는 저사양 환경 특성을 고려하여, 해당 바이너리의 실행 권한을 제어(chmod -x)하는 방식으로 프로세스를 강제 차단했습니다.

    결과: 조치 후 CPU 점유율은 10% 미만으로, 온도는 50°C 대의 정상 범위로 안정화되었습니다.

단순한 상태 출력을 넘어, 실제 시스템 장애를 진단하고 하드웨어 가용성을 확보하는 모니터링 도구의 효용성을 확인한 사례입니다.
실행 방법

    가상환경 설정 및 라이브러리 설치
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    서버 실행
    python app.py

    접속
    브라우저에서 http://[라즈베리파이-IP]:5000 접속.
