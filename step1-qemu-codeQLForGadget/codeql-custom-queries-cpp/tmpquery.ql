
 import cpp

 predicate isCallFunction(Function func) {
  func.getName() = "flash_write"
   }
 
 predicate isTargetFunction(Function func) {
 func.getName() = "dma_memory_read"
   }
   
   predicate callsTargetFunction(Function caller, Function target) {
     exists(FunctionCall fc |
       fc.getEnclosingFunction() = caller and
       fc.getTarget() = target
     )
     or
     exists(FunctionCall fc, Function intermediate |
       fc.getEnclosingFunction() = caller and
       fc.getTarget() = intermediate and
       callsTargetFunction(intermediate, target)
     )
   }
 
 
   from Function startFunction, Function targetFunction, Function tmpFunction
 where 
   isTargetFunction(targetFunction) and
   callsTargetFunction(startFunction, targetFunction) and isCallFunction(startFunction) and callsTargetFunction(startFunction,tmpFunction) and callsTargetFunction(tmpFunction,targetFunction)
 select tmpFunction
 /*   from Function func, FunctionCall call
   where 
     isTargetFunction(func) and
     call.getEnclosingFunction() = func
   select func, call, "Function call in $@ located at $@.", call.getTarget().getName(), call.getLocation() */
 
 /* 
 from MMIOFn entry_fn, ReentryFn end_fn
 where edges+(entry_fn, end_fn)
 select end_fn, entry_fn, end_fn, "MMIO -> Reentry: from " + entry_fn.getName() + " to " +
 end_fn.getName() */