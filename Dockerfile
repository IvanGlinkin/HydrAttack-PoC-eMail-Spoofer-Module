FROM ubuntu:latest

# Set the working directory
WORKDIR /app

# Install necessary packages (modify as needed)
RUN apt-get update && apt-get install -y bash dnsutils postfix python3 python3-pip 

# Copy local files into the container (optional)
COPY . /app

# Install Python requirements
RUN pip3 install --no-cache-dir colorama py-emailprotections --break-system-packages

#Creating chroot
RUN mkdir -p /var/spool/postfix/etc \
    && cp /etc/resolv.conf /var/spool/postfix/etc/ 2>/dev/null || true \
    && cp /etc/hosts /var/spool/postfix/etc/ 2>/dev/null || true \
    && cp /etc/services /var/spool/postfix/etc/ 2>/dev/null || true

# Set the default domain value via an environment variable
ENV USERNAME=spoofed
ENV DOMAIN=spoofed.com
ENV SENDTO=spoofed@spoofed.com
ENV ATTACH=""

# Use bash to enable environment variable expansion
ENTRYPOINT ["bash", "-c", "python3 main.py $DOMAIN"]
