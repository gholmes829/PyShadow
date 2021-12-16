all:
	g++ -g -std=c++14 stub.cpp -o stub

clean:
	rm -rf *.o gen/

test:
	pytest