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
asmlinkage long (*old_chdir)(const char __user *filename);

static struct kprobe kp = {
    .symbol_name = "kallsyms_lookup_name"
};

typedef unsigned long (*kallsyms_lookup_name_t)(const char *name);
unsigned long * get_system_call_table_address(void){
    kallsyms_lookup_name_t kallsyms_lookup_name;
    register_kprobe(&kp);
    kallsyms_lookup_name = (kallsyms_lookup_name_t) kp.addr;
    unregister_kprobe(&kp);
		return (unsigned long*) kallsyms_lookup_name("sys_call_table");
}


asmlinkage long hackers_chdir(const char __user *filename){
		long num_bytes;
		
		printk(KERN_NOTICE "chdir: called hacker fn");
		
		num_bytes = old_chdir(filename);
		

		printk(KERN_NOTICE "chdir: exit hacker fn");


		return num_bytes;
}

void hook_sys_call(void){
    printk(KERN_NOTICE "chdir: hooking sys call");


    disable_write_protection();
  	old_chdir = (long int (*)(const char __user *)) sys_call_table_address[__NR_chdir];
    if (!old_chdir) return;
    
    sys_call_table_address[__NR_chdir] = (unsigned long) hackers_chdir;
		enable_write_protection();
  
    printk(KERN_NOTICE "chdir: Hooked sys Call");

}

void restore_getdents_sys_call(void){
    disable_write_protection();
		sys_call_table_address[__NR_chdir] = (unsigned long) old_chdir;
		enable_write_protection();
}

static int startup(void){
    printk(KERN_NOTICE "chdir: startup");

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

