# Story-Teller
# Hackathon project for HackDuke 2018

## Inspiration
In a time when students get distracted by their mobile phones, and have started neglected reading books, it is of utmost importance that we reintroduce the magic of books to young children. Accustomed to having visual feedback instantly, many young children find reading texts difficult, as they often find it mundane.

## What it does
The application basically uses Deep Learning tools for Computer Vision and Natural Language Processing to provide contextual images for each paragraph in a book. It tries to ensure that while reading a book, children get some kind of visual feedback, that could help nurture their imagination as well as make the hobby of reading interesting again.

***1. User proceeds through the book paragraph by paragraph.***

***2. Each sentence in a paragraph has associated images, if they are crucial for reference.***

***3. User proceeds to next paragraph using the Next button.***

## How I built it
- The back-end was built using **Python** and the REST API were written using **Flask**.
- **Google Cloud Platform Natural Language API** was used to identify the key words in each sentence of the text.
- **Google Custom Search API** was used to search images based on the key words that were extracted from the text, guided by the domain of the book.
- **Google Cloud Platform Cloud Vision API** was used to obtain image characteristics like **web tags and color information from images**.
- **Web Page** was developed using **HTML5, CSS3, jQuery and Bootstrap.**

## Challenges I ran into
1. **Fixing the errors inherent in Natural Language Processing**. A lot of time was spent just to make sure the correct keywords were identified, but like any other **Neural Network Algorithm**, it **can never be perfect**.
2. **Reducing the amount of time it takes to search for images** using the API was a big task. I minimized the number of API calls on the backend to a **balance between latency and accuracy.**
3. Handling asynchronous and synchronous calls to the REST API I developed was really difficult. Many **issues on the front end rose out of managing these calls to backend API**.

## Accomplishments that I am proud of
2. I was able to **integrate 3 different Google Cloud Platform API's** together to make the app work!
3. I was able to get **fairly decent results when it comes to fetching relevant images from the text**.
4. This was the **first time** I have used **Google Cloud Platform** to **develop an app**!

## What I learned
1. This is the first time I used **Flask**, so **Beginner Badge** earned over 24 hours!
2. How to build **Machine Learning driven Web Apps**.
3. How to setup **Google Custom Search Engine for my own apps!**.

## What's next for Story Teller
1. Improve the performance of my **Natural Language logic**.
2. Include **support for other books!**
3. Redesign the UI using some intuitive Front-End framework like **Angular or React.**
4. Improve the **Image Search logic** to **fetch better suited images related to the text**.

## Gallery

***Paragraph 1 of Harry Potter and The Sorcerer's Stone Chapter 1***
![Paragraph 1](docs/Para1.png)

***Paragraph 2 of Harry Potter and The Sorcerer's Stone Chapter 1***
![Paragraph 2](docs/Para1.png)

***About Page***
![About](docs/About.png)
