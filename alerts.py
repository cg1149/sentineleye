from plyer import notification

def send_alert(threat_level, description):
    if threat_level == "LOW":
        return

    title = f"🚨 SentinelEye - {threat_level} THREAT"
    message = description[:100]

    notification.notify(
        title=title,
        message=message,
        app_name="SentinelEye",
        timeout=10
    )
    print(f"Alert sent: {title}")

if __name__ == "__main__":
    send_alert("HIGH", "Exposed API key detected in terminal window!")
