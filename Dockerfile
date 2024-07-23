FROM python:3.12.3
WORKDIR .
COPY . .
RUN pip install poetry
RUN peotry install
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

