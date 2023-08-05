from gql import gql, Client#, AIOHTTPTransport, RequestsHTTPTransport # This is gql version 3
from gql.transport.requests import RequestsHTTPTransport
from loguru import logger
import base64
from numpy.core.records import array

import pandas
import sys
import json
import os
import requests
import pytz
import getpass

from .fileimport import FileImport
from .fileImportService import FileImportService
from .automation import Automation, Schedule
from .programming import Programming

from .utils.ut_core import Defaults, Utils
from .utils.ut_meta import Meta
from .timeseries import TimeSeries

class TechStack(Utils, Meta):
    """
    Initializes a Seven2one TechStack client.

    Parameters:
    ----------
    host: str
        The host domain or ip address, e.g. 'app.organisation.com'
    user: str
        A username
    password: str=None
        The password belonging to the user. If None, it needs to
        be entered interactively.
    logLevel: str='WARNING'
        Change the highest log level. Available log levels are 
        'ERROR', 'WARNING', 'INFO' and 'DEBUG'.
    usePorts: bool=False
        A developer feature: if True, ports with prefix '8' for a
        developer ComposeStack will be used.
    copyGraphQLString: bool=False
        A developer feature: if True, with each method execution, 
        the graphQL string is copied to the clipboard (Windows only).

    Examples:
    >>> client = TechStack('app.orga.com/', 'admin', logLevel='INFO')
    """

    def __init__(self, host:str, user:str, password:str=None, logLevel:str='WARNING', 
        usePorts:bool=False, copyGraphQLString:bool=False) -> object:
               
        try:
            logger.remove()
            logger.add(sys.stderr, format="{level:<10} {time} {message}", level=logLevel, colorize=True)
        except: pass

        if os.name == 'nt': 
            logger.debug('Dectected Windows, enabling pyperclip')
        else:
            logger.debug(f"Dectected platform: {os.name}")


        if password == None:
            password = getpass.getpass('Enter password: ')

        if usePorts == False:
            tokenUrl = f'https://{host}/authn/connect/token'
            dynEndpoint = f'https://{host}/dynamic-objects/graphql/'
            automationEndpoint = f'https://{host}/automation/graphql/'
            scheduleEndpoint = f'https://{host}/schedule/graphql/'
            programmingEndpoint = f'https://{host}/programming/graphql/'
            tsGatewayEndpoint = f'https://{host}/timeseries/graphql/'
            #fileImportServiceEndpoint = f'https://{host}/programming/graphql/'
        else: 
            tokenUrl = f'http://{host}:8040/connect/token'
            dynEndpoint = f'http://{host}:8050/graphql/'
            automationEndpoint = f'http://{host}:8120/graphql/'
            scheduleEndpoint = f'http://{host}:8130/graphql/'
            programmingEndpoint = f'http://{host}:8140/graphql/'
            tsGatewayEndpoint = f'http://{host}:8195/graphql/'
            fileImportServiceEndpoint = f'http://{host}:7200/graphql/'

        body = {
            'client_id': 'techstack-ui',
            'grant_type': 'password',
            'username': user,
            'password': password,
            'scope': 'dynamicobjectservice'
        }

        response = requests.post(tokenUrl, body, verify=True)
        try:
            response =  json.loads(response.text)
            token = response['access_token']
            logger.debug(f"Got Token: {token[:10]}...")
        except:
            logger.error(response)
            return

        header = {
            'authorization': 'Bearer ' + token
        }

        transport =  RequestsHTTPTransport(url=dynEndpoint, headers=header, verify=True)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)  
        self.accessToken = token
        self.scheme = self.client.introspection

        # Defaults:
        Utils._getDefaults()
        Defaults.copyGraphQLString = copyGraphQLString
            
        # self.timeZone = defaults['timeZone']
        # self.dateTimeFormat = defaults['dateTimeFormat']

        try:
            self.TimeSeries = TimeSeries(self.accessToken, tsGatewayEndpoint, self)
            self.FileImport = FileImport(self, self.TimeSeries)
        except Exception as err:
            logger.warning(f"Time series gateway not available")
            logger.debug(f"Reason: {err}")
            self.FileImport = FileImport(self)

        try:
            self.FileImportService = FileImportService(fileImportServiceEndpoint)
        except Exception as err:
            logger.debug(f"File import service not available")
            logger.debug(f"Reason: {err}")
        
        try:
            self.Automation = Automation(self.accessToken, automationEndpoint)
        except Exception as err:
            logger.warning(f"Automation service not available")
            logger.debug(f"Reason: {err}")
        
        try:
            self.Schedule = Schedule(self.accessToken, scheduleEndpoint)
        except Exception as err:
            logger.warning(f"Schedule service not available")
            logger.debug(f"Reason: {err}")

        try:
            self.Programming = Programming(self.accessToken, programmingEndpoint)
        except Exception as err:
            logger.warning(f"Programming service not available")
            logger.debug(f"Reason: {err}")

        return

    def inventories(self, fields:list=None, where:str=None, orderBy:str=None, 
        asc:bool=True) -> pandas.DataFrame:
        """
        Returns a DataFrame of existing inventories.

        Parameters:
        ----------
        fields: list=None
            The list of fields to be queried, e.g.
            ['name', 'inventoryId, variant.name']
        where: str=None
            Use a string to add where criteria like 'name eq "meterData"'.
            The argument is momentarily very limited.
        orderBy: str=None
            Select one field to sort by.
        asc: bool=True
            Determines the sort order of items. Set to False to apply descending order.

        Examples:
        >>> getInventories()
        >>> getInventories(fields=['name', 'inventoryId'], 
                where='city eq "Hamburg"', 
                orderBy='variant', asc=True)
        """

        if fields == None:
            fields = ['name', 'inventoryId', 'variant.name', 'historyEnabled', 'hasValidityPeriods', 'isDomainUserType']
            _fields = Utils._queryFields(fields, recursive=True)
        else:
            try:
                _fields = Utils._queryFields(fields, recursive=True)
            except:
                logger.error("Fields must be provided as list, e.g. ['name', 'inventoryId, variant.name']")

        resolvedFilter = ''
        if where != None: 
            resolvedFilter = Utils._resolveWhereString(where)

        if orderBy != None:
            if asc != True:
                _orderBy = f'order: {{ {orderBy}: DESC }}'
            else:
                _orderBy = f'order: {{ {orderBy}: ASC }}'
        else: _orderBy = ''

        graphQLString= f'''query getInventories {{
        inventories 
            (first: 50 {_orderBy} {resolvedFilter})
            {{
            nodes {{
                {_fields}
                }}
            }}
        }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pandas.json_normalize(result['inventories']['nodes'])
        return df

    def items(self, inventoryName:str, references:bool=False, fields:list=None, where:str=None, 
        pageSize:int=5000, orderBy:str=None, asc:bool=True) -> pandas.DataFrame:
        """
        Returns items of an inventory in a DataFrame.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        references : bool
            If True, items of referenced inventories will be added to the DataFrame. If
            the fields-parameter is used, this parameter is ignored.
        fields : list | str
            A list of all properties to be queried. If None, all properties will be queried.
            For referenced items use a '.' between inventory name and property.
        pageSize : int
            The page ize of items that is used to retrieve a large number of items.
        where : str
            Use a string to add where criteria like
            'method eq "average" and location contains "Berlin"'.
            Referenced items are not supported.
        orderBy : str
            Select a field to sort by.
        asc : bool
            Determines the sort order of items. If set to False, a descending order 
            is applied.

        Example:
        --------
        >>> items('appartments', references=True)
        """


        # tz = globalTimeZone

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)
        else:
            properties = Utils._properties(self, inventoryName, recursive=True)
            properties = Utils._propertyList(properties, recursive=references)
            
            _fields = Utils._queryFields(properties, recursive=references)

        if len(_fields) == 0:
            logger.error(f"Inventory '{inventoryName}' not found.")
            return

        resolvedFilter = ''
        if where != None: 
            resolvedFilter = Utils._resolveWhereString(where)
        
        if orderBy != None:
            if asc != True:
                _orderBy = f'order: {{ {orderBy}: DESC }}'
            else:
                _orderBy = f'order: {{ {orderBy}: ASC }}'
        else: _orderBy = ''

        result = []
        count = 0
        lastId = ''

        while True:
            graphQLString= f''' query getItems {{
                    {inventoryName} 
                    (pageSize: {pageSize} {lastId} {resolvedFilter} {_orderBy})
                    {{
                        edges {{
                            cursor
                            node {{
                                {_fields}
                            }}
                        }}
                    }}
                }}
                '''
            try:
                query = gql(graphQLString)
            except Exception as err:
                logger.error(err)
                return

            if count == 0:
                Utils._copyGraphQLString(graphQLString)

            try:
                _result = self.client.execute(query)
            except Exception as err:
                logger.error(err)
                return
            
            if _result[inventoryName]['edges']:
                result += _result[inventoryName]['edges']
                count += 1
            try:
                cursor = _result[inventoryName]['edges'][-1]['node']['_inventoryItemId']
                lastId = f'lastId: "{cursor}"'
            except: 
                break

        df = pandas.json_normalize(result)
        # Remove cursor columns and remove 'node' prefix
        try:
            del df['cursor']
        except: pass

        cols = [col.replace('node.','') for col in df.columns]
        df.columns = cols
        
        return df

    def inventoryProperties(self, inventoryName, namesOnly=False):
        """
        Returns a DataFrame of a query of properties of an inventory.

        Parameters:
        ----------
        inventoryName : str
            The name of the inventory.
        namesOnly : bool
            If True, only property names will be returned

        Example:
        --------
        >>> inventoryProperties('appartments') 


        """

        propertyFields = f'''
            name
            id
            type
            ... Scalar
            isArray
            nullable
            ... Reference
        '''

        graphQLString= f'''query Inventory {{
        inventory
            (inventoryName: "{inventoryName}")
            {{
            properties {{
                {propertyFields}
                }}
            }}
        }}
        fragment Scalar on IScalarProperty {{
            dataType
            }}
        fragment Reference on IReferenceProperty {{
            inventoryId
            inventoryName
        }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pandas.json_normalize(result['inventory']['properties'])

        if namesOnly == True:
            return list(df['name'])
        else:
            return df

    def propertyList(self, inventoryName, references=False, dataTypes=False):
        """
        Returns a list of properties of an inventory and its referenced inventories
        by reading out the scheme.

        Parameters:
        ----------
        inventoryName : str
            The name of the inventory.
        references : bool
            If True, properties of referenced inventories included.
        dataTypes : bool
            If True, result will be displayed as Series with properties as index and
            dataTypes as values.

        Example:
        --------
        >>> inventoryList('appartments') 

        """

        if references != True:
            _properties = Utils._properties(self, inventoryName=inventoryName)
        else:
            _properties = Utils._properties(self, inventoryName=inventoryName, recursive=True)

        if dataTypes == False:
            properties = Utils._propertyList(_properties)
        else:
            properties = pandas.Series(Utils._propertyTypes(_properties))

        return properties

    def addItems(self, inventoryName:str, items:list) -> str:
        """
        Adds from a list of dicts new items and returns a list
        of inventoryItemIds.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        items : list
            A list with dictionaries for each item.

        Example:
        --------
        >>> items = [
                {
                'meterId': '86IEDD99',
                'dateTime': '2020-01-01T05:50:59Z'
                },
                {
                'meterId': '45IXZ52',
                'dateTime': '2020-01-07T15:41:14Z'
                }
            ]
        >>> addItems('meterData', items)
        """
        items = Utils._propertiesToString(items)
        #_inventoryFieldName = utils._upperFirst(inventoryFieldName)

        graphQLString= f'''mutation addItems {{
            create{inventoryName} (input: 
                {items}
            )
            {{
                errors {{
                    message
                }}
                    InventoryItems {{
                _inventoryItemId
                }}
            }}
        }} 
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        key = f'create{inventoryName}'

        if result[key]['errors']:
            Utils._listGraphQlErrors(result, key)
        return result[key]['InventoryItems']

    def updateItems(self, inventoryName:str, items:list) -> None:
        """
        Updates from a list of dicts existing items. The '_inventoryItemId'
        must be passed to each item.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        items : list
            A list with dictionaries for each item.

        Example:
        --------
        >>> items = [
                {
                '_inventoryItemId':'118312438662692864',
                'meterId': '86IEDD99',
                'dateTime': '2020-01-01T05:50:59Z'
                },
                {
                '_inventoryItemId':'118312438662692864',
                'meterId': '45IXZ52',
                'dateTime': '2020-01-07T15:41:14Z'
                }
            ]
        >>> updateItems('meterData', items)
        """
        items = Utils._propertiesToString(items)
        #_inventoryFieldName = utils._upperFirst(inventoryFieldName)

        graphQLString= f'''mutation updateItems {{
            update{inventoryName} (input: 
                {items}
            )
            {{
                errors {{
                    message
                }}
                InventoryItems {{
                    _inventoryItemId
                }}
            }}
        }} 
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        key = f'update{inventoryName}'

        if result[key]['errors']:
            Utils._listGraphQlErrors(result, key)

        logger.info(f"{len(result[key]['InventoryItems'])} item(s) updated.")
        return

    def createInventory(self, name:str,  properties:list, variant:str=None, 
        propertyUniqueness:dict=None, historyEnabled:bool=False, 
        hasValitityPeriods:bool=False, isDomainUserType:bool=False) -> str:
        """
        Creates a new inventory. After creation, access rights must be set to add items.
        
        Parameters:
        ----------
        name : str
            Name of the new inventory (only alphanumeric characters allowed, 
            may not begin with a number)
        properties : list
            A list of dicts with the following mandatory keys: 
                name: str
                dataType: enum (STRING, BOOLEAN, DECIMAL, INT, LONG, DATE_TIME, 
                DATE_TIME_OFFSET)
            Optional keys:
                isArray: bool (Default = False)
                nullable: bool (Default = True)
                isReference: bool (Default = False)
                inventoryId: str (mandatory if hasReference = True)
        variant : str
            The inventory variant.
        propertyUniqueness : list
            A list of properties that should be unique in its combination. 
        historyEnabled : bool
            If True, changes in properties will be recorded in item history.
        hasValidityPeriods : bool
            If true, a validity period can be added to the item.    

        Example:
        --------
        >>> propertyDefinitions = [
            {
                'name': 'street',
                'dataType': 'STRING',
                'nullable': False,
            },
            {
                'name': 'postCode',
                'dataType': 'STRING',
                'nullable': False,
            },
            ]
            uniqueness = [{'uniqueKey': 'address', 'properties': ['street', 'postCode']}
        >>> createInventory('appartment', 'propertyDefinitions', propertyUniqueness=uniqueness) 
        """

        _properties = Utils._propertiesToString(properties)

        if variant != None:
            _variantId = Utils._getVariantId(self.variants(), variant) 
            logger.debug(f"Found variantId: {_variantId}")
            if type(_variantId) != str:
                logger.error(f"Variant name '{name} not found")
                return
        else: _variantId = ''

        if propertyUniqueness != None:
            _propertyUniqueness = 'propertyUniqueness: ' + Utils._uniquenessToString(propertyUniqueness)
            logger.debug(_propertyUniqueness)
        else: _propertyUniqueness = ''

        _history = 'true' if historyEnabled != False else 'false'
        _validityPeriods = 'true' if hasValitityPeriods != False else 'false'
        _domainUser = 'true' if isDomainUserType != False else 'false'
        

        
        graphQLString= f'''
        mutation createInventory {{
            createInventory (input: {{
                name: "{name}"        
                properties: {_properties}
                variantId: "{_variantId}"
                historyEnabled: {_history}
                hasValidityPeriods: {_validityPeriods}
                isDomainUserType: {_domainUser}
                {_propertyUniqueness}
                }})
            {{
            inventory {{
                inventoryId
            }}
            errors {{
                code
                message
                }}
            }}
        }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        if result['createInventory']['errors']:
            Utils._listGraphQlErrors(result, 'createInventory')
            return

        logger.info(f"New inventory {name} created.")
 
        return result['createInventory']['inventory']['inventoryId']

    def deleteInventory(self, inventoryName:str, force:bool=False) -> str:
        """ 
        Deletes an inventory with all its containg items. 
        
        Parameters:
        -----------
        inventoryName : str
            The field name of the inventory.
        force : bool
            Use True to ignore confirmation.

        Example:
        ---------
        >>> deleteInventory('meterData', force=True)
        """

        inventory = self.inventories(where=f'name eq "{inventoryName}"')
        
        if inventory.empty:
            logger.error(f'Unknown inventory "{inventoryName}".')
        inventoryId = inventory.loc[0, 'inventoryId']
        logger.debug(f'_inventoryId: {inventoryId}')

        if force == False:
            confirm = input(f"Press 'y' to delete '{inventoryName}': ")

        graphQLString= f'''mutation deleteInventory {{
            deleteInventory (input:{{inventoryId: "{inventoryId}"}})
            {{ 
                errors {{ 
                    code
                    message
                }}
            }}
            }}
            '''

        if force == True: confirm = 'y'
        if confirm == 'y':
            result = Utils._executeGraphQL(self, graphQLString)
            if result == None: return
            if result['deleteInventory']['errors']:
                Utils._listGraphQlErrors(result, 'deleteInventory')
            else: 
                logger.info(f"Inventory '{inventoryName}' deleted.")
        else: return

    def variants(self) -> pandas.DataFrame:
        """
            Returns a dataframe of available variants.
        """

        graphQLString= f'''query getVariants {{
        variants
            (first: 50)
            {{
            nodes {{
                name
                variantId
                }}
            }}
        }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pandas.json_normalize(result['variants']['nodes'])
        return df

    def clearInventory(self, inventoryName:str, force=False):
        """
        Deletes all items from the inventory

        Parameters
        -----------
        inventoryName : str
            The name of the inventory.
        force : bool
            Use True to ignore confirmation.
        """

        _result =self.items(inventoryName, ['_inventoryItemId', 'inventoryId'])
        if _result.empty:
            logger.info(f"Inventory {inventoryName} has no items.")
            return
        _inventoryItemIds = list(_result['_inventoryItemId'])

        _ids = ''
        for id in _inventoryItemIds:
            _ids += f'{{_inventoryItemId: "{id}"}}\n'    
      
        logger.debug(f"GraphQL Ids: {_ids}")
            
        if force == False:
            confirm = input(f"Press 'y' to delete  {len(_inventoryItemIds)} items: ")

        graphQLString= f'''
            mutation deleteItems {{
                delete{inventoryName} ( input: 
                    [{_ids}]
                )
                {{
                errors {{
                    code
                    message
                    }}
                }}
            }}
            '''

        if force == True: confirm = 'y'
        if confirm == 'y':
            result = Utils._executeGraphQL(self, graphQLString)
            if result == None: return
        else:
            return

        if result[f'delete{inventoryName}']['errors'] != None:
            Utils._listGraphQlErrors(result, f'delete{inventoryName}')
        else:
            logger.info(f"{len(_inventoryItemIds)} items deleted.")

    def deleteItems(self, inventoryName:str, inventoryItemIds:list=None, where:str=None, force=False):
        """
        Deletes inventory items from a list of inventoryItemIds or by where-criteria. 

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        items : list
            A list of inventoryItemIds that should be deleted.
        where : str
            Filter criteria to select items that should be deleted.
            Referenced items are not supported.
        all : bool
            All items of the inventory will be deleted
        force : bool
            Use True to ignore confirmation.

        Examples:
        ---------
        >>> deleteItems('meterData', where='changeDate gt "2020-12-01"', force=True)
        >>> deleteItems('meterData', inventoryItemIds=['ef73d6d5-d1d7-459a-b079-ec640cbb310e'])
        """

        if inventoryItemIds == None and where == None:
            logger.error(f"No list of items and no where-criteria were provided.")
        if inventoryItemIds != None and where != None:
            logger.warning(f"List of items and where-criteria has been provided. Item list is used.")

        if where != None:
            _result =self.items(inventoryName, ['inventoryItemId', 'inventoryId'], 
                where=where)
            if _result.empty:
                logger.info(f"The where criteria '{where}' led to no results.")
                return

            _inventoryItemIds = list(_result['_inventoryItemId'])
            
        if inventoryItemIds != None:
            _inventoryItemIds = inventoryItemIds

        _ids = ''
        for id in _inventoryItemIds:
            _ids += f'{{_inventoryItemId: "{id}"}}\n'    
      
        logger.debug(f"GraphQL Ids: {_ids}")
            
        if force == False:
            confirm = input(f"Press 'y' to delete  {len(_inventoryItemIds)} items: ")

        graphQLString= f'''
            mutation deleteItems {{
                delete{inventoryName} ( input: 
                    [{_ids}]
                )
                {{
                errors {{
                    code
                    message
                    }}
                }}
            }}
            '''
        

        if force == True: confirm = 'y'
        if confirm == 'y':
            result = Utils._executeGraphQL(self, graphQLString)
            if result == None: return
        else:
            return

        if result[f'delete{inventoryName}']['errors'] != None:
            Utils._listGraphQlErrors(result, f'delete{inventoryName}')
        else:
            logger.info(f"{len(_inventoryItemIds)} items deleted.")

    def updateVariant(self, variantName, newName=None, icon=None) -> None:
        """Updates a variant"""

        _variantId = Utils._getVariantId(self.variants(), variantName) 
        logger.debug(f"Found variantId: {_variantId}")
        if type(_variantId) != str:
            logger.er

        if newName != None:
            _name = f'name: "{newName}"'
        else:
            _name = ''

        if icon != None:
            _icon =f'icon: "{icon}"'
        else:
            _icon =''

        graphQLString = f'''mutation updateVariant {{
            updateVariant (input:{{
                variantId: "{_variantId}"
                {_name}
                {_icon}
                }})
            {{ 
                errors {{ 
                    code
                    message
                }}
            }}
            }}
            '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return
        print(result)
        # if result['updateVariant']['errors'] != 'None':
        #     Utils._listGraphQlErrors(result, 'updateVariant')
        # else: 
        #     logger.info(f"Variant '{variantName}' updated.")

        return

    def updateArrayProperty(self, inventoryName:str, inventoryItemId:str, arrayProperty:str, 
        operation:str, arrayItems:list=None, cascadeDelete:bool=False) -> None:
        """
        Updates a single array property of a single inventoryItemId. Arrays with and without 
        references are supported.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory where the item is located.
        inventoryItemId : str
            The inventory item id of the item.
        arrayProperty : str
            The name of the property whose array items are to be updated.
        operation : str
            The update operation to be performed. Options:
            insert: inserts a list of array items.
            removeById: removes array items by a list of given (item) ids.
            removeByIndex: removes array items by a list of given indices.
            removeAll: removes all array items
        cascadeDelete : bool (False)
            If array items are refencences, True will delete also the reference items. 

        Examples:
        ---------
        >>> client.updateArrayProperty('meterData', '118718694909018112',
                'timeSeries', action='insert', arrayItems=['387964598252380179'])
        >>> client.updateArrayProperty('meterData', '118718694909018112',
                'timeSeries', action='removeByIndex', arrayItems=[0,1], cascadeDelete=True)
        """


        operations = ['insert', 'removeById', 'removeByIndex', 'removeAll']
        if operation not in operations:
            logger.error(f"Action '{operation}' allowed. Possible update operations: {operations} ")

        if operation == 'removeAll':
            try:
                arrDf= TechStack.items(self, inventoryName, fields=[f'{arrayProperty}._inventoryItemId'],
                    where=f'_inventoryItemId eq "{inventoryItemId}"')
            except Exception as err:
                logger.error(err)
                return
            countArray = len(arrDf.iloc[0,0])
            arrayItems = [num for num in range(countArray)]
        _arrayItems = Utils._arrayItemsToString(arrayItems, operation, cascadeDelete)

        graphQLString = f'''mutation updateArray {{
            update{inventoryName}ArrayProperties(
                input: {{
                _inventoryItemId: "{inventoryItemId}"
                {arrayProperty}: {{
                    {_arrayItems}
                    }}
                }}
            ) {{
                errors {{
                message
                }}
            }}
        }}'''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        key = f'update{inventoryName}ArrayProperties'
        if result[key]['errors'] != None:
            Utils._listGraphQlErrors(result, key)
        else:
            logger.info(f"Array property {arrayProperty} for item {inventoryItemId} updated.")

    def addInventoryProperties(self, inventoryName:str, properties:list) -> None:
        """
        Adds one or more inventory properties to an existing inventory.

        Parameters:
        ----------
        inventoryName: str
            Name of inventory
        properties: list
            A list of dicts with the following mandatory keys: 
                name: str
                dataType: enum (STRING, BOOLEAN, DECIMAL, INT, LONG, DATE_TIME, 
                DATE_TIME_OFFSET)
            Optional keys:
                isArray: bool (Default = False)
                nullable: bool (Default = True)
                isReference: bool (Default = False)
                inventoryId: str (mandatory if hasReference = True)
        """

        key = 'addProperty' 
        inventory = self.inventories(where=f'name eq "{inventoryName}"')
        
        if inventory.empty:
            logger.error(f'Unknown inventory "{inventoryName}".')
        inventoryId = inventory.loc[0, 'inventoryId']
        _properties = Utils._propertiesToString(properties)

        graphQLString= f'''
        mutation {key} {{
        {key} (input: {{
            inventoryId: "{inventoryId}"	
            properties: {_properties}
            }}) 
            {{
                errors {{
                    message
                }}
            }}
        }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        if result[key]['errors']:
            Utils._listGraphQlErrors(result, key)
            return
        else:
            logger.info(f"New property(ies) added.")

    def resync(self) -> None:
        """Resynchornizes read databases"""

        key = 'reSyncReadDatabase'
        graphQLString= f'''mutation resync{{
            {key}
            }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        return result
    
    def defaultDataFrame(self, maxRows, maxColumns):
        """Sets default sizes for a DataFrame for the current session"""
        pandas.options.display.max_rows = maxRows
        pandas.options.display.max_columns = maxColumns
        return
# Some stand alone functions

def setGlobalDefault(default:str, value:object, verbose:bool=False) -> None:
    """
    Sets a default value for a specific option.
    Available defaults:
    timeZone : str
        A time zone provided in IANA or isoformat (e.g. 'Europe/Berlin' or 'CET')
    dateTimeFormat: str
        Use 'dateTimeOffSet' or 'dateTime'

    Parameters:
    -----------
    default : str
        Choose a default, e.g. 'timeZone'.
    value : object
        Choose a value to be set as default.
    verbose : bool
        If True, config file information will be shown.
    """
    #global globalTimeZone, globalDateTimeFormat

    ## Check for valid defaults:
    defaults = ['timeZone', 'dateTimeFormat', 'copyGraphQLString']
    if default not in defaults:
        raise ValueError(f"Unknown default '{default}'.")

    ## Check config file and create if not existing:
    path = os.path.abspath(__file__)
    path = path.replace('core.py', 'config.json')
    if verbose: print(f"Path to config file: '{path}'")

    try:
        with open(path, 'r') as configFile:
            content = json.load(configFile)
    except:
        print('I excepted')
        with open(path, 'w') as configFile:
            content = {
                'timeZone': 'local',
                'dateTimeFormat': 'dateTimeOffset',
                'copyGraphQLString': False
                }
            json.dump(content, configFile, indent=4)
    
    ## Check for valid values:
    if default == 'timeZone':
        pytz.timezone(value)
        globalTimeZone = value
    if default == 'dateTimeFormat':
        if value not in ['dateTimeOffset', 'dateTime']:
            raise ValueError(f"'{value}' is no valid DateTime format. Use 'dateTimeOffset' or 'dateTime'")
        globalDateTimeFormat = value
    if default == 'copyGraphQLString':
        if value not in [True, False]:
            raise TypeError(f"'{value}' is not valid. Use True or False.")
    # if default == 'saveAccessToken':
    #     if value not in [True, False]:
    #         raise TypeError(f"'{value}' is not valid. Use True or False.")
    # if default == 'tokenValidityHours':
    #     if type(value) != int:
    #         raise TypeError(f"'{value}' is not valid. Use an integer number.")

    ## New content
    content[default] = value
    print(content)

    ## Write to config file:
    with open(path, 'w') as configFile:
        #content = json.load(configFile)
        if verbose: print(f"Current settings of config file: \n {content}")
        json.dump(content, configFile, indent=4)
    if verbose: print(f"{default} set to {value}.")
    return

def encodeBase64(file:str):
    with open(file) as file:
        content = file.read()
        content = base64.b64encode(content.encode('ascii'))
        return content.decode('UTF8')
        
def decodeBase43(content:str):
    return base64.b64decode(content)