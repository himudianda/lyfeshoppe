import babel
from babel.dates import get_timezone


def format_datetime(value, format='medium'):
    pacific = get_timezone('US/Pacific')
    if format == 'full':
        format = "EEEE, d. MMMM y 'at' h:m a"
    elif format == 'medium':
        format = "MM/dd/yy h:mm a"  # look at babel time documentation for formatting
    elif format == 'time-only':
        format = "h:mm a"  # look at babel time documentation for formatting
    return babel.dates.format_datetime(value, format, tzinfo=pacific)
