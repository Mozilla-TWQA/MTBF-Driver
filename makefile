# Download and install all dependencies packages
#

device-id-in-forwardlist := $(shell adb forward --list | wc -l)

install: install-pip install-virtual-env create-virtual-env exec-setup get-b2g-install-b2gtool
	@echo Install Complete

update: update-mtbf-install update-gaia-install
	@echo Update Complete

run: create-adb-forward
	@. mtbf-driver-env/bin/activate; \
	MTBF_TIME=10m MTBF_CONF=mtbf_driver/conf/local.json mtbf --address=localhost:2828 --testvars=mtbf_driver/testvars.json mtbf_driver/tests/test_dummy_case.py	

create-adb-forward:
ifeq ($(device-id-in-forwardlist), 0)
	@echo Create new forward list for device 
	@adb forward tcp:2828 tcp:2828
else
	@echo Clean all devices in forward list
	@adb forward --remove-all
endif

update-mtbf-install:
	@. ./mtbf-driver-env/bin/activate; \
	git pull -u;\
	python setup.py install

update-gaia-install:
	@. ./mtbf-driver-env/bin/activate; \
	cd gaia; \
	git pull -u; \
	cd tests/python/gaia-ui-tests/; \
	python setup.py install

get-b2g-install-b2gtool:
	@git clone https://github.com/mozilla-b2g/B2G
	@cp -r B2G/tools .
	@rm -rf B2G
	@touch tools/__init__.py

get-gaia-install:
	@. ./mtbf-driver-env/bin/activate; \
	git clone https://github.com/mozilla-b2g/gaia;\
	cd gaia/tests/python/gaia-ui-tests/; \
	python setup.py install

exec-setup:
	. ./mtbf-driver-env/bin/activate; \
	python setup.py install	

create-virtual-env:
	@virtualenv mtbf-driver-env

install-virtual-env:
	@sudo pip install --upgrade virtualenv 

install-pip:
	@sudo apt-get install python-pip python-dev build-essential 
