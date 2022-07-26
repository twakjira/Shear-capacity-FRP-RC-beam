import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import pickle

EXPANDER_TEXT = """
    To change the current theme 🎈 
    In the app menu (☰ -> Settings -> Theme).
    """
    
READ_ME = """
To use the app, define the values of the predictors using sliders on the left side of the screen. 
The defined beam parameters are displayed under the section "User defined parameters"
the predicted Shear capacity of the beam will be updated under the section "Predicted Shear Capacity".
🎈 
"""
# Primary accent for interactive elements
primaryColor = 'red'

# Background color for the main content area
backgroundColor = '#273346'

#st.markdown(html_temp, unsafe_allow_html=True)
#alam = Image.open('ALAMS.png')
#st.image(alam, use_column_width=True)
#st.image(alam,width=450)



html_temp = """
<div style="background-color:black ;padding:10px">
<h2 style="color:cyan;text-align:center;"> 
Shear Capacity Prediction of FRP-RC Beams Using Machine Learning 
</h2>
</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)

#st.write("### By [Tadesse G. Wakjira](https://scholar.google.com/citations?user=Ka3iXSoAAAAJ)")
#import the dataset
dff = pd.read_excel('data.xlsx', sheet_name = 'data')
xx=dff.copy(deep=True)


fiber_long=[]
fiber_trans=[]
for i in range(xx.shape[0]):
    if xx['FRP longitudinal type'][i]=='AFRP':
        fiber_long.append(1)
    elif xx['FRP longitudinal type'][i]=='BFRP':
        fiber_long.append(2)
    elif xx['FRP longitudinal type'][i]=='CFRP':
        fiber_long.append(3)
    elif xx['FRP longitudinal type'][i]=='GFRP':
        fiber_long.append(4)
        
for i in range(xx.shape[0]):
    if xx['FRP web type'][i]==0:
        fiber_trans.append(0)
    if xx['FRP web type'][i]=='AFRP':
        fiber_trans.append(1)
    elif xx['FRP web type'][i]=='BFRP':
        fiber_trans.append(2)
    elif xx['FRP web type'][i]=='CFRP':
        fiber_trans.append(3)
    elif xx['FRP web type'][i]=='GFRP':
        fiber_trans.append(4)        
        
xx['FRP longitudinal type'] = fiber_long
xx['FRP web type'] = fiber_trans

df = xx.copy(deep=True)     



""
with st.beta_expander("Read me"):
    st.write(READ_ME)
with st.beta_expander("To change Theme"):
    st.write(EXPANDER_TEXT)

""
""

# Header
st.sidebar.header('Define the beam parameters')
t=14
def user_defined_paremeters():
    b = st.sidebar.slider('Width of the beam, bw (mm)', float(df['bw'].min()), float(df['bw'].max()),
                               float(df['bw'][t]))
    d = st.sidebar.slider('Effective depth of the beam, d (mm)', float(df['d'].min()), float(df['d'].max()),
                               float(df['d'][t]))
    fc = st.sidebar.slider('Compressive strength of concrete, fc (MPa)', float(df['fc'].min()), 
                            float(df['fc'].max()),
                            float(df['fc'][t]))
    rohfl = st.sidebar.slider('FRP longitudinal reinforcement ratio , rohfl (%)', float(df['rohfl'].min()), 
                            float(df['rohfl'].max()),
                            float(df['rohfl'][t]))    
    Efl = st.sidebar.slider('Elastic modulus of longitudinal FRP reinforcement, Efl (GPa)', float(df['Efl'].min()/1000), 
                            float(df['Efl'].max()/1000),
                            float(df['Efl'][t]/1000))   
    fful = st.sidebar.slider('Tensile strength of FRP shear reinforcement, fful (MPa)', float(df['fful'].min()), 
                            float(df['fful'].max()),
                            float(df['fful'][t]))
    FRP_long_type1 = st.sidebar.radio('FRP longitudinal bar type', ('AFRP', 'BFRP', 'CFRP', 'GFRP'))

    rohfw = st.sidebar.slider('FRP shear reinforcement ratio , rohfv (%)', float(df['rohfw'].min()), 
                            float(df['rohfw'].max()),
                            float(df['rohfw'][t]))    
    Efw = st.sidebar.slider('Elastic modulus of transverse FRP reinforcement, Efw (GPa)', float(df['Efw'].min()/1000), 
                            float(df['Efw'].max()/1000),
                            float(df['Efw'][t]/1000))    
    ffuw = st.sidebar.slider('Tensile strength of FRP shear reinforcement, ffuv (MPa)', float(df['ffuw'].min()), 
                            float(df['ffuw'].max()),
                            float(df['ffuw'][t])) 
    FRP_shear_type1 = st.sidebar.radio('FRP shear reinforcement bar type', ('AFRP', 'BFRP', 'CFRP', 'GFRP'))

    a_d = st.sidebar.slider('shear span-to-depth ratio', float(df['a/d'].min()), 
                            float(df['a/d'].max()),
                            float(df['a/d'][t])) 



     #fiber1 = fiber.astype('category')
    if FRP_long_type1 == 'AFRP':
        FRP_long_type = 0
    elif FRP_long_type1 == 'BFRP':
        FRP_long_type = 1
    elif FRP_long_type1 == 'CFRP':
        FRP_long_type = 2
    elif FRP_long_type1 == 'GFRP':
        FRP_long_type = 3
    
    #fiber1 = fiber.astype('category')
    if FRP_shear_type1 == 0:
        FRP_shear_type = 0
    elif FRP_shear_type1 == 'AFRP':
        FRP_shear_type = 1
    elif FRP_shear_type1 == 'BFRP':
        FRP_shear_type = 2
    elif FRP_shear_type1 == 'CFRP':
        FRP_shear_type = 3
    elif FRP_shear_type1 == 'GFRP':
        FRP_shear_type = 4

       
    data = {'b': b,
            'd': d,
            'fc': fc,
            'rohfl': rohfl,
            'Efl': Efl,
            'fful': fful,
            'FRP longitudinal type': FRP_long_type, 
            'rohfw': rohfw,
            'Efw': Efw,
            'ffuw': ffuw,
            'FRP web type':FRP_shear_type,
            'a/d':a_d,

            }

    features = pd.DataFrame(data, index=[0])
    return features

df1 = user_defined_paremeters()

#st.header('User defined parameters')
html_temp = """
<div style="background-color:gray ;padding:10px">
<h2 style="color:white;text-align:center;">User defined parameters </h2>
</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)

st.write('#### Beam geometry and mechanical properties of material')

df2 = df1.copy(deep=True)
# df2['Ef'] = 0.001*df1['Ef']

st.write(df2[['b', 'd', 'fc', 'rohfl', 'Efl', 'fful', 'FRP longitudinal type', 'rohfw', 'Efw', 'ffuw', 'FRP web type', 'a/d']])

st.write('---')

# Normalize the user defined variables 
dfn=[]
for i in range(0,df1.shape[1]):
    a = (df1.iloc[:,i]-df.iloc[:,i].min())/(df.iloc[:,i].max()-df.iloc[:,i].min())
    dfn.append(a)
    
dfn = pd.DataFrame(np.array(dfn)).T.values


# dfn = pd.DataFrame(np.array(dfn)).T
# x=df.iloc[:,:-1]
# dfn.columns = x.columns

model = pickle.load(open('model.pkl', 'rb'))
#model.__getstate__()['_sklearn_version']

#from joblib import dump, load
#model = load('super_learner.dat', mmap_mode='r')


Vpred =model.predict(dfn)[0]

# Inverse normalization
# observed responses
yy1 = df['V'].values

# predicted responses
y1=round(yy1.min()+(yy1.max()-yy1.min()) * Vpred, 2)


html_temp = """
<div style="background-color:teal ;padding:10px">
<h2 style="color:white;text-align:center;">Predicted Shear capacity of the beam </h2>
</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)
st.write('## Shear capacity (kN) =', y1)

st.write('---')



# SHAP explanation
#st.header('Model explanation using SHAP approach and significance of the input factors')
html_temp = """
<div style="background-color:gray ;padding:10px">
<h2 style="color:white;text-align:center;">Model explanation using SHAP approach and significance of the input factors </h2>
</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)

st.markdown('## **SHAP summary plot**')
image = Image.open('shap_plot.png')
st.image(image, use_column_width=True)
#st.markdown('## **Significance and effect of each parameter**')
#image = Image.open('importance_plot.tiff')
#st.image(image, use_column_width=True)
#st.markdown('**Positive effect increases the load-carrying capacity, while negative effect reduces the load-carrying capacity**')

st.write('<style>h1{color: red;}</style>', unsafe_allow_html=True)
st.write('<style>h3{color: green;}</style>', unsafe_allow_html=True)

#st.write("### For any comment or furthermore assistance contact: tgwakjira@gmail.com [Tadesse G. Wakjira](https://scholar.google.com/citations?user=Ka3iXSoAAAAJ)")
# st.write("### For any comments, please contact tgwakjira@gmail.com")
