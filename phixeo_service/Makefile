CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = phixeo_service

all: $(TARGET)

$(TARGET): phixeo_service.c
	$(CC) $(CFLAGS) -o $@ $<

install: $(TARGET)
	cp $(TARGET) /usr/local/bin/
	cp phixeo.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable phixeo.service
	systemctl start phixeo.service

uninstall:
	systemctl stop phixeo.service
	systemctl disable phixeo.service
	rm -f /etc/systemd/system/phixeo.service
	rm -f /usr/local/bin/$(TARGET)
	systemctl daemon-reload

clean:
	rm -f $(TARGET)
