import unittest
from popily_api import *
from settings import API_KEY, CONNECTION_STRING

class APITest(unittest.TestCase):
    def test_add_source(self):
        popily = Popily(API_KEY, url='https://staging.popily.com')

        source_data = {
            'connection_string': CONNECTION_STRING,
            'query': 'SELECT * FROM employees LIMIT 100;',
            'columns': [
                {
                    'data_type': 'rowlabel',
                    'column_header': 'emp_no'
                },
                {
                    'data_type': 'unknown',
                    'column_header': 'first_name'
                },
                {
                    'data_type': 'unknown',
                    'column_header': 'last_name'
                },
                {
                    'data_type': 'datetime',
                    'column_header': 'birth_date'
                },
                {
                    'data_type': 'datetime',
                    'column_header': 'hire_date'
                },
                {
                    'data_type': 'category',
                    'column_header': 'gender'
                }
            ]
        }

        #source = popily.add_source(**source_data)
        #self.assertTrue('id' in source)


    def test_get_sources(self):
        popily = Popily(API_KEY, url='https://staging.popily.com')
        sources = popily.get_sources()
        self.assertTrue('results' in sources)
        self.assertTrue(len(sources['results']) > 0)


    def test_get_source(self):
        popily = Popily(API_KEY, url='https://staging.popily.com')
        source = popily.get_source('employees-limit-100-1')
        self.assertTrue('id' in source)


    def test_get_insights(self):
        popily = Popily(API_KEY, url='https://staging.popily.com')
        insights = popily.get_insights('employees-limit-100-1')
        self.assertTrue('results' in insights)
        self.assertTrue(len(insights['results']) > 0)


    def test_get_insights_columns(self):
        popily = Popily(API_KEY, url='https://staging.popily.com')
        insights = popily.get_insights('employees-limit-100-1',columns=['gender'])
        all_insights = popily.get_insights('employees-limit-100-1')
        self.assertTrue('results' in insights)
        self.assertTrue(len(insights['results']) > 0)
        self.assertTrue(len(all_insights['results']) > len(insights['results']))


    def test_get_insights_filters(self):
        popily = Popily(API_KEY, url='https://staging.popily.com')
        insights = popily.get_insights('employees-limit-100-1',
                                        columns=['gender','hire_date'], 
                                        filters=[{'column':'gender','values': ['F']}],
                                        full=True)
        self.assertTrue('results' in insights)
        self.assertTrue(len(insights['results']) > 0)

        for result in insights['results']:
            self.assertTrue(all([v == 'F' for v in result['z_values']]))


    def test_get_insights_single(self):
        popily = Popily(API_KEY, url='https://staging.popily.com')
        insight = popily.get_insights('employees-limit-100-1',
                                        columns=['gender','hire_date'], 
                                        filters=[{'column':'gender','values': ['F']}],
                                        full=True,
                                        single=True,
                                        insight_actions=['count'])
        self.assertTrue('id' in insight)
        self.assertTrue(all([v == 'F' for v in insight['z_values']]))
        self.assertTrue(insight['insight_action'] == 'count')

        
        insight = popily.get_insights('employees-limit-100-1',
                                        columns=['hire_date'], 
                                        full=True,
                                        single=True,
                                        insight_actions=['ratio'])
        
        self.assertTrue(insight['insight_action'] == 'ratio')

        insight = popily.get_insights('employees-limit-100-1',
                                        columns=['hire_date'], 
                                        full=True,
                                        single=True,
                                        insight_actions=['count'])
        
        self.assertTrue(insight['insight_action'] == 'count')


    def test_customize_insight(self):
        import uuid
        popily = Popily(API_KEY, url='https://staging.popily.com')
        random_title = str(uuid.uuid4().get_hex().upper()[0:6])
        insight = popily.get_insights('employees-limit-100-1',
                                        columns=['gender','hire_date'], 
                                        filters=[{'column':'gender','values': ['F']}],
                                        full=True,
                                        single=True,
                                        insight_actions=['count'],
                                        title=random_title)

        self.assertTrue(insight['title'] == random_title)
        self.assertTrue('embed_url' in insight)


        