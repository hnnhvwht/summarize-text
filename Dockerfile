FROM python:3
LABEL maintainer="hannah.white@tutanota.com"
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt \
  && python -m spacy download en_core_web_sm
COPY . .
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["api.py"]
