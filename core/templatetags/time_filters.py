from django import template

register = template.Library()

@register.filter
def hour_to_ampm(hour_str):
    try:
        hour = int(hour_str)
        suffix = 'AM' if hour < 12 else 'PM'
        hour_12 = hour if 1 <= hour <= 12 else hour - 12 if hour > 12 else 12
        return f"{hour_12}:00 {suffix}"
    except:
        return hour_str
