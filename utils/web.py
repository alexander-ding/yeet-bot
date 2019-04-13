""" This is a file for web utilities such as downloading images
"""

from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

def get_image(url, acceptable_suffixes = ["jpeg", "jpg", "png"]):
    """ Gets an image from url, checking the validity of the url and whether the link is an image,
        returns ok?, a possbile error string, and the image itself (if possible)

        Returns
        -------
        (Bool, String, PIL.Image)
    """
    result = urlparse(url)

    # first make sure the link is not malformed
    if not all([result.scheme, result.netloc]):
        return False, "{} is not of the form https://xxx or http://xxx".format(url), None
    
    # then make sure the header is of the correct form
    image_formats = ["image/{}".format(suffix) for suffix in acceptable_suffixes]
    r = requests.head(url)
    if r.headers["content-type"] not in image_formats:
        return False, "Link must refer to a file with one of {} as suffix".format(", ".join(acceptable_suffixes)), None

    # then make sure the link returns properly
    r = requests.get(url)
    if r.status_code >= 400:
        return False, "Cannot open link {}".format(url), None
    return True, "", Image.open(BytesIO(r.content))