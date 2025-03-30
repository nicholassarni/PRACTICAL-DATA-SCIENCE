>>> from tinytroupe.agent import TinyPerson
>>> nick = TinyPerson("Nick")
>>> nick.define("age", 22)
>>> nick.define("nationality", "American")
>>> nick.define("occupation", "He is a Bookkeeper at a Property Management Company and a part time Data Science Masters student.")
>>> nick.listen_and_act("Tell me about yourself")
USER --> Nick: [CONVERSATION] 
          > Tell me about yourself
Nick acts: [THINK] 
          > I need to introduce myself. I should mention my name, age, occupation, and maybe a bit
          > about my studies.
Nick acts: [TALK] 
          > Sure! My name is Nick, I'm 22 years old, and I'm currently working as a bookkeeper at a
          > property management company. I'm also a part-time master's student in data science. I
          > enjoy learning new things and I'm excited about my studies!
Nick acts: [DONE] 

>>> scarlett = TinyPerson("Scarlett")
>>> scarlett.define("age", 22)
>>> scarlett.define("nationality", "Chinese")
>>> scarlett.define("occupation", "She is an aspiring video editor who just finished her studies at NYU with a major in film and animation.")
>>> from tinytroupe.environment import TinyWorld
>>> world = TinyWorld("Classroom", [yiqiao, john])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'yiqiao' is not defined
>>> world = TinyWorld("Classroom", [scarlett, nick])
>>> world.make_everyone_accesible()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'TinyWorld' object has no attribute 'make_everyone_accesible'. Did you mean: 'make_everyone_accessible'?
>>> world.make_everyone_accessible()
>>> nick.listen("What kind of things did you study?")
USER --> Nick: [CONVERSATION] 
          > What kind of things did you study?
TinyPerson(name='Nick')
>>> world.run(3) # trigger the conversation with 3 rounds back-and-forth
───────────────────────────────────────────── Classroom step 1 of 3 ─────────────────────────────────────────────
Scarlett acts: [DONE] 

Nick acts: [THINK] 
          > I should explain what I've been studying in my data science master's program. I can
          > mention the subjects I've covered and what interests me about them.
Nick acts: [TALK] 
          > In my data science master's program, I've been studying various subjects like
          > statistics, machine learning, and data visualization. I'm particularly interested in how
          > data can be used to make informed decisions and solve real-world problems.
Nick acts: [DONE] 

Nick --> Scarlett: [CONVERSATION] 
          > Sure! My name is Nick, I'm 22 years old, and I'm currently working as a bookkeeper at a
          > property management company. I'm also a part-time master's student in data science. I
          > enjoy learning new things and I'm excited about my studies!
Nick --> Scarlett: [CONVERSATION] 
          > In my data science master's program, I've been studying various subjects like
          > statistics, machine learning, and data visualization. I'm particularly interested in how
          > data can be used to make informed decisions and solve real-world problems.
───────────────────────────────────────────── Classroom step 2 of 3 ─────────────────────────────────────────────
Scarlett acts: [DONE] 

Nick acts: [DONE] 

───────────────────────────────────────────── Classroom step 3 of 3 ─────────────────────────────────────────────
Scarlett acts: [DONE] 

Nick acts: [DONE] 

>>> nick.listen("I want to get a new job")
USER --> Nick: [CONVERSATION] 
          > I want to get a new job
TinyPerson(name='Nick')
>>> world.run(3)
────────────────────────────────────────────────────────────────────────────────────────────────── Classroom step 1 of 3 ───────────────────────────────────────────────────────────────────────────────────────────────────
Scarlett acts: [DONE] 

Nick acts: [THINK] 
          > I should respond to the person's statement about wanting a new job. I can ask them what
          > kind of job they are looking for and if they need any advice or help with their job
          > search.
Nick acts: [TALK] 
          > That's great! What kind of job are you looking for? Do you need any help with your job
          > search?
Nick acts: [DONE] 

Nick --> Scarlett: [CONVERSATION] 
          > That's great! What kind of job are you looking for? Do you need any help with your job
          > search?
────────────────────────────────────────────────────────────────────────────────────────────────── Classroom step 2 of 3 ───────────────────────────────────────────────────────────────────────────────────────────────────
Scarlett acts: [TALK] 
              > Thank you for offering to help! I'm looking for a job that allows me to use my
              > skills in data analysis and visualization. Ideally, something that involves working
              > with real-world data to solve problems. Do you have any suggestions or know of any
              > openings?
Scarlett acts: [DONE] 

Scarlett --> Nick: [CONVERSATION] 
              > Thank you for offering to help! I'm looking for a job that allows me to use my
              > skills in data analysis and visualization. Ideally, something that involves working
              > with real-world data to solve problems. Do you have any suggestions or know of any
              > openings?
Nick acts: [THINK] 
          > Scarlett is looking for a job in data analysis and visualization. I should think about
          > any job openings I know of or suggest ways she can find opportunities in that field.
Nick acts: [TALK] 
          > I understand what you're looking for, Scarlett. You might want to check job boards like
          > LinkedIn or Indeed for openings in data analysis. Networking can also be really helpful,
          > so consider reaching out to professionals in your field. If you want, I can help you
          > refine your resume or cover letter!
Nick acts: [DONE] 

Nick --> Scarlett: [CONVERSATION] 
          > I understand what you're looking for, Scarlett. You might want to check job boards like
          > LinkedIn or Indeed for openings in data analysis. Networking can also be really helpful,
          > so consider reaching out to professionals in your field. If you want, I can help you
          > refine your resume or cover letter!
────────────────────────────────────────────────────────────────────────────────────────────────── Classroom step 3 of 3 ───────────────────────────────────────────────────────────────────────────────────────────────────
Scarlett acts: [TALK] 
              > Thank you for the suggestions, Nick! I appreciate your offer to help with my resume
              > or cover letter. I think refining those would be really beneficial. Could we set up
              > a time to work on that together?
Scarlett acts: [DONE] 

Scarlett --> Nick: [CONVERSATION] 
              > Thank you for the suggestions, Nick! I appreciate your offer to help with my resume
              > or cover letter. I think refining those would be really beneficial. Could we set up
              > a time to work on that together?
Nick acts: [THINK] 
          > Scarlett wants to set up a time to work on her resume and cover letter. I should suggest
          > a few times that work for me and ask her what her availability is like.
Nick acts: [TALK] 
          > Sure, Scarlett! How about we set up a time this weekend? I’m available Saturday
          > afternoon or Sunday morning. What works best for you?
Nick acts: [DONE] 

Nick --> Scarlett: [CONVERSATION] 
          > Sure, Scarlett! How about we set up a time this weekend? I’m available Saturday
          > afternoon or Sunday morning. What works best for you?
>>>
>>>


# 1. In order to install the tiny troupe package, you must first open a codespace on github. Once open, find the tiny troupe github link and clone the repository into the codespace. After cloning, enter the tinytroupe folder through your codespace and install the package through the “pip install .” command. Once the packages are installed, find your OpenAi API key and export it directly into your console. You can then enter python and import the many different packages that tinytroupe has to offer.

# 2. The Turing Test is a test developed by Alan Turing in order to determine if a human could be able to tell the difference between a machine and a human when conversing with them. However, because LLMs have become really good at mimicking human speak and natural language because of the large amount of data available, the Turing Test has become defined based on other ideas such as factors like long term consistency, understanding context beyond text, intentionality of the speaker, etc.

# 3. Based on this conversation, I believe that this conversation would not pass the Turing test for multiple reasons. For one, the conversation itself feels too overly formal considering they're both pretty young and would not speak to each other in such a professional way. Furthermore. the back and forth of them saying thank you makes them seem less human as no one would be this overly polite during a conversation.
