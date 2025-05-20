CC = gcc
CFLAGS = -fno-stack-protector  -no-pie -Wl,-z,norelro
TARGET = converter
SRC = converter.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)
