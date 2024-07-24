FROM mariadb:11.4 as mariadb_image
RUN apt-get update && apt-get install -y mariadb-server
EXPOSE 3306
CMD ["mariadbd"]