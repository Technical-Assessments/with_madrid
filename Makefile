refactor:
	clear &&\
	git add . &&\
	git commit -m "refactor" &&\
	git push

tidy:
	clear &&\
	pip list --format freeze > requirements.txt

docker-prod:
	clear
	$(info 🔥 Environment: Production 🔥)
	docker system prune -a -f
	docker network prune -f
	docker-compose -f docker-compose.yml stop
	docker-compose -f docker-compose.yml down --remove-orphans
	docker-compose -f docker-compose.yml up --build fsm-production