from tracepointdebug.probe.coded_exception import CodedException
from tracepointdebug.probe.errors import FILE_NAME_IS_MANDATORY, LINE_NUMBER_IS_MANDATORY

def validate_file_name_and_line_no(file_name, line_no):
    if not file_name or len(file_name) <= 0:
        raise CodedException(FILE_NAME_IS_MANDATORY)
    if not line_no or line_no <= 0:
        raise CodedException(LINE_NUMBER_IS_MANDATORY)