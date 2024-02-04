FROM ubuntu:18.04

WORKDIR /opt/hercules/tk4/

RUN apt-get update && \
  apt-get install -y unzip wget binutils && \
  wget http://wotho.ethz.ch/tk4-/tk4-_v1.00_current.zip && \
  unzip tk4-_v1.00_current.zip && \
  rm tk4-_v1.00_current.zip && \
  apt-get -y purge wget unzip && \
  apt-get -y autoclean && apt-get -y autoremove && \
  apt-get -y purge $(dpkg --get-selections | grep deinstall | sed s/deinstall//g) && \
  rm -rf /var/lib/apt/lists/*

EXPOSE 3270 8038

ENTRYPOINT [ "./mvs" ]
