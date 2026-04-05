from twin_manager import inject_failure


def cpu_spike():
    return inject_failure("cpu")


def crash():
    return inject_failure("crash")


def memory_leak():
    return inject_failure("memory")
