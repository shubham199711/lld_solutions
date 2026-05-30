class VM:
    def __init__(self):
        self.cpu = None
        self.disk = None
        self.ram = None
        self.monitor = None

    def __str__(self):
        return f"{self.cpu=} {self.ram=} {self.disk=} {self.monitor=}"

class VMBuilder:
    def __init__(self):
        self.vm = VM()
    
    def add_cpu(self, cpu):
        self.vm.cpu = cpu
        return self
    
    def add_ram(self, ram):
        self.vm.ram = ram
        return self
    
    def add_disk(self, disk):
        self.vm.disk = disk
        return self

    def add_monitor(self, monitor):
        self.vm.monitor = monitor
        return self
    
    def build(self):
        return self.vm


vm = VMBuilder().add_cpu("1").add_disk("1tb").add_ram("16gb").add_monitor("4k").build()

print(vm)