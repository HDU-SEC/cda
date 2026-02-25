#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <ctype.h>
#include <inttypes.h>

typedef uint64_t hwaddr;

#define EHCI_BASE 0xfebf2000
#define EHCI_SIZE 0x1000

void *ehci_mmio_base;

#define CAPS_OFFSET  0x00  // p/x (*(EHCIState*)0)->capsbase
#define OPREG_OFFSET 0x20  // p/x (*(EHCIState*)0)->opregbase
#define PORTS_OFFSET 0x44  // p/x (*(EHCIState*)0)->portscbase

void *mem_map(const char *dev, size_t offset, size_t size) {
    int fd = open(dev, O_RDWR | O_SYNC);
    if (fd == -1) {
        return 0;
    }

    void *result = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, offset);
    if (!result) {
        close(fd);
        return 0;
    }

    close(fd);
    return result;
}

char *trim(char *str) {
    while (isspace(*str)) str++;
    if (*str == 0) return str;

    char *end = str + strlen(str) - 1;
    while (end > str && isspace(*end)) end--;
    *(end + 1) = '\0';
    return str;
}

void ehci_write(hwaddr addr, uint32_t value) {
    *(uint32_t *)(ehci_mmio_base + addr) = value;
}

uint32_t ehci_read(uint64_t addr) {
    return *(uint32_t *)(ehci_mmio_base + addr);
}

void parse_and_execute(const char *line) {
    char fname[64];
    uint64_t opaque = 0;
    hwaddr addr = 0;
    uint32_t val = 0;
    unsigned size = 0;

    if (sscanf(line, "%[^'(](%" SCNx64 ", %" SCNx64 ", %" SCNx32 ", %d)",
               fname, &opaque, &addr, &val, &size) == 5) {
        // full format with value
    } else if (sscanf(line, "%[^'(](%" SCNx64 ", %" SCNx64 ", %d)",
                      fname, &opaque, &addr, &size) == 4) {
        // read-only format
    }

    uint64_t result;
    if (strstr(fname, "caps_read")) {
        addr = addr + CAPS_OFFSET;
        result = ehci_read(addr);
        printf("[caps_read]   addr=0x%lx => 0x%lx\n", addr, result);
    } else if (strstr(fname, "caps_write")) {
        addr = addr + CAPS_OFFSET;
        ehci_write(addr, val);
        printf("[caps_write]  addr=0x%lx val=0x%x\n", addr, val);
    } else if (strstr(fname, "opreg_read")) {
        addr = addr + OPREG_OFFSET;
        result = ehci_read(addr);
        printf("[opreg_read]  addr=0x%lx => 0x%lx\n", addr, result);
    } else if (strstr(fname, "opreg_write")) {
        addr = addr + OPREG_OFFSET;
        ehci_write(addr, val);
        printf("[opreg_write] addr=0x%lx val=0x%x\n", addr, val);
    } else if (strstr(fname, "port_read")) {
        addr = addr + PORTS_OFFSET;
        result = ehci_read(addr);
        printf("[port_read]   addr=0x%lx => 0x%lx\n", addr, result);
    } else if (strstr(fname, "port_write")) {
        addr = addr + PORTS_OFFSET;
        ehci_write(addr, val);
        printf("[port_write]  addr=0x%lx val=0x%x\n", addr, val);
    }
}

int main(int argc, char *argv[]) {
    ehci_mmio_base = mem_map("/sys/bus/pci/devices/0000:00:05.0/resource0", 0, EHCI_SIZE);
    if (!ehci_mmio_base) {
        return 0;
    }

    FILE *fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen");
        return 1;
    }

    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        char *clean = trim(line);
        if (*clean == '\0') continue;
        parse_and_execute(clean);
    }

    fclose(fp);
    return 0;
}
