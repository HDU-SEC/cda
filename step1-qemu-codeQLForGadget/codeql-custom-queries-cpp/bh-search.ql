import cpp

class BHTFn extends Function {
    BHTFn() {
    exists(FunctionCall fc |
    fc.getTarget().getName().regexpMatch("qemu_bh_new_full|timer_new_ns") and
    fc.getFile().getAbsolutePath().regexpMatch(".*/hw/.*") and
    (fc.getChild(0).toString() = this.toString() or fc.getChild(1).toString() =
    this.toString())
    )
    }}

from BHTFn bh_fn
select bh_fn

    