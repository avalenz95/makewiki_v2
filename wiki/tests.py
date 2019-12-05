import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Page

#Test suites are defined in classes
#[appname]TestCase
class wikiTestCase(TestCase):


    def test_true_is_true(self):
        """Test that true equals true"""
        self.assertEquals(True, True)

    def test_page_slugify_on_save(self):
        """ Tests the slug generated when saving a Page. """
        # Author is a required field in our model.
        # Create a user for this test and save it to the test database.
        user = User()
        user.save()

        # Create and save a new page to the test database.
        page = Page(title="My Test Page", content="test", author=user)
        page.save()

        # Make sure the slug that was generated in Page.save()
        # matches what we think it should be.
        self.assertEqual(page.slug, "my-test-page")


class PageListViewTests(TestCase):

    def test_multiple_pages(self):
        # Make some test data to be displayed on the page.
        #creates and save user - not thread safe
        user = User.objects.create()

        Page.objects.create(title="My Test Page", content="test", author=user)
        Page.objects.create(title="Another Test Page", content="test", author=user)

        # Issue a GET request to the MakeWiki homepage.
        # When we make a request, we get a response back.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the number of pages passed to the template
        # matches the number of pages we have in the database.
        responses = response.context['pages']
        self.assertEqual(len(responses), 2)

        self.assertQuerysetEqual(
            responses,
            ['<Page: My Test Page>', '<Page: Another Test Page>'],
            ordered=False
        )

class PageDetailViewTests(TestCase):

    def test_detail_view(self):
        """Test details page for aspecific page"""
        user = User.objects.create()

        Page.objects.create(title="My Test Page", content="test", author=user)

        response = self.client.get('/my-test-page/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

class PageCreateViewTest(TestCase):
    def test_create_view(self):
        """Test creation form loading"""

        response = self.client.get('/create-post')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_create_submission(self):
        #create post request
        post_request = self.client.post('/create-post',{
            'title': 'Test Post',
            'content': 'this test' ,
            'author': 'admin'},follow=True,)

        # Check that the response is 302 redirect.
        self.assertEqual(post_request.status_code, 302)



#In the same tests.py file we’ve used today, write tests that prove the following:

#Next, write a test that proves that we can successfully create a new wiki page by filling out the new page form. This one involves a few more steps:

#Create a dictionary of key-value pairs containing the post data to be sent via the form
#Make a POST request to the client with self.client.post()
#Check that we get a 302 status code (Why 302 and not 200?)
#Check that a new page object was created in the test database

    