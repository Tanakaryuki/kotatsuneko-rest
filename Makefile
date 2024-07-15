install-package:
	@read -p "Enter package name: " package; \
	docker compose exec oauth_api poetry add $$package

remove-package:
	@read -p "Enter package name: " package; \
	docker compose exec oauth_api poetry remove $$package