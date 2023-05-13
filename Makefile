r=python3
p=pip
d=docker
container_name=wikidataru
container_alias=parsing

venv: venv/touchfile

data:
	wget https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz
	tar -xvzf cifar-100-python.tar.gz

venv/touchfile: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -r requirements.txt
	touch venv/touchfile

test: venv
	. venv/bin/activate; python test/app.test.py

run: venv
	. venv/bin/activate; cd app; flask run

clean:
	rm -rf venv/
	find . -iname "*.pyc" -delete

imageRecognizer: 
	docker build  $(container_alias)-$(container_name) rns .
	docker run -p $(addr):$(p):$(p)/udp -p $(addr):$(p):$(p)/tcp --name $(container_alias) $(container_name)