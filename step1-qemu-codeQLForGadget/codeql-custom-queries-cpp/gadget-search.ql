
 import cpp

 class GadgetFn extends Function {
  GadgetFn() {
     this.getName()
     .regexpMatch("address_space_write|address_space_unmap|dma_memory_unmap|dma_memory_write_relaxed|pci_dma_unmap|dma_memory_write|pci_dma_write|dma_buf_read|dma_blk_write|dma_memory_read")
     }
     }

     from GadgetFn gadget_fn
     select gadget_fn