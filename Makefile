refactor:
	clear &&\
	git add . &&\
	git commit -m "refactor" &&\
	git push

tidy:
	clear &&\
	pip list --format freeze > requirements.txt