# Step 3 — PoC Reconstruction
The seed file obtained in Step 2 allows fuzzing to trigger the gadget, but it is not yet a standalone executable PoC.

To reconstruct an executable PoC:

1. Attach GDB to the fuzzing process.
2. Set breakpoints at the MMIO read/write functions.
3. For each breakpoint hit, record:
   - the address
   - the offset
   - the value

We then assemble these recorded operations into a deterministic sequence of MMIO read/write actions and embed them into a PoC template.

The result is a standalone executable program that reliably triggers the target gadget



Notice:This step can be merged into step 2 to directly generate the poc or execute separately.

#### (1) Recording Inputs

```shell
cd ./record/
# Set the breakpoint in line 4 of `fuzz-record.sh` to the target function.
nano ./fuzz-record.sh
./fuzz-record.sh
```

```c++
# QEMUDIR/include/fuzz-util.h
#modify fuzzing_entry funciton
void fuzzing_entry(void) {
    _afl_start();
    hwaddr reg;
    uint64_t val;
    unsigned access_size, index;
    cur_file_offset = 0;
    for(int i=0; i<ops_number; i++) {
        read_from_testcase(&reg, sizeof(hwaddr));
        read_from_testcase(&val, sizeof(uint64_t));
        read_from_testcase(&index, sizeof(unsigned));
        access_size = access_sizes[index % sizeof(access_sizes)];
        if(access_size < min_access_size[i] || access_size > max_access_size[i])
            access_size = min_access_size[i];
        read_ops[i](opaque_ops[i], reg % size_ops[i] - reg % access_size, access_size);
        write_ops[i](opaque_ops[i], reg % size_ops[i] - reg % access_size, val, access_size);
    }
    _afl_stop();
    timer_mod(fuzz_timer, qemu_clock_get_ns(QEMU_CLOCK_VIRTUAL));
    if(exec_times++>10000) {
        __gcov_dump();
        exec_times = 0;
    }
    return;
}
```

This step generates an `mmio.log` file, which records the concrete read/write operations invoked within `fuzzing_entry()`, along with their corresponding parameters.

#### (2) reproduce

Locate the offsets of `mem_cpas`, `mem_opreg`, and `mem_ports`.
```shell
p/x (*(EHCIState*)0)->capsbase
p/x (*(EHCIState*)0)->opregbase
p/x (*(EHCIState*)0)->portscbase
```
Update the macros in `poc.c` according to the resolved addresses.
```shell
cd poc
gcc -o -g poc poc.c
```
Start the guest VM.
```shell
cd repro
./repro.sh
```
Execute the following command inside the guest VM:
```shell
# Mount the shared folder inside the guest VM.
mkdir /mnt/host
mount -t 9p -o trans=virtio hostshare /mnt/host
cd /mnt/host
# Reproduce
./poc mmio.log
```