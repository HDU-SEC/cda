pwndbg -x ./repro.gdb \
--arg QEMUDIR/build/qemu-system-x86_64 \
  -m 2048 \
  -smp 2 \
  #we didn't provide ubuntu.img here 
  -drive format=qcow2,file=./ubuntu.img \
  -nographic \
  -monitor /dev/null \
  -snapshot \
  -no-reboot \
  -enable-kvm \
  -fsdev local,id=fs0,path=../poc,security_model=none \
  -device virtio-9p-pci,fsdev=fs0,mount_tag=hostshare \
  -device usb-ehci,id=ehci \
  -device usb-tablet,bus=ehci.0,port=1,id=usbdev1
