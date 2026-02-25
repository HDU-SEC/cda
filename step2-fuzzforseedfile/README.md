# Step 2 — Input Generation via Fuzzing
For each identified gadget, we generate an input that can trigger the gadget execution path.

Specifically:

- We hook the MMIO read/write functions to monitor the input flow.
- We insert a deliberate crash (e.g., an assertion or abort) in the destination (`dst`) function.

When fuzzing reaches the destination function along the expected path, the program intentionally crashes.  
The fuzzer then saves the corresponding input as a **seed file**, which contains the complete sequence of inputs delivered to the program.

---



Use Fuzz to get the mmio sequence which can trigger the gadget

take the gadget below as example:

```
ehci_work_bh -> ehci_advance_periodic_state -> ehci_advance_state -> ehci_state_execute -> ehci_execute -> usb_packet_map
```

##compile afl
```bash
cd afl-2.52b
make
make install
```
##compile qemu
- Get QEMU source code (Take [QEMU 9.1.2] as an example)

- Move `fuzz-util.h` and `hook-write.h` to QEMU_DIR/include

- Move `memory.c` to QEMU_DIR/softmmu

- Insert `#include "fuzz-util.h"` into the target device's code (depends on what device to test, such as QEMU_DIR/hw/usb/hcd-ohci.c)

- Compile QEMU

```bash
./configure --enable-debug --enable-sanitizers --enable-gcov --cc=./afl-2.52b/afl-gcc --target-list=x86_64-softmmu
make -j8

mkdir in out
touch seed_file
```

##fuzz
Take hcd-ehci as an exmaple

```bash
./fuzz.sh
```

 after the process died by a manual setting crash we get the input(seed_file) which can trigger the gadget

