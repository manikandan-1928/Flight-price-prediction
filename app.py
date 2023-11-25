from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("Flight_tic_price_pred_83p90.pkl", "rb"))



@app.route("/")
@cross_origin()
def base():
    return render_template("home.html")




@app.route("/predict", methods = ["post"])
@cross_origin()
def predict():
    if request.method == "POST":  
        # Date_of_Journey
        date_dep = pd.to_datetime(request.form["Dep_date"])
        Journey_day = int(date_dep.day)
        Journey_month = int(date_dep.month)
        Journey_weekday = int(date_dep.weekday())

        time_dep = pd.to_datetime(request.form["Dep_Time"])
        Dep_hour = int(time_dep.hour)
        Dep_min = int(time_dep.minute)

        date_arr = pd.to_datetime(request.form["Arrival_date"])
        Arrival_hour = int(date_arr.hour)
        Arrival_min = int(date_arr.minute)
        
        # Total Stops
        Total_stops = int(request.form["stops"])
        if Total_stops == 'Non-Stop':
            Total_stops = 0
        # print(Total_stops)

        # Airline
        # AIR ASIA = 0 (not in column)
        airline=request.form['airline']
        if(airline=='Jet Airways') or (airline=='Jet Airways Business'):
            Jet_Airways = 1
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 0 

        elif (airline=='IndiGo'):
            Jet_Airways = 0
            IndiGo = 1
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 0 

        elif (airline=='Air India'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 1
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 0 

        elif (airline=='Multiple carriers') or (airline=='Multiple carriers Premium economy'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 1
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 0  
                
        elif (airline=='SpiceJet'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 1
            Vistara = 0
            GoAir = 0
            Trujet = 0  
                
        elif (airline=='Vistara') or (airline=='Vistara Premium economy'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 1
            GoAir = 0
            Trujet = 0 

        elif (airline=='GoAir'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 1
            Trujet = 0

        
        elif (airline=='Trujet'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 1

        else:
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 0 
                
            
        Source = request.form["Source"]
        if (Source == 'Delhi'):
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Kolkata'):
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Mumbai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0

        elif (Source == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        Source = request.form["Destination"]
        if (Source == 'Cochin'):
            d_Cochin = 1
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0
            
        elif (Source == 'Delhi'):
            d_Cochin = 0
            d_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0

            
        elif (Source == 'Hyderabad'):
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0

        elif (Source == 'Kolkata'):
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        else:
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0
    
            
        prediction=model.predict([[
                Total_stops,
                Journey_day,
                Journey_month,
                Journey_weekday,
                Dep_hour,
                Dep_min,
                Arrival_hour,
                Arrival_min,
                Air_India,
                GoAir,
                IndiGo,
                Jet_Airways,
                Multiple_carriers,
                SpiceJet,
                Trujet,
                Vistara,
                s_Chennai,
                s_Delhi,
                s_Kolkata,
                s_Mumbai,
                d_Cochin,
                d_Delhi,
                d_Hyderabad,
                d_Kolkata,
                ]])

        output=round(prediction[0],2)


        return render_template('home.html',prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("home.html")




if __name__ == "__main__":
    app.run(debug=True)