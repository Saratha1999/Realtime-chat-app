from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class ChatRoomViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_room_view_renders(self):
        room_name = "testroom"
        response = self.client.get(reverse("room", args=[room_name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, room_name)
