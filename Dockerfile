FROM python:3-slim
RUN python3 -m pip install --upgrade pip
CMD [ "/bin/bash" ]
    