#Imports
from flask_restful import Resource, Api, reqparse
from logging.config import dictConfig
from flask import render_template
from app import app, api
from app.forms import SearchForm


#Configure logging (This can be copy pasted across apps, or configured as needed)
dictConfig({"version": 1,
            "disable_existing_loggers": False,
            "formatters": {"default": {
                        "format": '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                }},

            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                    }
                },

            "root": {"level": "DEBUG", "handlers": ["wsgi"]},
            })


# A function for sorting strings
# This could be replaced by any other function to achieve different things
# for example a machine learning algorithm
def sort_strings(strings):
    sorted_strings = []
    for string in strings:
        sorted_strings.append(str(sorted(string)))
    return zip(strings,sorted_strings)
    

#The decorator defines what url will be used to access this function
@app.route("/example_static", methods=['GET', 'POST'])
def static_page():
    #The render template function renders a template
    return render_template("example_static.html")


#Define route
@app.route("/", methods=['GET', 'POST'])
@app.route("/example_form", methods=['GET', 'POST'])
def example_form():
    #instantiating a SearchForm type (defined in forms.py)
    #Allows us to access the content submitted by a user
    form = SearchForm()

    if form.validate_on_submit():
        try:
            #Get the data from the form
            all_strings = str(form.input_string.data)
            #Process the data from the form
            all_strings = all_strings.split(",")
            #Remember if this was a production app you should sanitise your inputs
            # Process the input:
            results = sort_strings(all_strings)
            return render_template("example_form.html", form=form, results=results)

        except Exception as e:
            app.logger.debug(e)
            return render_template("example_form.html")
            
    #This part of the code gets called if the user hasn't just submitted the form
    # e.g. they are loading the page for the first time
    return render_template("example_form.html", form=form)


#Now for the API
#reqparse is used to parse (an sanitise) inputs
parser = reqparse.RequestParser()
parser.add_argument('strings')

#We can then define an API endpoint
class ApiEndpoint(Resource):
    #Different HTTP functions are defined within the resource
    def get(self):
        return {"Hello": "world"}

     
    def post(self):
        args = parser.parse_args()
        if "strings" not in args:
            return {"Error":"Failed to process input, check both metal and SMILES are provided."}    
        try:
            #Process the input
            if isinstance(args["strings"],str):
                strings = [args["strings"]]
            else:
                strings = args["strings"]            
            
            return list(sort_strings(strings))
        except Exception as e:
            app.logger.debug(e)
            return {"Error":"Failed to process input, check it is properly formatted."}

#You then add the resource to the API, and deffine the end point to be called        
api.add_resource(ApiEndpoint, "/API")
