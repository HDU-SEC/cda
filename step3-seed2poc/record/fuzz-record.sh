AFL_Fuzzing=1 pwndbg -x ./record.gdb \
--arg PATH/afl-2.52b/afl-fuzz \
  -t 5000+ -i ./in -o ./out -m none -f seed_file -- \
  QEMU_DIR/build/qemu-system-x86_64 \
  -display none \
  -device usb-ehci,id=ehci \
  -device usb-tablet,bus=ehci.0,port=1,id=usbdev1