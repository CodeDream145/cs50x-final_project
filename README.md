# For Future Me
#### Video Demo:  
#### Description:

- __Base Concept(Non-Technical)__:-


    - Well, first of all, this site is built to create a new productive system or develop an existing productive system. I call it 
    as five-day-a-week system. Starting from Monday, which is the 0th day, to Sunday, which is the nul day. And on every numeric day 
    from the 0th day to the 5th day, stay focused. Focus on the things you need to do, including your personal development. At the 
    nul day, don't even think about your work and enjoy as much as you can. This is the key concept of this site.
    
    - Okay, we looked up the bigger picture, and it's time to extract it. As every numeric day was a working day, if you had no idea 
    how to do something or were stuck with confusion about what to do first, then you really needed to plan your goal before. The 
    *"Eat"* menu will help you do exactly this. Think of your work or goal as a dish. Store your daily dishes for eating. If the 
    dish is stored and not eaten, it will spoil. You can't eat a three-day-old dish on the fourth day. So try to eat the dish on the 
    day it is prepared. So create a dish (your goals) and its description (what actually to do or how to do it) inside the eat menu, 
    and eat it when it is done.
    
    - Have you eaten all your dishes prepared on that day and come to the end of the day? Now it's time to slice it up. Just go to 
    the "*Slice*" menu and click on the current day you are on, just to slice it up. Hey, don't worry if you have not eaten your 
    dishes for some unexpected reason; it may happen sometimes. But if your heart was fully satisfied or, in some cases, accepted 
    the reason for not eating the goals, then please don't forget to slice the day up. Even If you took a break that day 
    intentionally, just slice it up. Because you are under your control, you decided to take a break. And a kind recommendation: 
    Just before slicing, I always used to record the highlighted points from every day in a physical journal. It works great for me 
    to use those points or events to fine-tune my future days. So I recommend you try this out.
    
    - After slicing, don't simply end the day. Try to hear some really good stuff. That may be for your personal development or 
    about the thing you are learning or doing. The thing you heard before going to sleep will drive into your subconscious mind, and 
    you may come up with a new idea extracted from the words of the proven personalities. So before you go to sleep, hear something 
    good that is relevant to you. Try to avoid videos. Hear something in audio format. I will post what I hear regularly inside the 
    *"Hear"* menu. That will help you out.
    
    - At last, everything should be recorded to improve. A school without an attendance record will not be a school; it will be a 
    park where anyone can come at any time or day. So this site will store all your records, just to improve you. If you doubt your 
    process or get stuck at some point, just go to the "Dashboard" menu and see where you came from and how far you've come. 


- __Code Concept (Technical)__:-


    - This site is basically built on the flask and Bootstrap framework with basic HTML, CSS, and a few Javascripts.


    - *"app.py"*: It contains all the app routes, and every app route contains @login_required imported inside "helpers.py". Inside, 
    every route had its own separate function. And if the route had only one method(methods=["GET"]), then it may just render the 
    required HTML template. Else if the route had two methods(methods=["GET", "POST"]), after rendering the HTML template, it may 
    get some inputs from the Forms inside it and again render the HTML template accordingly.


    - *"helpers.py"*: It just contains two functions: apology (which renders apology.html with an error message in case some funny 
    hakish thing happens). and login_required (for confirming that the user was logged in by checking the flask session, and if not, 
    redirecting the user to the login page).

    - *"static"*: All static files like images, css, and javascript files were stored. styles.css contains all the CSS and the 
    jscript.js contains the javascript used in this website.


    - *"templates"*: All the templates used throughout this website were implemented here as a.html file. Used Templates: apology.
    html, dashboard.html, eat.html, hear.html, hearing.html, home.html, layout.html, login.html, register.html, slice.html. Every 
    template was designed except hearing.html, which was extended by layout.html. hearing.html was just the section extended inside 
    the hear.html. And every .html file was designed with the help of Bootstrap as a framework.
    
    - *"liftup.db"*: It is a sqlite3 basic database used to store every piece of data throughout this website.


    - These are the major files and folders used in this site. Remaining folders such as "flask_session" (used to store the session 
    values), "notes.txt" (just to take random notes during the creation of this site), and "requirements.txt" (created for the 
    purpose of deploying this website) are minor files that help this site slightly.

    
- __Design Theme__:-

    - "* Dark themed *": I used to create light-themed home pages for my prior project in Cs50x, so this time I tried a dark theme, 
    which came out pretty nice. I hope so.

    - "* Basic fonts *": I didn't try too many fonts; just three font families with varying sizes were used throughout this website.