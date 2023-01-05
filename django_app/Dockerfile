FROM python:3.9.13-slim

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN addgroup --system app && adduser --system --no-create-home --group app
RUN chown -R app:app /home/app && chmod -R 755 /home/app
USER app

WORKDIR /home/app
COPY --chown=app:app ./requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app ./. .