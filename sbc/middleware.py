from django.conf import settings
from django.utils.http import urlquote
from django import http
 
class EnforceHostnameMiddleware(object):
    """
    Enforce the hostname per the ENFORCE_HOSTNAME setting in the project's settings
    
    The ENFORCE_HOSTNAME can either be a single host or a list of acceptable hosts
    """
    def process_request(self, request):
        """Enforce the host name"""
        try:
            if not settings.ENFORCE_HOSTNAME:
                # enforce not being used, don't do anything
                return None
        except AttributeError, e:
            return None
        
        host = request.get_host()
        
        # find the allowed host name(s)
        allowed_hosts = settings.ENFORCE_HOSTNAME
        if not isinstance(allowed_hosts, list): 
            allowed_hosts = [allowed_hosts]
        if host in allowed_hosts:
            return None
        
        # redirect to the proper host name
        new_url = [allowed_hosts[0], request.path]
        new_url = "%s://%s%s" % (
            request.is_secure() and 'https' or 'http',
            new_url[0], urlquote(new_url[1]))
        if request.GET:
            new_url += '?' + request.META['QUERY_STRING']
 
        return http.HttpResponsePermanentRedirect(new_url)