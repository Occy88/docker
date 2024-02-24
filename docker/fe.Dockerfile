# Stage 1: Node.js stage for installing Node.js, Yarn, and other dependencies
FROM node:18 AS nodebase

# Install Yarn globally
RUN npm install -g yarn --force

# Stage 2: Final image based on octo_base
FROM octo_base

# Copy Node.js and Yarn from the nodebase stage
COPY --from=nodebase /usr/local/bin /usr/local/bin
COPY --from=nodebase /usr/local/lib /usr/local/lib

# You might need to adjust permissions or perform additional steps depending on octo_base setup
# Ensure the copied binaries and libraries are correctly accessible

# Set the entrypoint
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
