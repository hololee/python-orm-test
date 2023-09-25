# python-ORM-test

## 환경 설정

### 가상환경

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
