# -*- coding: utf-8 -*-
from redturtle.faq.testing import REDTURTLE_FAQ_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit


import unittest


class FaqStructureTest(unittest.TestCase):

    layer = REDTURTLE_FAQ_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.folder = api.content.create(
            container=self.portal, type="Folder", title="A folder"
        )
        self.faq_folder_root = api.content.create(
            container=self.portal, type="FaqFolder", title="Root", icon=""
        )

        api.content.create(
            container=self.portal, type="FaqFolder", title="Root", icon=""
        )

        api.content.create(
            container=self.faq_folder_root,
            type="FaqFolder",
            title="a",
            icon="",
        )

        api.content.create(
            container=self.faq_folder_root,
            type="FaqFolder",
            title="b",
            icon="",
        )

        api.content.create(
            container=self.faq_folder_root["a"],
            type="FaqFolder",
            title="aa",
            icon="",
        )

        api.content.create(
            container=self.faq_folder_root,
            type="Faq",
            title="faq first level",
            icon="",
        )

        api.content.create(
            container=self.faq_folder_root["a"]["aa"],
            type="Faq",
            title="faq about a searchable",
            icon="",
        )

        api.content.create(
            container=self.faq_folder_root["a"]["aa"],
            type="Faq",
            title="another faq about a",
            icon="",
        )

        api.content.create(
            container=self.faq_folder_root["b"],
            type="Faq",
            title="faq b searchable",
            icon="",
        )
        api.content.create(
            container=self.faq_folder_root["b"],
            type="FaqFolder",
            title="bb",
            icon="",
        )
        api.content.create(
            container=self.faq_folder_root["b"]["bb"],
            type="Faq",
            title="another b faq",
            icon="",
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_faq_structure_in_components_only_for_faq_folders(self):
        faq_folder_resp = self.api_session.get(
            self.faq_folder_root.absolute_url()
        ).json()
        folder_resp = self.api_session.get(self.folder.absolute_url()).json()
        self.assertIn("faq-structure", faq_folder_resp["@components"])
        self.assertNotIn("faq-structure", folder_resp["@components"])

    def test_faq_structure_return_all_structure_inside_faq_folder(self):
        url = "{}/@faq-structure".format(self.faq_folder_root.absolute_url())
        resp = self.api_session.get(url).text

        self.assertIn(self.faq_folder_root["a"].UID(), resp)
        self.assertIn(self.faq_folder_root["a"]["aa"].UID(), resp)
        self.assertIn(
            self.faq_folder_root["a"]["aa"]["faq-about-a-searchable"].UID(),
            resp,
        )
        self.assertIn(
            self.faq_folder_root["a"]["aa"]["another-faq-about-a"].UID(), resp,
        )
        self.assertIn(self.faq_folder_root["b"].UID(), resp)
        self.assertIn(
            self.faq_folder_root["b"]["faq-b-searchable"].UID(), resp,
        )
        self.assertIn(self.faq_folder_root["b"]["bb"].UID(), resp)
        self.assertIn(
            self.faq_folder_root["b"]["bb"]["another-b-faq"].UID(), resp
        )
        self.assertIn(self.faq_folder_root["faq-first-level"].UID(), resp)

    def test_faq_structure_return_only_matching_folders_and_faqs_if_query(
        self,
    ):
        url = "{}/@faq-structure?SearchableText=searchable".format(
            self.faq_folder_root.absolute_url()
        )
        resp = self.api_session.get(url).text

        self.assertIn(self.faq_folder_root["a"].UID(), resp)
        self.assertIn(self.faq_folder_root["a"]["aa"].UID(), resp)
        self.assertIn(
            self.faq_folder_root["a"]["aa"]["faq-about-a-searchable"].UID(),
            resp,
        )
        self.assertNotIn(
            self.faq_folder_root["a"]["aa"]["another-faq-about-a"].UID(), resp,
        )
        self.assertIn(self.faq_folder_root["b"].UID(), resp)
        self.assertIn(
            self.faq_folder_root["b"]["faq-b-searchable"].UID(), resp,
        )
        self.assertNotIn(self.faq_folder_root["b"]["bb"].UID(), resp)
        self.assertNotIn(
            self.faq_folder_root["b"]["bb"]["another-b-faq"].UID(), resp
        )
        self.assertNotIn(self.faq_folder_root["faq-first-level"].UID(), resp)
