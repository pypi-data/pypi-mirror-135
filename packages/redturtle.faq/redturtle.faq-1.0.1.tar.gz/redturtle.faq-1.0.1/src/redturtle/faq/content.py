# -*- coding: utf-8 -*-
from redturtle.faq.interfaces import IFaq
from redturtle.faq.interfaces import IFaqFolder
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IFaq)
class Faq(Container):
    """
    """


@implementer(IFaqFolder)
class FaqFolder(Container):
    """
    """
