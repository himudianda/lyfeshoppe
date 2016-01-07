import babel


def format_datetime(value, format='medium'):
    if format == 'full':
        format = "EEEE, d. MMMM y 'at' h:m a"
    elif format == 'medium':
        format = "MM/dd/yy h:mm a"  # look at babel time documentation for formatting
    return babel.dates.format_datetime(value, format)
