import time
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

class MyEventHandler(PatternMatchingEventHandler):
    def hook(self, thing):
        self.thing = thing

    def on_modified(self, event):
        super(MyEventHandler, self).on_modified(event)
        #logging.info("File %s was just modified" % event.src_path)
        self.thing.readConfigFile()  #<- i want to call this method in class Configuration


class Configuration:
    def readConfigFile(self):
         # set certain values here
         print("readconfigfile")
    def provideValues(self):
         # get certain values here
         print("providevalues")


class MainClass:
    def __init__(self):
        self.conf = Configuration()
        self.event_handler = MyEventHandler(patterns='*')
        self.event_handler.hook(self.conf)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, ".")
        self.observer.start()

    def main(self):
        while True:
            # using values from configFile here
            bla = self.conf.provideValues()
            time.sleep(1)

if __name__ == '__main__':
    mc = MainClass()
    mc.main()
    # do something else