import pandas as pd
import pytz
from gql import gql, Client#, AIOHTTPTransport, RequestsHTTPTransport # This is gql version 3
from gql.transport.requests import RequestsHTTPTransport
from loguru import logger
from numpy import nan

from .utils.ut_core import Utils
from .utils.ut_timeseries import UtilsTimeSeries
from . import core

class TimeSeries():

    def __init__(self, accessToken:str, endpoint:str, client:object) -> None:
        global coreClient
        coreClient = client
            
        header = {
            'authorization': 'Bearer ' + accessToken
        }
        
        transport =  RequestsHTTPTransport(url=endpoint, headers=header, verify=True)
        self.client = Client(transport=transport, fetch_schema_from_transport=False)

        return

    def addTimeSeriesItems(self, inventoryName:str, timeSeriesItems:list) -> list:
        """
        Adds new time series and time series group items from a list of 
        dictionaires and returns a list of the created inventoryItemIds.

        Parameters:
        -----------
        inventoryName: str
            The name of the inventory.
        timeSeriesItems: list
            This list contains the properties of the time series item and the properties
            of the time series feature (unit, timeUnit and factor)

        Example:
        >>> timeSeriesItems = [
                {
                'meterId': 'XYZ123',
                'orderNr': 300,
                'isRelevant': True,
                'dateTime': '2020-01-01T00:00:56Z',
                'resolution': {
                    'timeUnit': 'HOUR',
                    'factor': 1,
                    },
                'unit': 'kWh'
                },
                {
                'meterId': 'XYZ123',
                'orderNr': 301,
                'isRelevant': True,
                'dateTime': '2020-01-01T00:00:55Z',
                'resolution': {
                    'timeUnit': 'HOUR',
                    'factor': 1,
                    },
                'unit': 'kWh',
                },
            ]
        >>> client.TimeSeries.addTimeSeriesItems('meterData', timeSeriesItems)
        """
        
        properties = Utils._tsPropertiesToString(timeSeriesItems)
        if properties == None: return

        graphQLString = f'''mutation addTimeSeriesItems {{
            create{inventoryName} (input: 
                {properties}
            )
            {{
                InventoryItems {{
                    _inventoryItemId
                }}
                errors {{
                    message
                }}
            }}
        }} 
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        key = f'create{inventoryName}'
        if result[key]['errors']:
            Utils._listGraphQlErrors(result, key)

        ids = result[key]['InventoryItems']
        idList = [item['_inventoryItemId'] for item in ids]
        logger.info(f"Created {len(idList)} time series items.")

        return idList

    def addTimeSeriesItemsToGroups(self, inventoryName:str, timeSeriesItems:list):
        """Adds new time series items to existing time series groups."""

        properties = Utils._propertiesToString(timeSeriesItems)
        if properties == None: return

        key = f'addTimeSeriesTo{inventoryName}'

        graphQLString = f'''mutation addTimeSeriesItemstoGroup {{
           {key} (input: 
                {properties}
            )
            {{
                InventoryItems {{
                    _inventoryItemId
                }}
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

        try:
            ids = result[key]['InventoryItems']
            idList = [item['_inventoryItemId'] for item in ids]
            logger.info(f"Group instance(s) created.")
        except:
            pass

        return idList

    def setTimeSeriesData(self, inventoryName, inventoryItemId:str, timeUnit:str, factor:int, 
        unit:str, dataPoints:dict, chunkSize:int=10000) -> None:
        """
        Sets new time series data (timestamp & value) to an existing time series or 
        overwrites existing values. The inventoryItemId of the time series is used. As 
        timestamp format you can use UTC (e.g. 2020-01-01T00:01:00Z) or DateTimeOffset 
        (e.g. 2020-01-01T00:00:00+01:00).

        Parameters
        ---------
        inventoryName: str
            The name of the inventory to which the time series belong.
        inventoryItemId: str
            The inventoryItemId to which data is to be written.
        timeUnit: str
            Is the time unit of the time series item
        factor: int
            Is the factor of the time unit
        unit: str
            The unit of the values to be written. 
        dataPoints: dict
            Provide a dictionary with timestamps as keys.
        chunkSize:int = 10000
            Specifies the chunk size of time series values that are written in 
            a single transaction
        
        Example: 
        >>> inventory = 'meterData'
            inventoryItemId = '383202356894015488'
            tsData = {
                '2020-01-01T00:01:00Z': 99.91,
                '2020-01-01T00:02:00Z': 95.93,
            }
            
        >>> client.TimeSeries.setTimeSeriesData(inventory, inventoryItemId,
                'MINUTE', 1, 'W', tsData)
        """
        inventories = core.TechStack.inventories(coreClient, fields=['name', 'inventoryId'])
        inventoryId = Utils._getInventoryId(inventories, inventoryName)
        logger.debug(f"Found inventoryId {inventoryId} for {inventoryName}.")
        key = f'setTimeSeriesData'
        def _setTimeSeriesData(_dataPoints):
           
            graphQLString = f'''
                mutation setTimeSeriesData {{
                setTimeSeriesData(input: {{
                    _inventoryId: "{inventoryId}"
                    _inventoryItemId: "{inventoryItemId}",
                    data: {{
                        resolution: {{
                            timeUnit: {timeUnit}
                            factor: {factor}
                            }}
                        unit: "{unit}"
                        dataPoints: [
                            {_dataPoints}
                        ]
                    }}
                }})
                    {{
                        errors {{
                            message
                        }}
                    }}
                }}
            '''
            try:
                result = Utils._executeGraphQL(self, graphQLString)
            except Exception as err:
                logger.error(err)
                return

            return result

        if len(dataPoints) < chunkSize:
            _dataPoints = UtilsTimeSeries._dataPointsToString(dataPoints)
            result = _setTimeSeriesData(_dataPoints)
            
            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
            else:
                logger.info(f"{len(dataPoints)} data points set for time series {inventoryItemId}.")
            if result == None: return
            return

        else:
            dataPointsCount = 0
            for i in range(0, len(dataPoints), chunkSize):
                sliceDataPoints = UtilsTimeSeries._sliceDataPoints(dataPoints.items(), i, i + chunkSize)
                _sliceDataPoints = UtilsTimeSeries._dataPointsToString(sliceDataPoints)
                result = _setTimeSeriesData(_sliceDataPoints)
                if result == None: continue
                if result[key]['errors']:
                    Utils._listGraphQlErrors(result, key)
                
                dataPointsCount += len(sliceDataPoints)

            logger.info(f"{dataPointsCount} data points set for time series {inventoryItemId}.")

        return

    def setTimeSeriesDataCollection(self, timeSeriesData:list, chunkSize:int=1000) -> None:
        """
        Sets new time series data (timestamp & value) to an existing time series or 
        overwrites existing values. The inventoryItemId of the time series is used. 
        As timestamp format you can use UTC (e.g. 2020-01-01T00:01:00Z) or 
        DateTimeOffset (e.g. 2020-01-01T00:00:00+01:00).

        Parameters
        ----------
        data: list
            A list of dictionaries defining inventory, inventoryItemId, resolution, 
            unit and time series values. Is used to write time series values for
            many time series in one single transaction.
        chunkSize:int = 10000
            Determines the packageSize of time series values that ar written in 
            a single transaction
        
        """
        try:
            _timeSeriesData = UtilsTimeSeries._tsCollectionToString(timeSeriesData)
        except Exception as err:
            logger.error(f"GraphQL string could not be created out of dictionary. Cause: {err}")
            return

        key = f'setTimeSeriesData'        
        graphQLString = f'''
            mutation {key} {{
            {key} (input: {_timeSeriesData})
                {{
                    errors {{
                        message
                    }}
                }}
            }}
        '''
        try:
            result = Utils._executeGraphQL(self, graphQLString)
        except Exception as err:
            logger.error(err)
            return
           
        if result[key]['errors']:
            Utils._listGraphQlErrors(result, key)
        else:
            logger.debug(f"time series data points set.")
        if result == None: return
        return
   
    def timeSeriesData(self, inventoryName:str, fromTimepoint:str, toTimepoint:str, 
        fields:list=['_displayValue'], where:str=None, timeUnit:str=None,
        factor:int=1, aggregationRule:str='AVG', displayMode:str='compressed') -> pd.DataFrame:
        """
        Queries time series data and returns its values and properties 
        in a DataFrame.

        Parameter:
        --------
        inventoryName: str
            The name of the inventory.
        fromTimepoint: str
            The starting timepoint from where time series data will be retrieved. Different
            formats are available. If you use DateTimeOffset, any time zone information will be
            neglected.
        toTimepoint: str
            The ending timepoint from where time series data will be retrieved
        fields:list|str = None
            Uses the displayValue as default. If fields are not unique for each column,
            duplicates will be omitted. If you use multiple fields, a MultiIndex DataFrame will 
            be created. Use inventoryProperties() to find out which properties are available 
            for an inventory. To access MultiIndex use syntax like <df[header1][header2]>.
        where: str = None
            Use a string to add where criteria like
            'method eq "average" and location contains "Berlin"'
            Referenced items are not supported.
        timeUnit: str = None
            The time unit if you want aggregate time series values. Use either 'MILLISECOND', 'SECOND'
            'MINUTE', 'HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR'.
        factor: int = 1
            A factor for time unit aggrergation, e.g. 15 for a 15 MINUTE intervall.
        aggregationRule: str = 'AVG'
            Choose between 'SUM', 'AVG', 'MIN' and 'MAX'.
        displayMode: str = compressed 
            compressed: pivot display with dropping rows and columns that are NaN
            pivot-full: full pivot with all NaN columns and rows
            rows: row display

        Examples:
        ---------
        >>> timeSeriesData('meterData', '2020-10-01', '2020-10-01T:05:30:00Z')
        >>> timeSeriesData('meterData', fromTimepoint='2020-06-01', 
                toTimepoint='2020-06-15', fields=['meterId', 'phase'] 
                where='measure eq "voltage"')    
        """

        #tz = Utils._timeZone(timeZone)

        #_fromTimepoint = _convertTimestamp(fromTimepoint, tz)
        #_toTimepoint = _convertTimestamp(toTimepoint, tz)

        if type(fields) != list:
            _fields = fields
        else:
            _fields = ''
            for header in fields:
                _fields += header + '\n'


        resolvedFilter = ''
        if where != None: 
            resolvedFilter = Utils._resolveWhereString(where)

        if timeUnit != None:
            aggregation = f'''
                aggregation: {aggregationRule}
                resolution: {{timeUnit: {timeUnit} factor: {factor}}}
                '''
        else:
            aggregation = ''

        # if unit != None:
        #     _unit = f'unit:"{unit}"'
        # else:
        #     _unit = ''

        graphQLString = f'''query timeSeriesData {{
                {inventoryName}
                (pageSize: 500 {resolvedFilter})
                {{
                    nodes{{
                        {_fields}
                        _dataPoints (input:{{
                            from:"{fromTimepoint}"
                            to:"{toTimepoint}"
                            {aggregation}
                            }})
                        {{
                            timestamp
                            value
                            flag
                        }}
                    }}
                }}
            }}'''
        
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result[inventoryName]['nodes'], ['_dataPoints'], fields)
        if df.empty:
            logger.info('The query did not produce results.')
            return df
        df.loc[(df.flag == 'MISSING'), 'value'] = nan

        if displayMode == 'pivot-full':
            df = df.pivot_table(index='timestamp', columns=fields, values='value', dropna=False)
            columnNumber = len(result[inventoryName]['nodes'])
            dfColumnNumber = len(df.columns)
            if dfColumnNumber < columnNumber:
                logger.warning(f"{columnNumber-dfColumnNumber} columns omitted due to duplicate column headers.")
        elif displayMode == 'compressed':
            df = df.pivot_table(index='timestamp', columns=fields, values='value', dropna=True)
            columnNumber = len(result[inventoryName]['nodes'])
            dfColumnNumber = len(df.columns)
            if dfColumnNumber < columnNumber:
                logger.warning(f"{columnNumber-dfColumnNumber} columns omitted due to duplicate column headers or NaN-columns")
        elif displayMode == 'rows':
            pass
            #df.index = pd.to_datetime(df.index, format='%Y-%m-%dT%H:%M:%S').tz_convert(pytz.timezone(tz))
                
        # if globalDateTimeFormat == 'dateTime':
        #     df.index = df.index.tz_localize(tz=None)
        
        return df

    def units(self) -> pd.DataFrame:
        """
        Returns a DataFrame of existing units.

        Examples:
        >>> units()
        """

        graphQLString = f'''query getUnits {{
        units
            {{
            name
            baseUnit
            factor
            isBaseUnit
            aggregation
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        return pd.json_normalize(result['units'])

    def createUnit(self, unit:str, baseUnit:str, factor:float, aggregation:str) -> None:
        """
        Creates a unit on basis of a base unit.

        Parameters:
        ----------
        unit : str
            The name of the unit to be created.
        baseUnit : str
            The name of an existing base unit.
        factor : float
            The factor related to the base unit.
        aggregation : str
            The enum value for default aggregation. Possible are 'SUM' and 'AVG' This 
            kind of aggregation is used for integral units (kW -> kWh), which are not supported 
            yet.

        Example:
        >>> createUnit('kW', 'W', 1000, 'AVG')
        """

        graphQLString = f'''
            mutation createUnit {{
                createUnit(input: {{
                    name: "{unit}"
                    baseUnit: "{baseUnit}"
                    factor: {factor}
                    aggregation: {aggregation}}})
                {{
                    errors {{
                        message
                    }}
                }}
            }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        key = f'createUnit'
        if result[key]['errors']:
            Utils._listGraphQlErrors(result, key)
        else:
            logger.info(f"Unit {unit} created.")

        return

    def createBaseUnit(self, baseUnit:str, aggregation:str) -> None:
        """
        Creates a base unit.

        Parameters:
        ----------
        baseUnit : str
            The name of the base unit to be created.
        aggregation : str
            The enum value for default aggregation. Possible are 'SUM' and 'AVG' This 
            kind of aggregation is used for integral units (kW -> kWh), which are not supported 
            yet.

        Example:
        >>> createBaseUnit('W', 'AVG')
        """

        graphQLString = f'''
            mutation createBaseUnit {{
                createBaseUnit(input: {{
                    name: "{baseUnit}"
                    aggregation: {aggregation}}})
                {{
                    errors {{
                        message
                    }}
                }}
            }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        key = f'createBaseUnit'
        if result[key]['errors']:
            Utils._listGraphQlErrors(result, key)
        else:
            logger.info(f"Unit {baseUnit} created.")

        return

    def deleteUnit(self, unit:str, force=False) -> None:
        """
        Deletes a unit. Units can only be deleted if there are no Time Series that use this unit. 
        Base units can only be deleted, if no derived units exist.

        Parameters:
        ----------
        unit : str
            Name of the unit to be deleted.
        force : bool
            Optional, use True to ignore confirmation.
        
        Example:
        >>> deleteUnit('kW', force=True)
        """

        if force == False:
            confirm = input(f"Press 'y' to delete unit '{unit}'")
        else: confirm = 'y'

        graphQLString = f'''
        mutation deleteUnit{{
            deleteUnit (input: {{
                name: "{unit}"
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

        logger.info(f"Unit {unit} deleted.")

        return

