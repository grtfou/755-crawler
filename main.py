from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class CrawlerWidget(BoxLayout):
    def check_status(self, url, stop_date):
        print('URL is: {txt}'.format(txt=url))
        print('Stop Date is: {txt}'.format(txt=stop_date))


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

    def build(self):
        return CrawlerWidget()

if __name__ == '__main__':
    MainApp().run()
