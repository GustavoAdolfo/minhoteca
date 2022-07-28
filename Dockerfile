FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip && pip --version
RUN mkdir /minhoteca
WORKDIR /minhoteca
COPY requirements.txt /minhoteca/
COPY ./ /minhoteca/
RUN pip install -r requirements.txt && ls -la && chmod -R 777 /minhoteca/setup.sh
EXPOSE 80
ENTRYPOINT [ "/minhoteca/setup.sh" ]
CMD bash
