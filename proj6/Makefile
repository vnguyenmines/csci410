OUT = Assembler

all: 
	cargo build --release
	cp target/release/proj6 ./$(OUT)

debug:
	cargo build

clean:
	cargo clean
	find . -name "*.hack" -type f -delete
	rm ./$(OUT)