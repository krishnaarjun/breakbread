FROM node:10.15.3
ARG BUILD_DATE
ARG VCS_REF

# Traceability to source code
LABEL org.label-schema.build-date=$BUILD_DATE \
org.label-schema.vcs-ref=$VCS_REF \
org.label-schema.vcs-url="https://github.com/inmar/breakbread.git" \
org.label-schema.vendor="Inmar Inc."
ADD . /code/
WORKDIR /code
RUN npm install

