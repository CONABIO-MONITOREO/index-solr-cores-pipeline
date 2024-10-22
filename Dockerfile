FROM python:3.10

WORKDIR /app

COPY ./requirements.txt .
COPY ./megad.py .
COPY ./sipecam_anotationes_cor.py .
COPY ./.env .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

CMD ["python"]