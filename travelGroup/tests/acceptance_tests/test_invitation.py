from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from travelGroup.models import CustomUser
from travelGroup.tests.acceptance_tests.util import login, go_to_invitation


class AddInvitationViewAcceptanceTest(StaticLiveServerTestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username='testuser', first_name='test', last_name='user', email='testemail@email.com', password='testpassword')
        self.user.save()
        self.driver = webdriver.Edge()

    def add_invitation(self):
        self.driver.get(self.live_server_url)

        login(self.driver, self.user)
        go_to_invitation(self.driver)





