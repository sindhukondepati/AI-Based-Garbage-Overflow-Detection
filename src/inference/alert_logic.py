# src/inference/alert_logic.py

def get_alert(label: str) -> str:
    """
    Returns alert message based on predicted label.
    Currently no SMS logic included.
    """
    if label == "overflow":
        return "🚨 Garbage bin is OVERFLOWING!Please collect the Garbage"
    elif label == "full":
        return "⚠️ Garbage bin is FULL!Ready to be collected"
    elif label == "half":
        return "🟡 Garbage bin is HALF filled"
    else:
        return "✅ Garbage bin is EMPTY"
