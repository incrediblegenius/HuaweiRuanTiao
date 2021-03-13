from Server import VM

class RuningVM():
    def __init__(self,vm:VM,id:int) -> None:
        self.vm = vm
        self.id = id
        