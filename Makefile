
.PHONY:all run install help git

all: run

run:
	python3.9 app.py

install:
	pip3.9 install -r requirements.txt

git:
	git add .
	git commit -m "change"
	git push

help:
	@echo "make help - 查看帮助"
	@echo "make all - 执行文件"
	@echo "make run - 启动"
	@echo "make venv"
