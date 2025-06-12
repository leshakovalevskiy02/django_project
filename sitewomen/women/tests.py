from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from .models import Women
from .utils import DataMixin


class GetPagesTestCase(TestCase):
    fixtures = ['women_women.json', 'women_category.json', 'women_husbands.json',
                'women_tagspost.json', "users_authors.json", "users_groups.json"]

    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_mainpage(self):
        path = reverse("home")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "women/index.html")
        self.assertEqual(response.context_data["title"], "Главная страница")

    def test_addpage_redirect(self):
        path = reverse("add_page")
        path_redirect = reverse("users:login")
        response = self.client.get(path)
        self.assertRedirects(response, f"{path_redirect}?next={path}",
                             HTTPStatus.FOUND, HTTPStatus.OK)

    def test_data_mainpage(self):
        posts = Women.published.select_related("cat").select_related("author")
        path =  reverse("home")
        response = self.client.get(path)
        self.assertQuerySetEqual(posts[:DataMixin.paginate_by], response.context_data["posts"])

    def test_paginate_pages(self):
        path = reverse("home")
        response = self.client.get(path)
        num_pages = response.context_data["paginator"].num_pages
        posts = Women.published.select_related("cat").select_related("author")

        page = 1
        paginate_by = DataMixin.paginate_by

        while page <= num_pages:
            response = self.client.get(f"{path}?page={page}")
            self.assertQuerySetEqual(response.context_data["posts"],
                                 posts[(page - 1) * paginate_by: page * paginate_by])
            page += 1

    def test_content_post(self):
        posts = Women.published.all()
        for post in posts:
            path = reverse("post", args=(post.slug, ))
            response = self.client.get(path)
            self.assertEqual(post.content, response.context_data["post"].content)

    def tearDown(self):
        "Действия после выполнения каждого теста"