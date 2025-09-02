# 1. Python 3.13 slim 이미지 사용
FROM python:3.13-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 환경 변수
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PORT=9001

# 4. 시스템 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 5. pyproject.toml과 poetry.lock 복사
COPY pyproject.toml poetry.lock /app/

# 6. Poetry 설치 및 패키지 설치
RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev --no-interaction --no-ansi

RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev --no-interaction --no-ansi

# 7. 앱 소스 전체 복사
COPY . /app

# 8. uvicorn으로 FastAPI 앱 실행
# main.py가 루트 디렉토리에 있으므로 main:app 기준
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
