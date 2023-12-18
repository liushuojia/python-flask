
.PHONY:all run pip help

all: run

run:
	python3.9 app.py

pip:
	pip3.9 install flask
	pip3.9 install sqlalchemy
	pip3.9 install redis

help:
	@echo "make help - 查看帮助"
	@echo "make all - 执行文件"
	@echo "make run - 启动"
	@echo "make venv"
