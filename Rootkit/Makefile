#obj-m += hello.o
#obj-m += reboot_blocker.o
obj-m += hide_file.o
#obj-m += chdir.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
  
