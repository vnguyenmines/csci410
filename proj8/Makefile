OUT = VMTranslator

all: 
	cargo build --release
	cp target/release/proj8 ./$(OUT)

debug:
	cargo build

clean:
	cargo clean
	rm -rf asmtest
	find . -name "*.asm" -type f -delete
	rm ./$(OUT)