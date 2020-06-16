import datetime

from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver
from django.utils.translation import gettext_lazy as _

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

        # He fills inputs in and clicks "Submit"
        username.send_keys('user1')
        password1.send_keys('Password4321')
        password2.send_keys('Password4321')

        submit.click()

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
        # The title of the film is a link. User clicks it and comes to seance detail page

        # self.browser.get(self.live_server_url + '/')
        # self.browser.find_element_by_id('link-login').click()
        # login_form = self.browser.find_element_by_id('login-form')
        # login_form.find_element_by_id('id_username').send_keys('admin')
        # login_form.find_element_by_id('id_password').send_keys('password1')
        # login_form.find_element_by_id('submit-login-form').click()
        #
        # self.fail(msg='Incomplete test')

    def test_staff_can_add_content(self):
        """
        Tests that a 'staff' user can access the admin and
        add Albums, Tracks, and Solos
        """
        # Bill would like to add a record and a number of
        # solos to JMAD. He visits the admin site
        admin_root = self.browser.get(self.live_server_url + '/admin/')

        # He can tell he's in the right place because of the
        # title of the page
        self.assertEqual(self.browser.title, 'Log in | Django site admin')

        # He enters his username and password and submits the
        # form to log in
        login_form = self.browser.find_element_by_id('login-form')
        login_form.find_element_by_name('username').send_keys('admin')
        login_form.find_element_by_name('password').send_keys('password1')
        login_form.find_element_by_css_selector('.submit-row input').click()

    def test_filter_form_is_in_index_page(self):
        """
        Test that filter form was rendered and has fields we expect (at index page)
        """
        self.browser.get(self.live_server_url + '/')
        ordering_form = self.browser.find_element_by_id('ordering-form')
        choices = ordering_form.find_element_by_id('id_ordering')
        filter_submit = ordering_form.find_element_by_id('submit-ordering')

        self.assertEqual(filter_submit.get_attribute('value'), _('Order'))
        self.assertIsNotNone(ordering_form.find_elements_by_css_selector('label[for="id_ordering"]'))

