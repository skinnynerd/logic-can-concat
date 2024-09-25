# CAN Concatenator High Level Analyzer for Saleae Logic 2 software. This script
# concatenates Logic 2 CAN "frames" (actually individual fields of the message)
# into a single frame which can be more easily read.

# https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame

# High level analyzers must subclass the HighLevelAnalyzer class.
class CanConcatenator(HighLevelAnalyzer):

    result_types = {
        'canframe': {
            'format': '{{data.datastring}}'
        }
    }

    def __init__(self):
        self.currentStart = 0
        self.currentId = 0
        self.currentData = b''
        self.currentCrc = 0

    def decode(self, frame: AnalyzerFrame):

        if frame.type == 'identifier_field':
            self.currentStart = frame.start_time
            self.currentId = frame.data['identifier']
            self.currentData =b''
        elif frame.type == 'data_field':
            self.currentData = self.currentData + frame.data['data']
        elif frame.type == 'crc_field':
            self.currentCrc = frame.data['crc']
        elif frame.type == 'ack_field':
            # Return the data frame
            datastring = ('{:03X}'.format(self.currentId) + '#'
                        + '.'.join('{:02X}'.format(a) for a in self.currentData))

            print(datastring) # If streaming to the terminal, this will be printed

            return AnalyzerFrame('canframe', self.currentStart, frame.end_time, {
                'id': self.currentId,
                'data': self.currentData,
                'crc': self.currentCrc,
                'datastring': datastring
            })

