# Getting the Image from the registry docker odoo
FROM registry-gitlab.horanet.com:4567/horanet/docker/odoo:latest

USER root

ARG CI_JOB_TOKEN

# Installing package
RUN apt-get update
RUN apt-get install -y --no-install-recommends git && \
    apt-get install -y openssh-client && \
    apt-get install -y npm && \
    ln -s /usr/bin/nodejs /usr/bin/node

# Install less
RUN npm install -g less

# Update pip version
RUN pip install --upgrade pip

# Install pip dependencies : coverage
RUN pip install coverage

# Copy project sources in odoo addons directory (for installation and volume creation)
WORKDIR /opt/odoo-addons
COPY ./ payment_autopay/
WORKDIR /opt/odoo-addons/payment_autopay/

# Installing package
RUN pip install -e .

# Edit directory rights for Odoo addons directory
RUN chown -R odoo /opt/odoo-addons

# Uninstall no more required packages and empty caches
RUN apt-get remove --purge -y python-pip openssh-client && \
  apt-get clean && apt-get autoremove -y && \
  rm -rf /var/lib/apt && \
  rm -rf /tmp/* && \
  rm -rf /root/.cache

RUN usermod -aG root odoo

USER odoo
