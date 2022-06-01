FROM pytorch/pytorch:latest

RUN apt-get update \
    && apt-get install -y \
        libgl1-mesa-glx \
        libx11-xcb1 \
    && apt-get clean all \
    && rm -r /var/lib/apt/lists/*

RUN pip install \
    pillow \
    matplotlib \
    fastapi \
    uvicorn \
    python-multipart

COPY src .
EXPOSE 8000

# CMD ["python3", "item_prediction.py"]
ENTRYPOINT ["uvicorn", "item_prediction:app", "--host", "0.0.0.0", "--port", "8000"]
