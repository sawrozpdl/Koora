# Koora

## College project

## Live site of Koora's `master` branch is hosted [here](http://kooora.herokuapp.com "Koora App Heroku")

#### Group Info

### Group Name : Dali's

### Group Members : 

- Dipesh Lama
- Neha Modi
- Prasesh Maharjan
- Saroj Paudyal


## Project Deployment

>Set/Export variables in `.env.example` and build the `Dockerfile` with

>>docker build .


## Project Development Setup

>Copy .env.example as .env and setup the required variables (besides the database variables) And,

**For Docker Users ,**

>`docker-compose up`

**For Non Docker Users :**

>`virtualenv .`

>>`source bin/activate` (Linux)

>>**OR**
 
>>`source Scripts/activate` (Windows @ GitBash)
 
>`pip install -r requirements.txt`

>`export $(cat .env)`

>`cd src`

>`python manage.py runserver 0.0.0.0:$APP_PORT`



## Detailed Description

    Aiming to create the platform where one can get various answers to their
    different questions online, we decided of creating a web application. Regarding the
    current scenario, Internet is used by almost 58% of the people worldwide, where they
    use Internet for the various purposes like social networking, online shopping, learning
    new things and so on. So, this platform for the Internet users will work as a guide. Our
    web application is named as “KOORA”. The name itself describes its purpose. It is the
    place where people ask questions and get answers from complete strangers, which can
    lead it to be called as the hub of information and source. It will also empower people to
    share their knowledge worldwide. It is quite simple to use, users just have to create their
    profile and get started.


**Features:**

- Users can create their own profile. They can also select the topics during
registration which they want the most in their feed.
- Users can ask questions and provide answers to other questions.
- Users can purchase premium plan which provides features like anonymous
posting, downloading the attachments.
- Users can up-vote or down-vote on a post (More up-votes more karma – kind of
like good deeds ;references: Reddit)
- Users can put their profile picture, description
- Users can changed their forgotten passwords as well
- Users are given CRUD functionality on their posts (kooras)
- The app provides Multi-threaded comments support (comment on a comment
and so on)
- The app will also provide the usability of sharing questions/answers to their
friends/relatives on sites like Facebook and Twitter.
