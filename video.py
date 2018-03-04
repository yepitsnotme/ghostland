class Video:
    def __init__(self, app):
        self.framerate = 24
        self.head = app.cache['video.html']

    def frames():
        width = 80
        height = 24
        frame0 = ('>'*width+'\n')*height
        frame1 = ('<'*width+'\n')*height

        while True:
            yield frame0
            yield frame1
