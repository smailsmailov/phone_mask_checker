FROM python

WORKDIR "/work_dir/"

COPY requirements.txt ./

RUN pip install -r requirements.txt