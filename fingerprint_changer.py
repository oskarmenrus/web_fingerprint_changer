from fake_usrag_bor import FakeUserAgentBOR
import json
import random


def separator():
    return print('***********************************************')


def generate_accept_language(self):
    with open('language.json', 'r') as file:
        data = json.load(file)

    lang = [key for key, value in data.items()]
    string = f'{random.choice(lang)};q={str(random.randint(8, 9) / 10)}, ' \
             f'{random.choice(lang)};q={str(random.randint(6, 7) / 10)}, ' \
             f'{random.choice(lang)};q={str(random.randint(4, 5) / 10)}, ' \
             f'*;q=0.3'

    self.browser.page().profile().setHttpAcceptLanguage(string)
    return print(f'Accept-Language: {string}')


def change_screen_size(self, width, height):
    self.move(0, 0)
    self.resize(random.randint(width // 2, width), random.randint(height // 2, height))
    print(f'Текущее разрешение экрана: {self.frameGeometry().width()} x {self.frameGeometry().height()}')


def change_user_agent(self):
    ua = FakeUserAgentBOR()
    ua_list = [
        ua.random_android_user_agent, ua.random_chrome_user_agent,
        ua.random_edge_user_agent, ua.random_firefox_user_agent,
        ua.random_ie_user_agent, ua.random_opera_user_agent,
        ua.random_safari_user_agent
    ]
    user_agent = random.choice(ua_list)()
    self.browser.page().profile().setHttpUserAgent(user_agent)
    print(f'User-Agent: {user_agent}')


separator()
