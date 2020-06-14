import datetime

from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver

from seance.models import Film, Hall, Seance
from seance.tests.test_models import BaseInitial


class UsersTestCase(LiveServerTestCase, BaseInitial):

    def setUp(self):
        # path to geckodriver can be added using terminal with this command (on my local comp):
        # export PATH=$PATH:/home/mike/geckodriver
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

        BaseInitial.__init__(self)

    def tearDown(self):
        self.browser.quit()

    def test_user_sees_startpage(self):
        """
        Test user can enter the start page with url '/'.
        """
        # User enters the start page of the site. He can see, that he is at the cinema's site
        # because the name of the site in the heading. It's "Broadway cinema"

        self.browser.get(self.live_server_url + '/')

        self.assertEqual(self.browser.title, 'Broadway cinema')

        # There are also links to log in, and to register
        login_a = self.browser.find_element_by_id('link-login')
        self.assertEqual(login_a.text, 'LogIn')

        register_a = self.browser.find_element_by_id('link-register')
        self.assertEqual(register_a.text, 'Registration')

        # Our user isn't registered on the site, so he clicks Registration link
        register_a.click()

        # and comes to the registration page with URL 'accounts/register/'
        self.assertEqual(self.browser.current_url, self.live_server_url + '/accounts/register/')

        # There he sees a form for registration with fields: username,

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
