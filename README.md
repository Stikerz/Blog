# FS TDC Developer Assessment**


## Scenario   Background:
 
#### W. Pressford is a partner at Pressford Consulting.He would like to create a system to which he can publish news for all the employees to view.The system should do the following services:


- There should be a simple menu bar which allows you to navigate across the site, along with some dummy pages with placeholder text.
- A publisher should be able to publish news articles. The article should have a title, body, publish date, and any other fields you think would be valid e.g. author.
- A publisher should have the ability to edit and remove an article.
- An employee should be able to see a list of news articles, and read each article.
- Employees should have the ability to “like” an article. Ideally each user has a limited amount of “likes” they can provide.
- It should be possible to identify which article has the most likes.
- A user can log on and identify themselves, as an employee or publisher. (You do not have to implement password storage as this is just a demonstration to the client).
- Ideally he would be able to see some type of graphic. E.g. the number of likes plotted against each article on a chart.
- If time allows, Mr. Pressford would really like employees to have the ability to comment on each article.

## Setup:

- Create virtualenv(Optional) using python 3.6
- Run pip install -r requirements.txt
- Run python manage.py makemigrations
- Run python manage.py migrate
- Run python manage.py runserver # Now go to localhost:8000
   
## Testing
- Run python manage.py test accounts.tests # Run accounts test
- Run python manage.py test articles.tests # Run articles test
- Run python manage.py test comments.tests # Run comments test
