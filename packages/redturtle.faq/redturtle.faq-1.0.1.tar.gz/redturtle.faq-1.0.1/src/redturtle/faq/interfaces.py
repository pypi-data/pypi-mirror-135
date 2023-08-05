# -*- coding: utf-8 -*-
from redturtle.faq import _
from plone.supermodel import model
from zope.schema import TextLine
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class IRedturtleFaqLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IFaq(model.Schema):
    """
    """


class IFaqFolder(model.Schema):
    """
    """

    icon = TextLine(
        title=_(u"icon_label", default=u"Icon"),
        description=_(
            "icona_help",
            default="You can select an icon from select menu or set a "
            "FontAwesome icon name.",
        ),
        required=False,
        default="",
    )


class ISerializeFaqToJsonSummary(Interface):
    """
    custom interface to serialize faqs
    """
