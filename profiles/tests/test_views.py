from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Category
from profiles.models import UserProfile
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404

class ProfileViewsTestCase(TestCase):
    
    def setUp(self):
        # Create users and associated profiles
        self.user1 = User.objects.create_user(username='testuser1', password='password')
        self.user_profile1 = UserProfile.objects.create(
            user=self.user1,
            name='Test User 1',
            email='testuser1@example.com',
            username='testuser1',
            profession='Developer',
            about='A developer profile.'
        )
        
        # Create posts for the user
        category = Category.objects.create(name='Test Category')
        self.post1 = Post.objects.create(
            writer=self.user_profile1,
            title='Post 1',
            text='Content for Post 1',
            category=category,
            post_slug='post-1',  # Ensure unique 
        )

        self.post2 = Post.objects.create(
            writer=self.user_profile1,
            title='Post 2',
            text='Content for Post 2',
            category=category,
            post_slug='post-2',  # Ensure unique slug
        )


    def test_profile_view(self):
        # Test profile view (GET request)
        response = self.client.get(reverse('profile', kwargs={'pk': self.user_profile1.profile_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User 1')
        self.assertContains(response, 'Content for Post 1')
        self.assertContains(response, 'Content for Post 2')

    def test_account_view(self):
        # Test account view (GET request when the user has a profile)
        self.client.login(username='testuser1', password='password')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User 1')
        self.assertContains(response, 'Content for Post 1')
        self.assertContains(response, 'Content for Post 2')

    def test_account_view_no_profile(self):
        # Створюємо користувача без профілю
        user2 = User.objects.create_user(username='testuser2', password='password')
        
        # Логін користувача
        self.client.login(username='testuser2', password='password')
        
        # Перевірка доступу до сторінки акаунту
        response = self.client.get(reverse('account'))
        
        # Перевірка, що відповідь містить повідомлення, що профіль не знайдено
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile not found')  # Повідомлення про відсутність профілю

    def test_account_view_with_profile(self):
        # Create a user with a unique username
        username = 'testuser_unique'
        user1 = User.objects.create_user(username=username, password='password')
        
        # Create the profile for the user
        user_profile = UserProfile.objects.create(user=user1, name='Test User', profession='Developer', about='Some bio')

        # Log the user in
        self.client.login(username=username, password='password')
        
        # Access the account page
        response = self.client.get(reverse('account'))
        
        # Check that the profile is correctly displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')  # Check that the user's name is displayed
        self.assertContains(response, 'Developer')  # Check that the user's profession is displayed

    def test_edit_post_view_get(self):
        # Test the edit post view with GET request
        self.client.login(username='testuser1', password='password')
        response = self.client.get(reverse('edit_post', kwargs={'post_slug': self.post1.post_slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post 1')
        self.assertContains(response, 'Content for Post 1')

    def test_edit_post_view_post(self):
        # Test the edit post view with POST request (updating post)
        self.client.login(username='testuser1', password='password')
        response = self.client.post(reverse('edit_post', kwargs={'post_slug': self.post1.post_slug}), {
            'title': 'Updated Post 1',
            'text': 'Updated Content for Post 1',
            'category': self.post1.category.id
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful save
        self.post1.refresh_from_db()  # Refresh the post instance from the database
        self.assertEqual(self.post1.title, 'Updated Post 1')
        self.assertEqual(self.post1.text, 'Updated Content for Post 1')

    def test_delete_post(self):
        # Test delete post view
        self.client.login(username='testuser1', password='password')
        response = self.client.post(reverse('delete_post', kwargs={'post_slug': self.post1.post_slug}))
        self.assertEqual(response.status_code, 302)  # Should redirect after deletion
        with self.assertRaises(Post.DoesNotExist):
            self.post1.refresh_from_db()

    def test_update_profile_view_get(self):
        # Test GET request for updating profile
        self.client.login(username='testuser1', password='password')
        response = self.client.get(reverse('updateprofile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User 1')

    def test_update_profile_view_post(self):
        self.client.login(username='testuser1', password='password')
        response = self.client.post(reverse('updateprofile'), {
            'name': 'Updated Test User 1',
            'email': 'updated@example.com',
            'username': 'updatedtestuser1',  # Add the username here
            'profession': 'Senior Developer',
            'about': 'Updated about me content.'
        })

        # Check the response
        self.assertEqual(response.status_code, 302)  # Should redirect after update

        # Refresh the profile to check the changes
        self.user_profile1.refresh_from_db()
        self.assertEqual(self.user_profile1.name, 'Updated Test User 1')
        self.assertEqual(self.user_profile1.email, 'updated@example.com')
        self.assertEqual(self.user_profile1.profession, 'Senior Developer')
        self.assertEqual(self.user_profile1.user.username, 'updatedtestuser1')  # Check updated username

    def test_profile_view_pagination(self):
        # Create 10 posts for the user
        for i in range(10):
            Post.objects.create(
                writer=self.user_profile1,
                title=f'Post {i}',
                text=f'Content for Post {i}',
                category=self.post1.category
            )
        
        self.client.login(username='testuser1', password='password')
        
        # Request the third page (page=3)
        response = self.client.get(reverse('profile', kwargs={'pk': self.user_profile1.profile_id}), {'page': 3})
        
        # Check that the posts for page 3 (Post 8 and Post 9) are in the response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post 8')
        self.assertContains(response, 'Post 9')

    def test_profile_view_no_posts(self):
        # Create a user with no posts
        user_no_posts = User.objects.create_user(username='noprofile', password='password')
        
        # Create a user profile with no posts
        user_profile_no_posts = UserProfile.objects.create(
            user=user_no_posts,
            name='No Posts User',
            email='noprofile@example.com',
            username='noprofile',
            profession='Tester',
            about='No posts here.'
        )
        
        response = self.client.get(reverse('profile', kwargs={'pk': user_profile_no_posts.profile_id}), {'page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No posts here.')

    def test_profile_view_empty(self):
        # Ensure no UserProfile exists for user1
        UserProfile.objects.filter(user=self.user1).delete()

        # Create a user profile with no posts
        empty_user_profile = UserProfile.objects.create(
            user=self.user1,
            name='Empty User',
            email='emptyuser@example.com',
            username='emptyuser',
            profession='Designer',
            about='A profile with no posts.'
        )

        response = self.client.get(reverse('profile', kwargs={'pk': empty_user_profile.profile_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A profile with no posts.')


