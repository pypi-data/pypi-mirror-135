from bank_sync.Resources.resource import Resource

class Accounts(Resource):

    urls = {}

    def set_bank_id(self, bank_id):
        super().set_bank_id(bank_id)        
        return self._set_urls()

    def _set_urls(self):

        self.urls = {
            "read" : f"/accounts/{super().get_bank_id()}"
        }

        super().set_urls(self.urls)

        return self
        
    def balance(self,payload = None,endpoint='/get_balance'):
        
        return super().read(payload=payload,endpoint=f'{self.urls["read"]}{endpoint}')
        
    def mini_statement(self,payload = None,endpoint='/get_mini_statement'):
        
        return super().read(payload=payload,endpoint=f'{self.urls["read"]}{endpoint}')
        
    def full_statement(self,payload = None,endpoint='/get_full_statement'):
        
        return super().read(payload=payload,endpoint=f'{self.urls["read"]}{endpoint}')
        
    def account_validation(self,payload = None,endpoint='/get_validation'):
        
        return super().read(payload=payload,endpoint=f'{self.urls["read"]}{endpoint}')
        
    def account_transactions(self,payload = None,endpoint='/get_transactions'):
        
        return super().read(payload=payload,endpoint=f'{self.urls["read"]}{endpoint}')
    
    def serialize(self, payload = None, operation = None):

        data = {}

        if operation is None:
            return "Specify the operation: Resource.BALANCE, Resource.MINI_STATEMENT, Resource.FULL_STATEMENT, Resource.ACCOUNT_VALIDATION or Resource.ACCOUNT_TRANSACTIONS"
        
        if operation == super().BALANCE or operation == super().MINI_STATEMENT or operation == super().ACCOUNT_VALIDATION:            
            
            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": payload.get("reference", "")
                })
                data.update({
                    "AccountNumber": f'{payload.get("account_number", "")}'
                })
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "country_code": payload.get("country_code", "")
                })
                data.update({
                    "account_number": payload.get("account_number", "")
                })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:
                pass

        elif operation == super().FULL_STATEMENT:
            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": payload.get("reference", "")
                })
                data.update({
                    "AccountNumber": f'{payload.get("account_number", "")}'
                })
                data.update({
                    "StartDate": payload.get("start_date", "")
                })
                data.update({
                    "EndDate": payload.get("end_date", "")
                })
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "country_code": payload.get("country_code", "")
                })
                data.update({
                    "account_number": f'{payload.get("account_number", "")}'
                })
                data.update({
                    "start_date": payload.get("start_date", "")
                })
                data.update({
                    "end_date": payload.get("end_date", "")
                })
                data.update({
                    "limit": payload.get("limit", 3)
                })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:
                pass

        elif operation == super().ACCOUNT_TRANSACTIONS:
            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": payload.get("reference", "")
                })
                data.update({
                    "AccountNumber": f'{payload.get("account_number", "")}'
                })
                data.update({
                    "NoOfTransactions": f'{payload.get("limit", "")}'
                })
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                pass

            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:
                pass

        data.update(payload.get("additional_properties", {}))

        return data