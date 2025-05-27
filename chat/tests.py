from django.test import TestCase
from django.urls import reverse

class ChatRoomViewTest(TestCase):
    def test_room_view_renders(self):
        room_name = "testroom"
        response = self.client.get(reverse("room", args=[room_name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, room_name)
