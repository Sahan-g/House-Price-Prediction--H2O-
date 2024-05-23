from h2o_wave import main, ui, app, Q
import h2o
import pandas as pd
from model import predict, predict_batch
from house import House

h2o.init()

model = h2o.load_model('./saved_models/StackedEnsemble_BestOfFamily_1_AutoML_3_20240521_131303')


saved_predictions = []

@app('/housepriceprediction')
async def serve(q: Q):
    '''
    main endpoint of the application 
    initailys shows the input form to predict price of a house
    '''

    if not q.client.initialized:
        add_header(q)
        show_sidebar(q)
        add_footer(q)
        show_main_card(q)
        q.client.saved_predictions=[]
        q.client.initialized = True

    if q.args.predict:
        validate_and_predict(q)
    elif q.args.save:
        save_prediction(q)
    elif q.args.view_saved:
        del q.page['batch_upload']
        del q.page['result_table']
        del q.page['main_card']
        show_saved_predictions(q)
       
    elif q.args.single:
        
        del q.page['saved']
        del q.page['batch_upload']
        del q.page['result_table']
        show_main_card(q)
       
        
    elif q.args.batch:
        del q.page['main_card']
        del q.page['saved']
        batch_card(q)
      
    elif q.args.upload_csv:
       
        
        await add_result_table(q)
       
        



    await q.page.save()

def add_header(q: Q):
    '''
    adds the header card to the page.
    '''
    
    q.page['header'] = ui.header_card(
        box='1 1 10 1',
        title='House Price Predictor',
        subtitle='H2O Wave',
        image='https://wave.h2o.ai/img/h2o-logo.svg',
    )

def show_main_card(q: Q, area_error=None, bedrooms_error=None, bathrooms_error=None, prediction=None):

    '''
    The main card of the application
    Contains the fieds that are required to predict the price with the unique neighborhood types

    '''


    df = pd.read_csv('./dataset/housing_price_dataset.csv')

    button_visibillity = True if not prediction else False

    items = [
        ui.text_xl(content='House Details'),
        ui.inline(items=[
            ui.button(name='save', icon='Heart', primary=True),
        ], justify='end'),
        ui.textbox(
            name='area',
            label='Area - SquareFeet',
            value=q.args.area,
            required=True,
            type='number',
            error=area_error
        ),
        ui.inline(items=[
            ui.textbox(
                name='bedrooms',
                label='Number of Bedrooms',
                value=q.args.bedrooms,
                required=True,
                type='number',
                error=bedrooms_error
            ),
            ui.textbox(
                name='bathrooms',
                label='Number of Bathrooms',
                value=q.args.bathrooms,
                required=True,
                type='number',
                error=bathrooms_error
            )
        ], justify='between'),
        ui.inline(items=[
            ui.textbox(
                name='year',
                label='Built Year',
                value=q.args.year,
                required=True,
                type='number',
                error=None
            ),
            ui.dropdown(
                name='neighborhood',
                label='Neighborhood Type',
                value=q.args.neighborhood,
                required=True,
                choices=[ui.choice(name=i, label=i) for i in df['Neighborhood'].unique()],
            )
        ], justify='between'),

        
        ui.buttons([
            ui.button(name='predict', label='Predict',visible=button_visibillity),
        ],justify='center')
    ]


    '''
    If there is prediction this will show 
    '''
    if prediction:
        items.append(ui.text_xl(content=f'Predicted Price: {prediction:.2f}'))

    q.page['main_card'] = ui.form_card(
        box='4 3 4 5',
        items=items
    )

def show_sidebar(q: Q):
    '''
    Adds the side menu which contains the menu options
    '''
    q.page['sidebar'] = ui.nav_card(
        box='1 2 2 7',
        items=[
           ui.nav_group('Menu', items=[
                ui.nav_item(name='single', label='Single Prediction'),
                ui.nav_item(name='batch', label='Batch Prediction'),
                ui.nav_item(name='view_saved', label='View Saved Predictions'),
           ])
        ]
    )

def validate_and_predict(q: Q):
    '''
    Function for validating the user inputs and predicts the price of the house
    
    '''
    bedrooms = q.args.bedrooms
    bathrooms = q.args.bathrooms
    area = q.args.area
    bedrooms_error = None
    bathrooms_error = None
    area_error = None

    
    if bedrooms is not None:
        try:
            bedrooms_value = int(bedrooms)
            if bedrooms_value < 0:
                bedrooms_error = 'Number of bedrooms should be greater than or equal to 0'
        except ValueError:
            bedrooms_error = 'Invalid number'

    
    if bathrooms is not None:
        try:
            bathrooms_value = int(bathrooms)
            if bathrooms_value < 0:
                bathrooms_error = 'Number of bathrooms should be greater than or equal to 0'
        except ValueError:
            bathrooms_error = 'Invalid number'

    
    if area is not None:
        try:
            area_value = int(area)
            if area_value <= 0:
                area_error = 'Area should be greater than 0'
        except ValueError:
            area_error = 'Invalid number'

    if bedrooms_error or bathrooms_error or area_error:
        show_main_card(q, area_error, bedrooms_error, bathrooms_error)
    else:
        house = House(
            area=q.args.area,
            neighborhood=q.args.neighborhood,
            bedrooms=q.args.bedrooms,
            bathrooms=q.args.bathrooms,
            year=q.args.year
        )

        prediction = predict(model, {
            'SquareFeet': house.area,
            'Bedrooms': house.bedrooms,
            'Bathrooms': house.bathrooms,
            'YearBuilt': house.year,
            'Neighborhood': house.neighborhood
        })

        show_main_card(q, prediction=prediction)

def save_prediction(q: Q):

    '''
    Function to save the result of the prediction with all the details
    '''

    house = House(
        area=q.args.area,
        neighborhood=q.args.neighborhood,
        bedrooms=q.args.bedrooms,
        bathrooms=q.args.bathrooms,
        year=q.args.year
    )

    prediction = predict(model, {
        'SquareFeet': house.area,
        'Bedrooms': house.bedrooms,
        'Bathrooms': house.bathrooms,
        'YearBuilt': house.year,
        'Neighborhood': house.neighborhood
    })

    q.client.saved_predictions.append({
        'house': house,
        'prediction': prediction
    })

    show_main_card(q, prediction=prediction)
    

def show_saved_predictions(q: Q):

    '''
    Function to dipplay all the saved predition in a table which enables to comare between each result 
    '''

    rows = []
    for idx, entry in enumerate(q.client.saved_predictions):
        house = entry['house']
        prediction = entry['prediction']
        formatted_prediction = f"{prediction:.2f}"
        rows.append(
            ui.table_row(
                name=str(idx),
                cells=[
                    str(idx + 1),
                    str(house.area),
                    str(house.bedrooms),
                    str(house.bathrooms),
                    str(house.year),
                    house.neighborhood,
                    formatted_prediction
                ]
            )
        )

    items = [
        ui.text_xl(content='Saved Predictions'),
        ui.table(
            name='saved_table',
            columns=[
                ui.table_column(name='id', label='ID', max_width='25', sortable=True),
                ui.table_column(name='area', label='Area (SquareFeet)', max_width='150', sortable=True),
                ui.table_column(name='bedrooms', label='Bedrooms', max_width='100', sortable=True),
                ui.table_column(name='bathrooms', label='Bathrooms', max_width='100', sortable=True),
                ui.table_column(name='year', label='Built Year', max_width='100', sortable=True),
                ui.table_column(name='neighborhood', label='Neighborhood', max_width='150', filterable=True),
                ui.table_column(name='prediction', label='Prediction', max_width='130', sortable=True)
            ],
            rows=rows
        ),
        
    ]
    
    q.page['saved'] = ui.form_card(box='3 2 7 7', items=items)


def  batch_card(q:Q):
     '''
     Adds the card where user can upload a batched file to the server
     '''
     q.page['batch_upload'] = ui.form_card(box='4 3 4 4', items=[
        ui.file_upload(
            name='upload_csv',
            label='Upload csv',
            multiple=False,
            file_extensions=['csv'],
            max_file_size=10, # in MB
            
        )
    ])
     
async def add_result_table(q: Q):

    '''
    Predits prices for all the rows of the csv file and displays the results table
    '''
    
    file_path = await q.site.download(q.args.upload_csv[0], './Uploads')

   
    predictions_df = predict_batch(model=model, file_path=file_path)

   
    df = pd.read_csv(file_path)

   
    df['Predicted Price'] = predictions_df['predict'].round(2)  

    
    table_rows = [
        ui.table_row(
            name=str(index),
            cells=[str(row[col]) for col in df.columns]
        )
        for index, row in df.iterrows()
    ]

    
    table_columns = [
        ui.table_column(name=col, label=col) for col in df.columns
    ]

    
    q.page['result_table'] = ui.form_card(
        box='3 2 7 7', 
        items=[
            ui.text_l(content='Prediction Results'),
            ui.table(
                name='results',
                columns=table_columns,
                rows=table_rows
            ),
            
        ]
    )
def add_footer(q: Q):
    '''
    Adds the footer card to the page.
    '''

    q.page['footer'] = ui.footer_card(
        box='2 9 8',
        caption='House Price Prediction using AUTOML'
    )
