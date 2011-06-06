from django.test                import TestCase
from django.test.client         import Client
from django.contrib.auth.models import Group
from tutordb.models             import Centre, Tutor

class AccessControls(TestCase):

    fixtures = ['groups', 'test_data']

    def setUp(self):
        """Get ready for the testing"""
        
        # check that the test group has been created
        self.head_office_group = Group.objects.get(name='Head Office')

        # check that the test users are loaded
        self.tutor          = Tutor.objects.get(username='tutor')
        self.head_office    = Tutor.objects.get(username='headoffice')
        self.centre_manager = Tutor.objects.get(username='centremanager')
        
        # get the centres
        self.mayfair_library  = Centre.objects.get(name='Mayfair Library')
        self.victoria_library = Centre.objects.get(name='Victoria Library')


    def test_head_office_sees_all(self):
        """
        Test that someone in the head office group can see everything
        """
        c = Client()
        ho = self.head_office

        # login to the site
        self.assertTrue( c.login( username=ho.email, password='secret' ) )

        # # check that HO user can see all the centres
        # res = c.get('/tutors/')
        # self.assertEqual( res.status_code, 200 )
        # self.assertEqual( len(res.context['object_list']), 3 )
        
        # check that can see details for a centre
        res = c.get('/centres/' + str(self.victoria_library.id) + '/tutors')
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 2 )
        self.assertEqual( res.context['object_list'][0].first_name, 'Centre Manager' )
        
        # not tested here - that HO user can view/edit details in the admin


    def test_centre_manager(self):
        """
        Test what the centre manager can see
        """

        c = Client()
        cm = self.centre_manager

        # login to the site
        self.assertTrue( c.login( username=cm.email, password='secret' ) )

        # # check that they only see one centre listed for tutors
        # res = c.get('/tutors/')
        # self.assertEqual( res.status_code, 200 )
        # self.assertEqual( len(res.context['object_list']), 1 )
        # self.assertEqual( res.context['object_list'][0].name, 'Victoria Library' )

        # check that they see the tutors for their centre
        res = c.get('/centres/' + str(self.victoria_library.id) + '/tutors' )
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 2 )
        self.assertEqual( res.context['object_list'][0].first_name, 'Centre Manager' )
        
        # check that the can't see users for other centres
        res = c.get('/centres/' + str(self.mayfair_library.id) + '/tutors' )
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 0 )


    def test_tutor(self):
        """
        Check that tutor can only see their own details
        """
        c = Client()
        tutor = self.tutor

        # login to the site
        self.assertTrue( c.login( username=tutor.email, password='secret' ) )

        # # check that they only see one centre listed for tutors
        # res = c.get('/tutors/')
        # self.assertEqual( res.status_code, 200 )
        # self.assertEqual( len(res.context['object_list']), 0 )

        # check that they see the tutors for their centre
        res = c.get('/centres/' + str(self.victoria_library.id) + '/tutors')
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 0 )
