#!/bin/bash

set -e


# Espera até que o serviço do MySQL esteja disponível antes de tentar executar comandos
until mysql -h "localhost" -u "root" -p"${MYSQL_ROOT_PASSWORD}" &> /dev/null
do
  printf "."
  sleep 1
done

# Cria o banco de dados
mysql -h "localhost" -u "root" -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE}\`;"

# Cria o usuário e concede as permissões
mysql -h "localhost" -u "root" -p"${MYSQL_ROOT_PASSWORD}" -e "GRANT ALL ON \`${MYSQL_DATABASE}\`.* TO '${MYSQL_USERNAME}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}'; FLUSH PRIVILEGES;"


