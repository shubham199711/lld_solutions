class LegacyAPI:
    def get_data_xml(self):
        return "<tracking>SH123</tracking>"
    
class AdaptorAPI:
    def __init__(self, legacyAPI: LegacyAPI):
        self.legacyAPI = legacyAPI
    
    def get_data(self):
        data = self.legacyAPI.get_data_xml()
        return {
            "tracking": "SH123"
        }
    

adaptor = AdaptorAPI(LegacyAPI())
print(adaptor.get_data())