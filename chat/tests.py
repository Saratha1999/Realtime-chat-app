from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class ChatRoomViewTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Log in test user
        self.client.login(username='testuser', password='testpass')

    def test_room_view_renders(self):
        room_name = "testroom"
        url = reverse("room", args=[room_name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, room_name)
