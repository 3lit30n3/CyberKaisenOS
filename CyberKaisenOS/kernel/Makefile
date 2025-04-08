obj-m += phixeo_module.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

install:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules_install
	depmod -a
	mkdir -p /etc/modules-load.d/
	echo "phixeo_module" > /etc/modules-load.d/phixeo.conf

uninstall:
	rm -f /etc/modules-load.d/phixeo.conf
	rm -f /lib/modules/$(shell uname -r)/extra/phixeo_module.ko
	depmod -a
