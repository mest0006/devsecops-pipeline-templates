FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app
COPY app.py /app/app.py
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["python3", "/app/app.py"]
