import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
#---------------------------------------------------
st.set_page_config(page_title="KP WEB APP", page_icon=":sunglasses:", layout="centered", initial_sidebar_state="expanded")
with st.sidebar:
    option = option_menu("KP MODEL", options=["AIR_QUALITY_WEB_APP"],
    icons=[":grinning:",":stuck_out_tongue_winking_eye:",":grinning:","kissing"], default_index=0)
#option = st.sidebar.radio("SELECT WHAT YOU WANT", options=["URL SHORTNER", "IMAGE EDITOR", "WORD DENSITY CHECKER", "AUDIO TO TEXT CONVERTER"],ic)
#------------------------------------------------------

#-------------------------------------------------------
if option=="AIR_QUALITY_WEB_APP":
    st.sidebar.markdown("-----------")
    st.sidebar.markdown(f"<h3 style='text-align: center;'>{option}</h3>",unsafe_allow_html=True)
    st.sidebar.markdown(f"<i>THIS IS AIR QUALITY MEASUREMENT WEB APP USED TO FIND AIR QUALITY(AQI) OF YOUR CITY WITH GRAPHICAL VISUALIZATION</i>",unsafe_allow_html=True)
    st.sidebar.markdown("-----------")
    st.sidebar.markdown(f"<h3 style='text-align: center;'>Instructions</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("1.Please download the data from the standard site of the government and the data downloaded should be in excel form only")
    st.sidebar.markdown("2.Please download the data in two separate excel sheets one sheet download data (CO, Ozone for 8 hours) and the other sheet should have minimum (PM2.5, PM10, SO2, NO2) for 24hour")
    st.sidebar.markdown("3.Do not edit data Please paste your data here as is")
    #-------------------------------------------
    st.markdown("<h1 style='text-align: center;'>AIR QUALITY MEASUREMENT WEB APP(KP MODEL)</h1>", unsafe_allow_html=True)
    st.markdown("----------------")
    st.markdown(f"<h6 style='text-align: center;'>First File(Which contain CO and Ozone data per annum)</h6>", unsafe_allow_html=True)
    audio_1 = st.file_uploader("Upload Your First File", type=["xlsx"])
    st.markdown("    ")
    st.markdown(f"<h6 style='text-align: center;'>Second File(Which contain PM2.5 and other pollutant per annum data)</h6>", unsafe_allow_html=True)
    audio_2 = st.file_uploader("Upload Your Second File", type=["xlsx"])
    st.markdown("   ")
    a=st.button(label="Click On It")
    #------------------------------------------------
    if audio_1 and audio_2:
        if a:
            data_2 = pd.read_excel(audio_2)
            data_1 = pd.read_excel(audio_1)
            data_1 = data_1.iloc[15:]
            data_1=data_1.set_axis(data_1.iloc[0], axis=1)
            data_1 = data_1.iloc[1:]
            data_1 = data_1.reset_index()
            data_1.drop(data_1.columns[[0]], axis=1, inplace=True)
            data_1['From Date'] = pd.to_datetime(data_1['From Date'],format='%d-%m-%Y %H:%M')
            data_1['To Date'] = pd.to_datetime(data_1['To Date'],format='%d-%m-%Y %H:%M')
            data_1['From Date'] = pd.to_datetime(data_1["From Date"]).dt.date
            data_1['To Date'] = pd.to_datetime(data_1["To Date"]).dt.date
            data_1.isnull().sum()
            data_1 = data_1.replace(['None'], 0)
            data_1.info()
            data_12=data_1.groupby(["From Date"]).mean()
            data_2=data_2.iloc[15:]
            data_2=data_2.set_axis(data_2.iloc[0], axis=1)
            data_2 = data_2.iloc[1:]
            data_2 = data_2.reset_index()
            data_2.drop(data_2.columns[[0]], axis=1, inplace=True)
            data_2["From Date"] = data_2["From Date"].dropna(axis = 0)
            data_2['From Date'] = pd.to_datetime(data_2['From Date'],format='%d-%m-%Y %H:%M')
            data_2['From Date'] = pd.to_datetime(data_2["From Date"]).dt.date
            data_2['To Date'] = pd.to_datetime(data_2['To Date'],format='%d-%m-%Y %H:%M')
            data_2['To Date'] = pd.to_datetime(data_2["To Date"]).dt.date
            data_2= data_2.replace(['None'], 0)
            data_21 = data_2[["From Date", "PM2.5", "PM10", "SO2", "NO2"]]
            data=pd.merge(data_21, data_12,on="From Date")
            data.fillna (0)
            data.isnull().sum()
            def calculate_index(PM25):
                pi=0
                if(PM25<=30):
                   pi=PM25*(50/30)
                elif(PM25>30 and PM25<=60):
                   pi=50+(PM25-30)*(50/30)
                elif(PM25>60 and PM25<=90):
                   pi=100+(PM25-60)*(100/30)
                elif(PM25>90 and PM25<=120):
                   pi=200+(PM25-90)*(100/30)
                elif(PM25>120 and PM25<=250):
                   pi=300+(PM25-120)*(100/130)
                else:
                   pi=400+(PM25-250)*(100/130)
                return pi
            data["PM25"] = data["PM2.5"].apply(calculate_index)
            def calculate_index_1(PM10):
                PI=0
                if(PM10<=50):
                   PI = PM10*(50/50)
                elif(PM10>50 and PM10<=100):
                   PI = 50+(PM10-50)*(50/50)
                elif(PM10>100 and PM10<=250):
                   PI = 100+(PM10-100)*(100/150)
                elif(PM10>250 and PM10<=350):
                   PI = 200+(PM10-250)*(100/100)
                elif(PM10>350 and PM10<=430):
                   PI = 300+(PM10-350)*(100/80)
                else:
                   PI = 400+(PM10-430)*(100/80)
                return PI
            data["Pm10"] = data["PM10"].apply(calculate_index_1)
            def calculate_index_2(CO):
                CI=0
                if(CO<=1):
                   CI= CO*50/1
                elif(CO>1 and CO<=2):
                   CI= 50+(CO-1)*(50/1)
                elif(CO>2 and CO<=10):
                   CI= 100+(CO-2)*(100/8)
                elif(CO>10 and CO<=17):
                   CI = 200+(CO-10)*(100/7)
                elif(CO>17 and CO<=34):
                   CI= 300+(CO-17)*(100/17)
                else:
                   CI= 400+(CO-34)*(100/17)
                return CI
            data["co10"] = data["CO"].apply(calculate_index_2)
            def calculate_index_3(SO2):
                si=0
                if (SO2<=40):
                   si= SO2*(50/40)
                if (SO2>40 and SO2<=80):
                   si= 50+(SO2-40)*(50/40)
                if (SO2>80 and SO2<=380):
                   si= 100+(SO2-80)*(100/300)
                if (SO2>380 and SO2<=800):
                   si= 200+(SO2-380)*(100/800)
                if (SO2>800 and SO2<=1600):
                   si= 300+(SO2-800)*(100/800)
                if (SO2>1600):
                   si= 400+(SO2-1600)*(100/800)
                return si
            data["so2"] = data["SO2"].apply(calculate_index_3)
            def calculate_index_4(NO2):
                ni=0
                if(NO2<=40):
                   ni= NO2*50/40
                elif(NO2>40 and NO2<=80):
                   ni= 50+(NO2-40)*(50/40)
                elif(NO2>80 and NO2<=180):
                   ni= 100+(NO2-80)*(100/100)
                elif(NO2>180 and NO2<=280):
                   ni= 200+(NO2-180)*(100/100)
                elif(NO2>280 and NO2<=400):
                   ni= 300+(NO2-280)*(100/120)
                else:
                   ni= 400+(NO2-400)*(100/120)
                return ni
            data["no2"] = data["NO2"].apply(calculate_index_4)
            def calculate_index_5(Ozone):
                OZ=0
                if(Ozone<=50):
                   OZ= Ozone*50/50
                elif(Ozone>50 and Ozone<=100):
                   OZ= 50+(Ozone-50)*(50/50)
                elif(Ozone>100 and Ozone<=168):
                   OZ= 100+(Ozone-100)*(100/68)
                elif(Ozone>169 and Ozone<=208):
                   OZ= 200+(Ozone-169)*(100/39)
                elif(Ozone>208 and Ozone<=748):
                   OZ= 300+(Ozone-208)*(100/540)
                else:
                   OZ= 400+(Ozone-748)*(100/540)
                return OZ
            data["ozone"] = data["Ozone"].apply(calculate_index_5)
            def max_value(a,b,c,d,e,f):
                fig = max(a,b,c,d,e,f)
                return fig
            data['AQI']=data.apply(lambda x: max_value(x['PM25'],x['Pm10'],x['co10'],x['so2'], x['no2'], x['ozone']),axis=1)
            def AQI_Range(x):
                if x<=50:
                    return "GOOD"
                elif x>50 and x<=100:
                    return "SATISFACTORY"
                elif x>100 and x<=200:
                    return "MODERATELY POLLUTED"
                elif x>200 and x<=300:
                    return "POOR"
                elif x>300 and x<=400:
                    return "VERY POOR"
                elif x>400:
                    return "HAZARDOUS"
            data["Quality"] = data["AQI"].apply(AQI_Range)
            data.rename(columns={'From Date':'Date'}, inplace=True)
            data_new = data[["Date", "AQI", "Quality"]]
            st.markdown("    ")
            st.markdown(f"<h6 style='text-align: center;'>AIR QUALITY OF YOUR CITY</h6>", unsafe_allow_html=True)
            st.dataframe(data_new, 800, 400)
            st.markdown("  ")
            #b = st.button(label="VISUALIZATION")
            st.markdown("  ")
            #sns.pairplot(data, hue = 'AQI')
            #plt.show()
            #----------------------------------------------1
            PLOT = go.Figure()
            for C in list(data.Quality.unique()):                    
                PLOT.add_trace(go.Scatter3d(x = data[data.Quality == C]['Pm10'],
                                            y = data[data.Quality == C]['AQI'],
                                            z = data[data.Quality == C]['Date'],
                                            mode = 'markers', marker_size = 8, marker_line_width = 1,
                                            name = 'Quality ' + str(C)))
            PLOT.update_layout(width = 1000, height = 600, autosize = True, showlegend = True,                    
                               scene = dict(xaxis=dict(title = 'PM10', titlefont_color = 'black'),
                                            yaxis=dict(title = 'AQI', titlefont_color = 'black'),
                                            zaxis=dict(title = 'Date', titlefont_color = 'black')),
                               font = dict(family = "Gilroy", color  = 'black', size = 12))
            st.plotly_chart(PLOT)
#---------------------------------------------------------------2
            PLOT = go.Figure()
            for C in list(data.Quality.unique()):                    
                PLOT.add_trace(go.Scatter3d(x = data[data.Quality == C]['co10'],
                                            y = data[data.Quality == C]['AQI'],
                                            z = data[data.Quality == C]['Date'],
                                            mode = 'markers', marker_size = 8, marker_line_width = 1,
                                            name = 'Quality ' + str(C)))
            PLOT.update_layout(width = 1000, height = 600, autosize = True, showlegend = True,                    
            scene = dict(xaxis=dict(title = 'CO', titlefont_color = 'black'),
                        yaxis=dict(title = 'AQI', titlefont_color = 'black'),
                        zaxis=dict(title = 'Date', titlefont_color = 'black')),
            font = dict(family = "Gilroy", color  = 'black', size = 12))
            st.plotly_chart(PLOT)
#------------------------------------------------------------------------------3
            PLOT = go.Figure()
            for C in list(data.Quality.unique()):                    
                PLOT.add_trace(go.Scatter3d(x = data[data.Quality == C]['so2'],
                                            y = data[data.Quality == C]['AQI'],
                                            z = data[data.Quality == C]['Date'],
                                            mode = 'markers', marker_size = 8, marker_line_width = 1,
                                            name = 'Quality ' + str(C)))
            PLOT.update_layout(width = 1000, height = 600, autosize = True, showlegend = True,                    
                               scene = dict(xaxis=dict(title = 'SO2', titlefont_color = 'black'),
                                           yaxis=dict(title = 'AQI', titlefont_color = 'black'),
                                           zaxis=dict(title = 'Date', titlefont_color = 'black')),
                               font = dict(family = "Gilroy", color  = 'black', size = 12))
            st.plotly_chart(PLOT)
#-------------------------------------------------------------------4
            PLOT = go.Figure()
            for C in list(data.Quality.unique()):                    
                PLOT.add_trace(go.Scatter3d(x = data[data.Quality == C]['no2'],
                                            y = data[data.Quality == C]['AQI'],
                                            z = data[data.Quality == C]['Date'],
                                            mode = 'markers', marker_size = 8, marker_line_width = 1,
                                            name = 'Quality ' + str(C)))
            PLOT.update_layout(width = 1000, height = 600, autosize = True, showlegend = True,
                               scene = dict(xaxis=dict(title = 'NO2', titlefont_color = 'black'),
                                            yaxis=dict(title = 'AQI', titlefont_color = 'black'),
                                            zaxis=dict(title = 'Date', titlefont_color = 'black')),
                               font = dict(family = "Gilroy", color  = 'black', size = 12))
            st.plotly_chart(PLOT)
#---------------------------------------------------------------------5
            PLOT = go.Figure()
            for C in list(data.Quality.unique()):
                PLOT.add_trace(go.Scatter3d(x = data[data.Quality == C]['ozone'],
                                            y = data[data.Quality == C]['AQI'],
                                            z = data[data.Quality == C]['Date'],
                                            mode = 'markers', marker_size = 8, marker_line_width = 1,
                                            name = 'Quality ' + str(C)))
            PLOT.update_layout(width = 1000, height = 600, autosize = True, showlegend = True,
                               scene = dict(xaxis=dict(title = 'Ozone', titlefont_color = 'black'),
                                            yaxis=dict(title = 'AQI', titlefont_color = 'black'),
                                            zaxis=dict(title = 'Date', titlefont_color = 'black')),
                               font = dict(family = "Gilroy", color  = 'black', size = 12))
            st.plotly_chart(PLOT)
#---------------------------------------------------------------------------------6
            PLOT = go.Figure()
            for C in list(data.Quality.unique()):
                PLOT.add_trace(go.Scatter3d(x = data[data.Quality == C]['PM25'],
                                            y = data[data.Quality == C]['AQI'],
                                                    z = data[data.Quality == C]['Date'],
                                            mode = 'markers', marker_size = 8, marker_line_width = 1,
                                            name = 'Quality ' + str(C)))
            PLOT.update_layout(width = 1000, height = 600, autosize = True, showlegend = True,
                               scene = dict(xaxis=dict(title = 'PM2.5', titlefont_color = 'black'),
                                            yaxis=dict(title = 'AQI', titlefont_color = 'black'),
                                            zaxis=dict(title = 'Date', titlefont_color = 'black')),
                               font = dict(family = "Gilroy", color  = 'black', size = 12))
            st.plotly_chart(PLOT)

            st.markdown("   ")
            #-------------------------------------------------------------------------
            fig = px.scatter(data_new, x="Date", y="AQI", color="Quality",
                             size='AQI', hover_data=['Quality'])
            st.plotly_chart(fig)
            fig = px.scatter(data, x="PM2.5", y="PM10", color='AQI')
            st.plotly_chart(fig)
            fig = px.line(data, x='Date', y="AQI", color='Quality')
            st.plotly_chart(fig)
            #---------------------------------------




    



