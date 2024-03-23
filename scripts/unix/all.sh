#!/bin/bash

scripts/unix/makemigrations.sh
scripts/unix/migrate.sh
scripts/unix/collectstatic.sh
scripts/unix/runserver.sh
