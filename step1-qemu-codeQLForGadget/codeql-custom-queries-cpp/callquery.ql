import cpp
 from Function startFunction, Function targetFunction
 where
 startFunction.getName() ="virtio_gpu_handle_ctrl" and targetFunction.getName() = "virtqueue_pop" and startFunction.calls(targetFunction)
 select startFunction,targetFunction