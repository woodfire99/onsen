FROM python:3.10-slim

# 시스템 패키지 업데이트 및 필수 라이브러리 설치
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    xdg-utils \
    libu2f-udev \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libdrm2 \
    libgbm1 \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 작업 디렉토리 설정
WORKDIR /app
COPY . .

# 환경 변수 설정 (chromedriver 경로 명시)
ENV CHROMIUM_BIN=/usr/bin/chromium
ENV PATH="/usr/lib/chromium:$PATH"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
