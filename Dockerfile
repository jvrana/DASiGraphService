FROM tiagopeixoto/graph-tool

RUN mkdir /home/code
ADD . /home/code
WORKDIR /home/code
RUN chmod 666 *
RUN yes Y | pacman -S python-pip
RUN pip install pip --upgrade
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt
#RUN pipenv install --dev --system   # click / pipenv is not compatible with this container due to ACSII locale