from django.test                import TestCase
from django.test.client         import Client
from django.contrib.auth.models import User, Group
from tutordb.models             import Centre

class AccessControls(TestCase):

    fixtures = ['groups', 'test_data']

    def setUp(self):
        """Get ready for the testing"""
        
        # check that the test group has been created
        self.head_office_group = Group.objects.get(name='Head Office')

        # check that the test users are loaded
        self.tutor          = User.objects.get(username='tutor')
        self.head_office    = User.objects.get(username='headoffice')
        self.centre_manager = User.objects.get(username='centremanager')
        
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

        # check that HO user can see all the centres
        res = c.get('/tutors/')
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 3 )
        
        # check that can see details for a centre
        res = c.get('/tutors/' + str(self.victoria_library.id) )
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 2 )
        self.assertEqual( res.context['object_list'][0].first_name, 'Centre Manager' )
        
        # not tested here - that HO user can view/edit details in the admin
        # we do check that they can access it though
        res = c.get('/admin/')
        self.assertEqual( res.status_code, 200 )


    def test_centre_manager(self):
        """
        Test what the centre manager can see
        """

        c = Client()
        cm = self.centre_manager

        # login to the site
        self.assertTrue( c.login( username=cm.email, password='secret' ) )

        # check that they only see one centre listed for tutors
        res = c.get('/tutors/')
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 1 )
        self.assertEqual( res.context['object_list'][0].name, 'Victoria Library' )

        # check that they see the tutors for their centre
        res = c.get('/tutors/' + str(self.victoria_library.id) )
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 2 )
        self.assertEqual( res.context['object_list'][0].first_name, 'Centre Manager' )
        
        # check that the can't see users for other centres
        res = c.get('/tutors/' + str(self.mayfair_library.id) )
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 0 )


    def test_tutor(self):
        """
        Check that tutor can only see their own details
        """
        
        # test that no centres shown to view tutors for
        # test that no tutors shown when going to centre direct


# test that the various access controls are correctly set

# head office (group):
# see all tutors and their certificates
# they can edit things through the admin interface (not tested here)


# centre managers (state in tenure):
#   can see all tutors in their centres
#   certificates
#   cannot edit


# tutors: