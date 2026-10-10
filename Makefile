.PHONY: serve build check

serve:
	./bin/docgen serve

build:
	./bin/docgen build --release

check: build
	git check-ignore bin/docgen site/index.html
