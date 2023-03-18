import streamlit as st
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re
import matplotlib.pyplot as plt

st.title('Phishing Website Detection using Machine Learning')
st.write('Objective of the app is detecting phishing websites only using content data. Not URL!')
st.write('\n')
st.write('This ML-based app is developed by - **Group No. 44**')
st.write('**(1) Mihir Pankhawala.    S19111050**')
st.write('**(2) Yohan Koshy.         S19111051**')
st.write('**(3) Junaid Minsiff.      S19111040**')
st.write('**(4) Prathamesh Neje.     S19111061**')

with st.expander("PROJECT DETAILS"):
     st.subheader('Approach')

     st.subheader('Data set')

     st.write('We used _"phishtank.org"_ & _"tranco-list.eu"_ as data sources.')
     st.write('Totally 26584 websites ==> **_16060_ legitimate** websites | **_10524_ phishing** websites')
     st.write('Data set was created in October 2022.')


     # ----- FOR THE PIE CHART ----- #
     labels = 'phishing', 'legitimate'
     phishing_rate = int(ml.phishing_df.shape[0] / (ml.phishing_df.shape[0] + ml.legitimate_df.shape[0]) * 100)
     legitimate_rate = 100 - phishing_rate
     sizes = [phishing_rate, legitimate_rate]
     explode = (0.1, 0)
     fig, ax = plt.subplots()
     ax.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=90, autopct='%1.1f%%')
     ax.axis('equal')
     st.pyplot(fig)
     # ----- !!!!! ----- #

     st.write('Features + URL + Label ==> Dataframe')
     st.markdown('label is 1 for phishing, 0 for legitimate')
     number = st.slider("Select row number to display", 0, 100)
     st.dataframe(ml.legitimate_df.head(number))


     @st.cache_data
     def convert_df(df):
          # IMPORTANT: Cache the conversion to prevent computation on every rerun
          return df.to_csv().encode('utf-8')


     csv = convert_df(ml.df)

     st.download_button(
          label="Download data as CSV",
          data=csv,
          file_name='phishing_legitimate_structured_data.csv',
          mime='text/csv',
     )


     st.subheader('Features')
     st.write('We used only content-based features. We didn\'t use url-based features like length of url etc.')

     st.subheader('Results')
     st.write('We used 7 different ML classifiers of scikit-learn and tested them implementing k-fold cross validation.'
              'Firstly obtained their confusion matrices, then calculated their accuracy, precision and recall scores.'
              'Comparison table is below:')
     st.table(ml.df_results)
     st.write('NB --> Gaussian Naive Bayes')
     st.write('SVM --> Support Vector Machine')
     st.write('DT --> Decision Tree')
     st.write('RF --> Random Forest')
     st.write('AB --> AdaBoost')
     st.write('NN --> Neural Network')
     st.write('KN --> K-Neighbours')

choice = st.selectbox("Please select your machine learning model",
                 [
                    'Gaussian Naive Bayes',
                    'Support Vector Machine',
                    'Decision Tree',
                    'Random Forest',
                    'AdaBoost',
                    'Neural Network',
                    'K-Neighbours'
                 ]
                )
model = ml.nb_model

if choice == 'Gaussian Naive Bayes':
    model = ml.nb_model
    st.write('GNB model is selected!')
elif choice == 'Support Vector Machine':
    model = ml.svm_model
    st.write('SVM model is selected!')
elif choice == 'Decision Tree':
    model = ml.dt_model
    st.write('DT model is selected!')
elif choice == 'Random Forest':
    model = ml.rf_model
    st.write('RF model is selected!')
elif choice == 'AdaBoost':
    model = ml.ab_model
    st.write('AB model is selected!')
elif choice == 'Neural Network':
    model = ml.nn_model
    st.write('NN model is selected!')
else:
    model = ml.kn_model
    st.write('KN model is selected!')


url = st.text_input('Enter the URL')
# check the url is valid or not
if st.button('Check!'):
    try:
        response = re.get(url, verify=False, timeout=40)
        if response.status_code != 200:
            print(". HTTP connection was not successful for the URL: ", url)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            vector = [fe.create_vector(soup)]  # it should be 2d array, so added []
            result = model.predict(vector)
            if result[0] == 0:
                st.success("This web page seems a legitimate!")
                st.balloons()

            else:
                st.warning("Attention! This web page is a potential PHISHING!")
                st.snow()

    except re.exceptions.RequestException as e:
        print("--> ", e)

with st.expander('EXAMPLE PHISHING URLs:'):
     st.write('_http://bitly.ws/utqB_')
     st.caption('PHISHING WEB PAGES HAVE SHORT LIFECYCLE!')

