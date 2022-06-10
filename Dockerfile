FROM continuumio/miniconda3

RUN pip install \
    torch \
    torchvision \
    --extra-index-url https://download.pytorch.org/whl/cpu

RUN pip install \
    pillow \
    matplotlib \
    fastapi \
    uvicorn \
    python-multipart

COPY src .
EXPOSE 8000

ENTRYPOINT ["uvicorn", "item_recognition:app", "--host", "0.0.0.0", "--port", "8000"]
