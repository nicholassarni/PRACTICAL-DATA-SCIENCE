#REPORT 

What is a class object:

A class object is a object created from a class of functions within python. Specifically when referencing our code we see that we defined a class object "URLValidator" or whichever name you decide to give your object, that the object consists of multiple different functions that take the object we are processing (in this case an input statement comparing our prompt with the url for the article we are evaluating) and in tandem creates an output based on how the functions operate on the object.

What is a docstring:

A docstring is a documentation string that explains what the code does and what the different functions do without having the code processing it has being apart of the class/functions. We place these docstrings inside the code so that users who have no familiarity with that the different parts of the code are doing can have a better understanding of what is going on.

How to define a init of a class object:

In order to define the init of a class object you would use the following syntax: 'def__init__(self):'

What is a method:

A method are the functions defined within the class that each processes and returns an output based on the object that was inputted. While technically we could write all of our functions within one method and process it like that, by seperating each part of the process into different methods we can not only utilize each one seperately if we wanted to (for example if we are interested in only evaluating our article against google scholar we could just call the check_google_scholar method in our code) overall it breaks down the process and makes sure that each part of the code is performing a specific job in a clear way to the programmer.

How do you let functions fail gracefully?

By using try and except statements, we can make it so that in the case where there is an error from what is inputted into the algorithim, rather than making it a larger issue for the user (for example if we had no way to make a function fail gracefully, the user could end up with the app crashing, a large jumble of code being outputted that they dont understand, or even a long wait time while the code continues to process the request that will never actually finish processing) it will instead just produce a statement letting the user/programmer know that the code failed (whether it be that the input could not be processed or it was taking too long)

What's a standard practice of a return statement?

The standard practice regarding a return statement is to have it consisely report all of the information processed by the methods of a class, usually as a json file which posseses general flexibility and ease of use when implementing into apps and in general when using APIs.