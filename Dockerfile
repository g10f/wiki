FROM ubuntu:20.04

ENV WORKDIR=/opt/g10f/wiki
ENV WIKI_DATA_DIR=/opt/g10f/wiki/data
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=$WORKDIR/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/opt/g10f/wiki/apps
ENV MOINLOGGINGCONF=/opt/g10f/wiki/apps/server/logfile

ARG USERNAME=worker
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
#RUN groupadd --gid $USER_GID $USERNAME \
#    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN apt-get update -y && apt-get -y install  \
    antiword \
    catdoc \
    libxapian30 \
    python-xapian \
    poppler-utils \
    locales \
    virtualenv && apt-get clean

# Set the locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR $WORKDIR

COPY requirements.txt .

RUN virtualenv --python="/usr/bin/python2.7" --system-site-packages $VIRTUAL_ENV && \
    . ${VIRTUAL_ENV}/bin/activate && \
    pip install -U pip wheel && \
    pip install -r requirements.txt

# Open attachment in full window
RUN sed -i "s/querystr\['do'\] = 'view'/querystr['do'] = getattr(self.cfg, 'default_do_action', 'view')/"  \
    venv/lib/python2.7/site-packages/MoinMoin/formatter/text_html.py

## add log dir
RUN mkdir -p ${WORKDIR}/logs

## add data_dir
RUN mkdir -p ${WIKI_DATA_DIR}/static

COPY data data/
COPY apps apps/
COPY Docker/gunicorn.conf.py apps/gunicorn.conf.py

#RUN chown -R $USERNAME: $WORKDIR
#USER $USERNAME

# Start gunicorn
WORKDIR $WORKDIR/apps
CMD ["gunicorn", "server.wsgi:application", "--bind",  "0.0.0.0:8000", "-w", "4"]
EXPOSE 8000
