# -*- coding: utf-8 -*-
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from redturtle.faq.interfaces import IFaqFolder
from redturtle.faq.interfaces import ISerializeFaqToJsonSummary
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(IFaqFolder, Interface)
class FaqStructure(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "faq-structure": {
                "@id": "{}/@faq-structure".format(self.context.absolute_url())
            }
        }
        if not expand:
            return result
        data = getMultiAdapter(
            (self.context, self.request), ISerializeFaqToJsonSummary
        )()
        if data:
            result["faq-structure"]["items"] = [data]
        return result


class FaqStructureGet(Service):
    def reply(self):
        data = FaqStructure(self.context, self.request)
        return data(expand=True)["faq-structure"]
