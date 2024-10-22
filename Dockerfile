FROM python:3.10

WORKDIR /app

COPY ./megad.py .
COPY ./requirements.txt .
COPY ./sipecam_anotationes_cor.py .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

CMD ["python"]