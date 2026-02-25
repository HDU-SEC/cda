
 import cpp
 
 predicate isCallFunction(Function func) {
  func.getName() = "xhci_port_write"
   }
 
 predicate isTargetFunction(Function func) {
 func.getName() = "dma_memory_write"
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
     or
     caller = target
   }
 
 
   from Function startFunction, Function targetFunction, Function tmpFunction1, Function tmpFunction2
 where 
   isTargetFunction(targetFunction) and
   callsTargetFunction(startFunction, targetFunction) and isCallFunction(startFunction) and callsTargetFunction(startFunction,tmpFunction1) and callsTargetFunction(tmpFunction1,targetFunction)
   and callsTargetFunction(startFunction,tmpFunction2) and callsTargetFunction(tmpFunction2,targetFunction) and tmpFunction2.calls(tmpFunction1)
 select tmpFunction2.getName() + "->" + tmpFunction1.getName()
