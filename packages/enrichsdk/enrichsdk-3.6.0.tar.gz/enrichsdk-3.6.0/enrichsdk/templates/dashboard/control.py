from django.urls import reverse
from enrichsdk.lib.customer import find_usecase

overview_spec = {
    'name': 'Control Center',
    'description': "Implement and Operate Complex Applications",
    "details": """<p class='text-center'>This dashboard gives an overview of the services enabled on this platform. Click on each tab to see details. The purpose of this platform is to enable strong and continuous model-driven operations.</p>

    <p class='text-center'>Product Owner is <a href=''>Sr. Exec Name</a>, and is currently managed by <a href="https://www.scribbledata.io">Scribble Team</a>.</p>

<p class='text-center'>Please reachout to <a href=''>Data Team</a> or <a href='mailto:support@scribbledata.io'>Scribble Support</a> for technical help</p>""",
    'usecase': find_usecase(__file__),
    'force_list': [],
    'usecases': [
        {
            'name': "ComplexApp",
            'category': 'Finance',
            'owner': 'John Deere',
            'description': 'Complex computation',
            'frequency': 'Daily',
            'services': ['Pipeline', 'App'],
            'datasets': ['many_tables'],
            'status': 'Production'
        },
    ],
    'implement': [
        {
            "category": "Tools",
            'label': "SDK",
            'url': '/docs/sdk/index.html',
            "description": "Developer Interface"
        },
        {
            'category': 'Tools',
            'label': 'Catalog',
            'url': 'APPNAME:catalog:index',
            "description": "Data Schemas and Notes"
        },
    ],
    'operate': [
        {
            'category': 'ComplexAnalysis',
            'label': 'PipelineName',
            'customer': 'UsecaseName',
            'pipeline':  'DailyForecaster',
            'description': 'Daily forecast run'
        },
    ],
    "audit": [
    ],
    "access": [
    ],
    "monitor": [
    ]
}

def get_spec():
    return overview_spec
