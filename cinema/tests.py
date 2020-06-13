from django.test import LiveServerTestCase
from selenium import webdriver


class UsersTestCase(LiveServerTestCase):

    def setUp(self):
        # path to geckodriver can be added using terminal with this command (on my local comp):
        # export PATH=$PATH:/home/mike/geckodriver
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_user_sees_startpage(self):
        """
        Test user can enter the start page with url '/'.
        """
        # User enters the start page of the site. He can see, that he is at the cinema's site
        # because the name of the site in the heading. It's "Broadway cinema"

        homepage = self.browser.get(self.live_server_url + '/')
        heading_element = self.browser.find_element_by_css_selector('.navbar-brand')

        # There are also links to log in, and to registrate
        # If user is logged in, he sees Log out link and Registration link
        #
        # He can see the list of available seances, with time of its beginning, time of its ending,
        # the title of film to watch, end the quantity of free seates and date of its end
        #
        # If there are no seats available, he sees message "The tickets on this seance are sold!"
        #
        #
        #
        #
        # The title of the film is a link. User clicks it and comes to seance detail page.
        self.fail(msg='Incomplete test')
