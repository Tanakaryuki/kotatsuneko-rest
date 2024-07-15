install-package:
	@read -p "Enter package name: " package; \
	docker compose exec kotatsuneko-api poetry add $$package

remove-package:
	@read -p "Enter package name: " package; \
	docker compose exec kotatsuneko-api poetry remove $$package