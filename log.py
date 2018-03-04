import aiohttp
import re

class AccessLogger(aiohttp.helpers.AccessLogger):
    LOG_FORMAT_MAP = {         
        'a': 'remote_address', 
        't': 'request_start_time',      
        'P': 'process_id',     
        'r': 'first_request_line',      
        's': 'response_status',
        'b': 'response_size',  
        'T': 'request_time',   
        'Tf': 'request_time_frac',      
        'D': 'request_time_micro',      
        'i': 'request_header', 
        'o': 'response_header',
        'A': 'remote_id',
    }
    FORMAT_RE = re.compile(r'%(\{([A-Za-z0-9\-_]+)\}([ioe])|[atPrsbODA]|Tf?)')

    def compile_format(self, log_format):
        methods = list()

        for atom in self.FORMAT_RE.findall(log_format):
            if atom[1] == '':  
                format_key = self.LOG_FORMAT_MAP[atom[0]]
                m = getattr(AccessLogger, '_format_%s' % atom[0])
            else:              
                format_key = (self.LOG_FORMAT_MAP[atom[2]], atom[1])
                m = getattr(AccessLogger, '_format_%s' % atom[2])
                m = functools.partial(m, atom[1]) 

            methods.append(self.KeyMethod(format_key, m))

        log_format = self.FORMAT_RE.sub(r'%s', log_format)
        log_format = self.CLEANUP_RE.sub(r'%\1', log_format)
        return log_format, methods

    @staticmethod
    def _format_A(req, res, time):
        if req is None:
            return '-'
        rid = req.rid
        return rid if rid is not None else '-'
