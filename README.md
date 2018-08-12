## Sandwhichi-django-api repository

Docker 인스턴스를 실행한 후, 해당 명령어를 실행 시켜야 합니다.


```bash
# setup env
$ python3 -m venv .env

# start vitual environments
$ source .env/bin/activate

# install packages
$ pip install -r ./requirements.txt

# install MySQL-python module
$ pip install MySQL-python

# start server 
$ make run
```

로컬 환경 변수를 관리하는 .local-super-secret-env.json 파일을 반드시 생성하고 내용을 채워주세요

```bash
# Copy file
$ cp .local-super-secret-env.json.example .local-super-secret-env.json

# SUPER_SECRET을 모두 채워주세요.
```

첫 배포

```bash
# Copy file
$ zappa deploy {envirment}
```

첫 배포후 업데이트

```bash
# Copy file
$ zappa update {envirment}
```