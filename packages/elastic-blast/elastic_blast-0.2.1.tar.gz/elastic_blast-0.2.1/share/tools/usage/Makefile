# Makefile for FIXME
# Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
# Created: Sat 27 Nov 2021 03:18:44 PM EST

SHELL=/bin/bash
.PHONY: all clean distclean check

VENV=.env
CONDA_ENV=condastas

all: ${VENV}
	source ${VENV}/bin/activate && \
		pypistats overall elastic-blast
	source ${VENV}/bin/activate && \
		pypistats overall elastic-blast -l
	source ${VENV}/bin/activate && \
		pypistats overall elastic-blast -t
	source ${VENV}/bin/activate && \
		parallel -j1 pypistats overall elastic-blast -m 2021-{} ::: 06 07 08 09 10 11

help: ${VENV}
	source ${VENV}/bin/activate && pypistats --help	
	source ${VENV}/bin/activate && pypistats overall --help	
	source ${VENV}/bin/activate && pypistats recent --help	
	source ${VENV}/bin/activate && pypistats system --help	
	source ${VENV}/bin/activate && pypistats python_major --help	
	source ${VENV}/bin/activate && pypistats python_minor --help	

recent: ${VENV}
	source ${VENV}/bin/activate && pypistats recent elastic-blast

# Report by OS
system: ${VENV}
	source ${VENV}/bin/activate && pypistats system elastic-blast

# Report by python version
py: ${VENV}
	source ${VENV}/bin/activate && pypistats python_major elastic-blast
	source ${VENV}/bin/activate && pypistats python_minor elastic-blast

${VENV}: requirements.txt
	[ -d ${VENV} ] || python3 -m venv $@
	source ${VENV}/bin/activate && pip install -r $^

${CONDA_ENV}:
	#[ -d ${CONDA_ENV} ] || conda create -y -n ${CONDA_ENV} -f environment.yml
	[ -d ${CONDA_ENV} ] || conda create -y -n ${CONDA_ENV}
	conda activate ${CONDA_ENV} && conda install -y -c conda-forge condastats

condastats: ${CONDA_ENV}
	conda activate ${CONDA_ENV} && condastats --help


conda:
	condastats overall elastic-blast
	condastats overall --monthly elastic-blast
	#condastats overall --complete elastic-blast
	condastats pkg_version elastic-blast

overall:
	condastats overall elastic-blast
	source ${VENV}/bin/activate && \
		pypistats overall elastic-blast



clean:
	${RM} -fr ${VENV}
	conda env remove -n ${CONDA_ENV}
