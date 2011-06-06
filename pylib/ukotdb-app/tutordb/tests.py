from django.test                import TestCase
from django.test.client         import Client
from django.contrib.auth.models import Group
from tutordb.models             import Centre, Tutor
from certificates.models        import Certificate

# NOTE ON CERTIFICATES:
#
# Ideally the certificate tests would be in the certificat app - but they are
# here for conveniance as they are so similar to other tests that are being done
# here.


class AccessControls(TestCase):

    fixtures = ['groups', 'test_data']

    def setUp(self):
        """Get ready for the testing"""
        
        # check that the test group has been created
        self.head_office_group = Group.objects.get(name='Head Office')

        # check that the test users are loaded
        self.tutor          = Tutor.objects.get(username='tutor')
        self.tutor2         = Tutor.objects.get(username='tutor2')
        self.head_office    = Tutor.objects.get(username='headoffice')
        self.centre_manager = Tutor.objects.get(username='centremanager')
        
        # get the centres
        self.mayfair_library  = Centre.objects.get(name='Mayfair Library')
        self.victoria_library = Centre.objects.get(name='Victoria Library')

        # get the certificates
        self.certificate = Certificate.objects.get(student_name='Student 1')
        self.certificate2 = Certificate.objects.get(student_name='Student 2')


    def test_head_office(self):
        """
        Test that someone in the head office group can see everything
        """
        c = Client()
        ho = self.head_office

        # login to the site
        self.assertTrue( c.login( username=ho.email, password='secret' ) )

        # check that can see details for a centre
        res = c.get('/centres/' + str(self.victoria_library.id) + '/tutors')
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 2 )
        self.assertEqual( res.context['object_list'][0].first_name, 'Centre Manager' )
        
        # check that we can see certificates listed for both test tutors
        for id in [ self.tutor.id, self.tutor2.id ]:
            res = c.get('/certificates/tutor/' + str(id) )
            self.assertEqual( res.status_code, 200 )
            self.assertEqual( len(res.context['object_list']), 1 )

        # check that we can see the certificates for both users
        for id in [ self.certificate.id, self.certificate2.id ]:
            # check the html
            res = c.get('/certificates/' + str(id) )
            self.assertEqual( res.status_code, 200 )
            self.assertEqual( res.context['object'].id, id )

            # check the pdf
            res = c.get('/certificates/' + str(id) + '/pdf' )
            self.assertEqual( res.status_code, 200 )

        # not tested here - that HO user can view/edit details in the admin


    def test_centre_manager(self):
        """
        Test what the centre manager can see
        """

        c = Client()
        cm = self.centre_manager

        # login to the site
        self.assertTrue( c.login( username=cm.email, password='secret' ) )

        # check that they see the tutors for their centre
        res = c.get('/centres/' + str(self.victoria_library.id) + '/tutors' )
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 2 )
        self.assertEqual( res.context['object_list'][0].first_name, 'Centre Manager' )
        
        # check that the can't see users for other centres
        res = c.get('/centres/' + str(self.mayfair_library.id) + '/tutors' )
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 0 )

        # check that we can see certificates for tutor (we are their admin)
        res = c.get('/certificates/tutor/' + str(self.tutor.id) )
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 1 )

        # check that we can see the certificate
        for id in [ self.certificate.id ]:
            res = c.get('/certificates/' + str( self.certificate.id ) )
            self.assertEqual( res.status_code, 200 )
            self.assertEqual( res.context['object'].id, id )
            res = c.get('/certificates/' + str(id) + '/pdf' )
            self.assertEqual( res.status_code, 200 )

        # check that we can't see certificates for tutor (we are not their admin)
        res = c.get('/certificates/tutor/' + str(self.tutor2.id) )
        self.assertEqual( res.status_code, 404 )

        # check that we can see the certificate
        for id in [ self.certificate2.id ]:
            res = c.get('/certificates/' + str(id) )
            self.assertEqual( res.status_code, 404 )
            res = c.get('/certificates/' + str(id) + '/pdf' )
            self.assertEqual( res.status_code, 404 )

    def test_tutor(self):
        """
        Check that tutor can only see their own details
        """
        c = Client()
        tutor = self.tutor

        # login to the site
        self.assertTrue( c.login( username=tutor.email, password='secret' ) )

        # check that they see the tutors for their centre
        res = c.get('/centres/' + str(self.victoria_library.id) + '/tutors')
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 0 )
        
        # check that we can see certificates for tutor it is us
        res = c.get('/certificates/tutor/' + str(self.tutor.id) )
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 1 )

        # check that we can see the certificate
        for id in [ self.certificate.id ]:
            res = c.get('/certificates/' + str(id) )
            self.assertEqual( res.status_code, 200 )
            self.assertEqual( res.context['object'].id, id )
            res = c.get('/certificates/' + str(id) + '/pdf' )
            self.assertEqual( res.status_code, 200 )

        # check that we can't see certificates for tutor (we are not their admin)
        res = c.get('/certificates/tutor/' + str(self.tutor2.id) )
        self.assertEqual( res.status_code, 404 )

        # check that we can see the certificate
        for id in [ self.certificate2.id ]:
            res = c.get('/certificates/' + str(id) )
            self.assertEqual( res.status_code, 404 )
            res = c.get('/certificates/' + str(id) + '/pdf' )
            self.assertEqual( res.status_code, 404 )
        

    def test_tutor2(self):
        """
        Check that tutor can only see their own details
        """
        c = Client()
        tutor = self.tutor2

        # login to the site
        self.assertTrue( c.login( username=tutor.email, password='secret' ) )
        
        # check that we can't see certificates for tutor (we are not their admin)
        res = c.get('/certificates/tutor/' + str(self.tutor.id) )
        self.assertEqual( res.status_code, 404 )

        # check that we can see the certificate
        for id in [ self.certificate.id ]:
            res = c.get('/certificates/' + str(id) )
            self.assertEqual( res.status_code, 404 )
            res = c.get('/certificates/' + str(id) + '/pdf' )
            self.assertEqual( res.status_code, 404 )

        # check that we can see certificates for tutor it is us
        res = c.get('/certificates/tutor/' + str(self.tutor2.id) )
        self.assertEqual( res.status_code, 200 )
        self.assertEqual( len(res.context['object_list']), 1 )
        
        # check that we can see the certificate
        for id in [ self.certificate2.id ]:
            res = c.get('/certificates/' + str(id) )
            self.assertEqual( res.status_code, 200 )
            res = c.get('/certificates/' + str(id) + '/pdf' )
            self.assertEqual( res.status_code, 200 )
