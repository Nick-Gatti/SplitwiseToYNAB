FROM python:latest
WORKDIR /SplitwiseToYNAB
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python","./SplitwiseToYNAB.py"]