set follow-fork-mode child
set breakpoint pending on
source ./dump.py
#b ehci_caps_write
#b hcd-ehci.c:2218
r