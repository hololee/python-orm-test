# python-ORM-test

## 환경 설정

### 가상환경

([참고](https://docs.python.org/3/library/venv.html))

```Shell
python3 -m venv .venv/orm-test
source .venv/orm-test/bin/activate
```

### 패키지

패키지 환경 설정 ([참고](https://medium.com/packagr/using-pip-compile-to-manage-dependencies-in-your-python-packages-8451b21a949e))

```Shell
pip3 install pip-tools
pip-compile requirements.in # 의존성 계산.
pip3 install -r requirements.txt
```

### commit convention

([참고](https://sxxk2.tistory.com/18?category=1085044))

```Shell
pre-commit install
pre-commit autoupdate # 변경한 경우 업데이트.
pre-commit run -a # 모든 파일 검사.
```

