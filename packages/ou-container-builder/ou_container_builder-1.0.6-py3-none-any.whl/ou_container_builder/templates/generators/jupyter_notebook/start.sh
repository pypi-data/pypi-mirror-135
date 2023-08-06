#!/bin/bash

set -e

{% if flags and flags.ou_container_content %}
ou-container-content startup
{% endif %}

if [[ ! -z "${JUPYTERHUB_API_TOKEN}" ]]; then
    exec jupyterhub-singleuser --ip=0.0.0.0 --port 8888 --NotebookApp.config_file=/etc/jupyter/jupyter_notebook_config.py
else
    exec jupyter notebook --NotebookApp.config_file=/etc/jupyter/jupyter_notebook_config.py
fi

{% if flags and flags.ou_container_content %}
ou-container-content shutdown
{% endif %}
