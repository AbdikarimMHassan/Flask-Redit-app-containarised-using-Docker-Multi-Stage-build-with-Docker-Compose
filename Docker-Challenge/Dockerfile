FROM python:3.12-slim AS build
WORKDIR /app
# install flask and redis into a wheel cache for use in prod
RUN pip wheel --wheel-dir=/wheels flask redis


FROM python:3.12-slim AS prod
WORKDIR /app
#copy dependencies from build to prod
COPY --from=build /wheels /wheels
RUN pip install --no-index --find-links=/wheels flask redis
COPY count.py ./
COPY templates ./templates
COPY static ./static
CMD [ "python", "count.py" ]

