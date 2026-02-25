import cpp

 class MMIOFn extends Function {
     MMIOFn() {
     exists(Variable gv |
     gv.getFile().getAbsolutePath().regexpMatch(".*/hw/.*") and
     gv.getType().getName().regexpMatch(".*MemoryRegionOps.*") and
     //gv.getName().regexpMatch(".*mmio.*") and
     gv.getInitializer().getExpr().getChild(1).toString() = this.toString()
     )
     }
     }

     from MMIOFn entry_fn
     select entry_fn

// import cpp

// from FunctionCall call, Function target, Expr arg3
// where
//   target.getName() = "memory_region_init_io" and
//   call.getTarget() = target and
//   call.getArgument(2) = arg3  // 第三个参数，索引从0开始
// select call, arg3, arg3.toString()

// import cpp

// from FunctionCall call, Function target, Expr arg3, GlobalVariable gv, Expr secondField
// where
//   target.getName() = "memory_region_init_io" and
//   call.getTarget() = target and
//   call.getArgument(2) = arg3 and
//   // 变量具有初始化表达式，且提取第 2 个字段（索引从 0 开始）
//   exists(Expr init = gv.getInitializer().getExpr() |
//     secondField = init.getChild(1)  // 第二个字段，如 .write
//   )
// select call, arg3.toString(), gv.getName(), secondField.toString()