import datetime

from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver

from seance.models import Film, Hall, Seance, AdvUser
from seance.tests.test_models import BaseInitial


class UsersTestCase(LiveServerTestCase, BaseInitial):

    def setUp(self):
        # path to geckodriver can be added using terminal with this command (on my local comp):
        # export PATH=$PATH:/home/mike/geckodriver
        self.browser = webdriver.Firefox()
        # self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)

        BaseInitial.__init__(self)

    def tearDown(self):
        self.browser.quit()
        # pass

    def test_user_sees_start_page_registers_logs_in(self):
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

        # There he sees a form for registration with fields, labeled: username, password1, password2
        reg_form = self.browser.find_element_by_id('registration-form')
        username = reg_form.find_element_by_id('id_username')
        password1 = reg_form.find_element_by_id('id_password1')
        password2 = reg_form.find_element_by_id('id_password2')
        submit = reg_form.find_element_by_id('form-submit')

        self.assertIsNotNone(self.browser.find_element_by_css_selector('label[for="id_username"]'))
        self.assertEqual(username.get_attribute('placeholder'), 'username')
        self.assertIsNotNone(self.browser.find_element_by_css_selector('label[for="id_password1"]'))
        self.assertEqual(password1.get_attribute('placeholder'), 'password')
        self.assertIsNotNone(self.browser.find_element_by_css_selector('label[for="id_password2"]'))
        self.assertEqual(password2.get_attribute('placeholder'), 'repeat password')
        self.assertEqual(submit.get_attribute('value'), 'Submit')

        # then he enters correct information and clicks "Submit"
        username.send_keys('user1')
        password1.send_keys('Password1234')
        password2.send_keys('Password1234')
        # submit.click()
        # submit.submit()

        # import pdb; pdb.set_trace()
        # self.assertTrue(AdvUser.objects.filter(username='user1'))

        # after been registered user is redirected to root url
        # self.assertEqual(self.browser.current_url, self.live_server_url + '/')

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

        # self.fail(msg='Incomplete test')



        # # First he enters username, password1 and password2, but makes a mistake in password2 clicks Submit
        # username.send_keys('user1')
        # password1.send_keys('password1')
        # password2.send_keys('some text')
        # submit.click()
        # self.assertFalse(AdvUser.objects.filter(username='user1'))
        #
        # Nothing

        self.browser.get(self.live_server_url + '/')
        self.browser.find_element_by_id('link-login').click()
        login_form = self.browser.find_element_by_id('login-form')
