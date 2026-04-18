def calculate_confidence(result):
    if "restart" in result.lower():
        return 85
    elif "memory" in result.lower():
        return 80
    else:
        return 70
