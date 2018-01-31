from lxml.html import fromstring


def get_html_element(html, tag):
    """ Parse html and return the content of the given tag
    """
    tree = fromstring(html)
    return tree.findtext(tag)
