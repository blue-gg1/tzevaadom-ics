# syntax=docker/dockerfile:1
FROM fedora:latest

# easy deploy command "echo > /app/code/main.py && vi /app/code/main.py && python /app/code/main.py"
# better docker command "docker build . -t test-ics"

# Set the timezone
ENV TZ="Asia/Jerusalem"
# fuck with the timezone.
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set the working directory
WORKDIR /app

# Make app folders
RUN mkdir /app/code

# Copy the script and requirements for The File
COPY ../main.py /app/code/main.py
COPY ../settings.py /app/code/kan/settings.py
COPY ../requirements.txt /app/code/requirements.txt

# update the system
RUN dnf upgrade --assumeyes
# install app dependencies
RUN dnf install --assumeyes python3 python3-pip
# install some debug apps
RUN dnf install --assumeyes which file htop

# once CRON is installed copy the cron file
RUN touch /var/spool/cron/root
COPY ./CronTab.cron /var/spool/cron/root
RUN chmod 0644 /var/spool/cron/root

# install all the python items
# upgrade pip
RUN python -m pip install --upgrade pip
# install all the pip packages
RUN pip install -r /app/code/requirements.txt --resume-retries 10

# fuck with the timezone again in order to make sure no updates unfucked with the timezone when we fucked with the timezone last time
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# run the cronjob
CMD ["crond", "-n"]