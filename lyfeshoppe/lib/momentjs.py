from jinja2 import Markup


# Trick from: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-dates-and-times
# Under section: Integrating moment.js
class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        _markup = '<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.0/moment.min.js" type="text/javascript"></script>'

        markup = _markup + "<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (
                                self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format)

        return Markup(markup)

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
