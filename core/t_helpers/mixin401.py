import json


class TMixin401:
    def test_options_401(self):
        response = self.client.options(self.URL)
        self.assertEqual(response.status_code, 401)

    def test_list_401(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 401)

    def test_retrieve_401(self):
        response = self.client.get(
            self.instance_url(self.instance))
        self.assertEqual(response.status_code, 401)

    def test_create_401(self):
        response = self.client.post(
            self.URL, data=json.dumps({}), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 401)

    def test_update_401(self):
        response = self.client.put(
            self.URL, data=json.dumps({}), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 401)

    def test_delete_401(self):
        response = self.client.delete(self.instance_url(self.instance))
        self.assertEqual(response.status_code, 401)
