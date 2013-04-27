ScenGen:
=======
>It's just python, but who doesn't love markdown.  

Hello comrades. This is a tool I made to generate potentially massive seeds in the smallest possible amount of time. With a bit of preliminary guidance, scenarios can be created up to ***one millon*** seeds per model.   

While even loading something like that in a test would take an eternity, it's just an idea. This readme included, this script has roughly 7-8 total hours of direct, and an additional 4 'dickaround' hours of work into it. What that means is that this likely has bugs, but hey it's the price I pay to entertain myself.   

Anyways, to the meat:  

###Installing / Running the generator  
    
1-  Pull the repository down to some directory.   

2-  Make a copy of the Rails project's schema.rb (db/schema.rb), place that in the directory.  

3-  Go to said directory in bash  

4-  type `python scengen.py <path to your schema.rb file>`

5-  You will be encountered by something like `Allow model <your model>?`  

6-  If you say `no`, it will just move to the next model, but if you say `yes`

7-  Script will say `Got <your model>, what's the model name?`. What this wants is the singular model name. So if it's saying it got a model named `people`, it wants `Person`. Case is *very* important here.   

7a- The script cares about your time, so it remembers how you input model names.

8-  Once the model name is provided, you begin to go through the attributes of that model. Use your discretion to choose the best generator to fill that field. For example, I'm met with: 
```
Generator for Person.first_name:string?
```  
We're being shown here that first name is of a type string, which should give you an idea of the acceptable **generators**(_see below_) to use. While the generator is fairly good at rendering types appropriately, it doesn't take being disrespected well. So here, I'd look at my generators and decide that
```
firstname
```  
was the best generator. If the generator is typed correctly the script will save that choice to file so that in the future, it will automatically fill this.  

9-  Go through all of your models you care to write (**Careful:Look at Foreign Keys below**) to the scenario  

10-  At the end, you are asked  
```
How many instances of each model do we want??
```  
At which time you tell the script how many of each model to write. So with 5 models and 10 instances, we have a file with 50 total scenario fixtures.  


Native Commands(Generators): 
-------------------------------
*Viewed by typing `??n`*

---------------------


###skip ###
*skip setting a value for the specific attribute, just this one time*  
ie. 
```
skip
```
OUTPUT[will be nothing.]   


###block ###
*skip setting a value for the specific attribute, and never bring it up again.*  
ie. 
```
block
```
OUTPUT[would be nothing...]

###c ###
*shorthand for 'crap', renders a string of 10 random a-z chars *  
**See below for result**

###crap ###
*renders a string of 10 random a-z chars *  
ie. 
```
crap
```
OUTPUT[could be]   
`oxuwlduizs`

- - -

###crap:(length)###
*renders a string of n random a-z chars*  
ie. 
```
crap:4
```
OUTPUT[could be]   
`nusq`

-  -  -

###char:(start)-(end)###
*renders a character within a specific range (start must have an ascii index lower than end. eg A-z works, a-Z doesn't.*  
ie. 
```
char:A-b
```
OUTPUT[could be]   
`K`

-  -  -

###char:(range):(count)###
*renders a collection of characters of a specific range*  
ie. 
```
char:A-z:5 
```
*would render 5 characters ranging from A to z next to eachother*  
OUTPUT[could be]   
`ArCHf`

-  -  -

###coll:{item1,...,itemn}###
*picks a random entry from a collection of static possibilities*  
ie.   

```
coll:{Duck,Duck,Goose!}
```  
  
OUTPUT[could be]   
`Goose!`

- - -

###coll!:{gen1,...,gen2}###
*picks a random entry from a collection of generators*  
ie. 
```
coll!:{lit:0,num:1-9:3,mycustomnum>}  
  
```
OUTPUT[could be]   
`224`

- - -


###lit:<literal string>###
*renders n literally*  
ie. 
```
lit:Pancakes
```
OUTPUT[WILL be]   
`Pancakes`

- - -

###dec ###
*renders a four digit decimal xx.xx*  
ie. 
```
dec
```
OUTPUT[could be]   
`23.44`

- - - 

###email###
*renders an email in the format firstname*  
ie. 
```
email
```
OUTPUT[could be]   
`JohnSmith@bldsa.com`

- - -

###zip ###
*Renders a 5 digit zip code*  
ie. 
```
zip
```
OUTPUT[could be]   
`98133`

- - - 

###address###
*Renders a simple address*   
ie. 
```
address
```
OUTPUT[could be]   
`67 N 187th ST`

- - - 

###fk - See Foreign Keys###
*but look here for some other stuff*  
Usage:
Lets say that in the model Shoes, that we have a foreign key causing them to belong to a person. Lets say that we'd like each person to have 2 shoes. We'd this when prompted for shoes*person_id:  

```
fk:people:2
```  
  
This establishes a 2-1 generation pattern between shoes and people. Simply putting  
  
```
fk:people
```  
  
Implies a 1-1 generation pattern, where a single shoe is owned by each person.  

####Has One Relations  
Lets say that a Person also has an address, but that address is made for the sole purpose of their existence. Putting  
  
```
fk:addresses:0
```  
  
Will create an address exclusively for that person, regardless of if there are enough iterations to do so. 


- - - 

###ip###
*renders a typical IP address*  
ie. 
```
ip
```
OUTPUT[could be]   
`192.111.231.32`

- - -

###operator###
*renders a logical operator*  
ie. 
```
operator
```
OUTPUT[could be]   
`>=`

- - -

###fullname###
*renders a first and last name*  
ie. 
```
fullname
```
OUTPUT[could be]   
`John Smith`

- - -

###file:.(extension)###
*renders a filename by having the right side determine the file type*  
ie. 
```
file:.exe
```
renders garbage text with a .exe extension
OUTPUT[could be]   
`giwnusdanw.exe`

- - -
    
###date###
*renders a date in yyyy-mm-dd*  
ie. 
```
date
```
OUTPUT[could be]   
`2012-03-04`

-  -  -

###datetime###
*renders a timestamp.*  
ie. 
```
datetime
```
OUTPUT[could be]   
`2012-03-04 12:34:22.45`

-  -  -

###num###
*renders a number from 0 to 50000*  
ie. 
```
num
```
OUTPUT[could be]   
`34342`

-  -  -

###num:(min)-(max)###
*renders a number within a specific range*  
ie. 
```
num:300-6000
```
OUTPUT[could be]   
`5342`

-  -  -

###num:(range):(count)###
*renders a collection of numbers of a specific range*  
ie. 
```
num:0-2:5 
```
*would render 5 numbers ranging from 0 to 2 next to eachother*  
OUTPUT[could be]   
`01201`

-  -  -

###iter###

*renders a number from 0 to the number of iterations*
ie 
```
iter 
```
(while running with 30 iterations/model)
OUTPUT[could be]   
`14`  

-  -  -

###fields:(model)###

*renders a random field from the association of the model*
ie 
```
fields:User 
```

OUTPUT[could be]   
`user_email`  

-  -  -

###models###

*renders a random model name from the association of the model*
ie 
```
models
```

OUTPUT[could be]   
`Users`


User Added Collection Commands:
===============================
*Viewed by typing `??a`*

--------------------------------------------------- 

in a directory in the same place as the python file (DATA_PATH, defaulting to groups/),
7 native files are kept, there are two purposes of these, and by purpose these are:

##Static data##

- - - 

- ***city.wtf*** : a list of city names
- ***state.wtf*** : a list of states
- ***firstname.wtf*** : a list of first names
- ***lastname.wtf*** : a list of last names

These provide a basic start for some common stuff. To reference a collection, just use the name of the file, minus the extension. The native *firstname*, *lastname*, *state*, and *city* derive from these.
  
  So lets say there are a list of statuses that you want to be using randomly. So you make a file called status.wtf (if .wtf is your extension) with one possibility per line. Then, to use that, you'd type 'status'. If it throws a 'command not recognized' error, then it was either not loaded, or you typed it wrong. To double check, type ??a to make sure the command is on the added collection list.

##Native Dynamic data##

- - - 

- ***custom.wtf*** : a list of custom tags (See below)
- ***remember.wtf*** : a list of remembered render options for specific model attributes, stored automatically. 
- ***deny.wtf*** : a list of model attributes that are blocked.

These are as-is, and may be modified while the program is not running to change defaults. If you want to completely redefine how
to render attributes, simple delete the remember file and re-choose. Same goes with the deny and custom files, but why would you want to delete customs!?



Custom Commands: 
================================
*Viewed by typing `??c`*

----------------------------------------------------
Custom commands can be created and referenced across usages, namely every time a custom command, it is saved and can just be referenced by it's name later instead of typing it all out again. 
A custom command would look like so:
```
mycommand>"Entry "+iter+" section "+num:0-50
```
so we're pretty much concatenating the existing commands in with strings.

Two things NOT to do here though
  
1.  **Don't use a custom inside a custom**

2.  **Don't just use a command, it NEEDS to have open and closed strings.** If you just wanted to render a tag, like `num:0-50`, then you'd have to put `""+num:0-50`.

BUT As i said, it stores custom strings to use them later. So with the above example, when we wanted to use it again, we'd just type `mycommand>` . if there is anything after the `>`, it will overwrite the value. 

To type a custom without saving it, just dont give it a name.
ie. 
```
>"I dont care about saving this "+firstname
```




Foreign Keys (fk:) and not breaking stuff.
----------------------------------------------------

*A note about foreign keys, and model names in general.*

When asked, "what's the model name?", the program is expecting the name to mimic that of the model name. 

What I mean is that for a model 'Person', it isn't 'person', 'People', or 'people'. It's 'Person'... 
When typing an association, the singular name of said table is expected, so if an attribute is a foreign key to the model User, we'd put `fk:user` or `fk:User` . NOT `fk:users` or any other plural derivation.

Last thing. The program will output the scenario in a way that puts dependent models below their dependencies. The algorithm that does this requires that all models being referred to be included in the output. So if you just want to output a model Person, but in that Person there is an fk: reference to User (fk:user), if you don't agree to include that user, the script will flip shit, and likely not output what you wanted. 

Because of this, it may be prudent to, in scenarios with large amounts of association, to just output all models. 

(PS): Attempting to set certain attributes (updated_at, deleted_at, to name a few), is not allowed via. scenarios, and will throw an "attribute not mass-assignable" or something silly like that. Add such things to the block list. 
