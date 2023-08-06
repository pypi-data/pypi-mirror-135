import json
import pandas as pd
# from ml.data_source.base import DataSource
from SentenceTokenizer import SentenceTokenizer
from takeusecases.ml.data_source.base import DataSource


class DataBase(DataSource):
    
    def __init__(self):
        """
        Constructor.
        
        Parameters
        -----------       
        arg : type
              description
        
        Returns
        -------
        class Object
        """
        pass
    
    def get_data(self)->pd.DataFrame:
        """
        Returns a flat table in Dataframe
        
        Parameters
        -----------         
        arg : type
              description
        
        Returns
        -------
        pd.DataFrame    
            Dataframe with data
        """
        pass
    
    def open_connection(self, connection):
        """
        Opens the connection to the database
        
        Parameters
        -----------         
        connection : string
                     Connection with database
        
        Returns
        -------
        bool
            Check if connection is open or not
            
        """
        pass
    
    def close_connection(self, connection ):
        """
        Close the connection database
        
        Parameters
        -----------         
        connection : string
                     Connection with database
        
        Returns
        -------
        bool
            Check if connection was closed
            
        """
        pass
    
    def clean_owner_caller(self, df):
        
        df = df[df['msgs'].notnull()]
        df = df[df['msgs']>0]
        # Altered by Ramon due to new usage in production
        # df.columns = ['Caller', 'Json', 'msgs']  
        assert 'Caller' in df.columns
        assert 'Json' in df.columns
        assert 'msgs' in df.columns
        
        messages =  []
        for index, row in df.iterrows():
            if isinstance(row['Json'], float)==False:
                info = json.loads(row['Json'])
                for i in info['states']:
                    if 'inputActions' in i:
                        for j in i['inputActions']:
                            if 'type' in j['settings'] and 'content' in j['settings']:
                                if j['settings']['type'] == 'text/plain':
                                    messages.append([row['Caller'],  'Input', j['settings']['content']])
                    if 'outputActions' in i:
                        for j in i['outputActions']:
                            if 'type' in j['settings'] and 'content' in j['settings']:
                                if j['settings']['type'] == 'text/plain':
                                    messages.append([row['Caller'],  'Output', j['settings']['content']])
        
        df_mes = pd.DataFrame(messages, columns=['BotId',  'Type', 'Message'])
        df_mes = df_mes[df_mes['Message'].notnull()]
        tokenizer = SentenceTokenizer()
        df_mes['Message'] = df_mes.Message.apply(lambda x: tokenizer.process_message(x))
        df_mes = df_mes[df_mes['Message'].notnull()]
        df_messages = df_mes[['BotId']].drop_duplicates()  
        df_messages['Message'] = df_mes.groupby(['BotId'])['Message'].transform(lambda x: '. '.join(x))
        return df_messages

