# The Running Team

![readmehero](documentation/images/responsive_demo.PNG)
[Live website](https://the-running-team.herokuapp.com)


![readmehero](documentation/images/database_diagram.jpeg)
The Running Team is the digital home of a fictional running team. The website is meant to be a place where the team members can plan workouts, share knowledge through blog posts, and keep up to date with the events the team is participating in. However, the website can also be accessed by anyone who's not a member of the team, although in a very restricted view.

 
## UX

### General

The owner of the website(read: the team) recognizes the need for an online gathering point for the team. The website needs to enable the team members to plan out their workouts, share information via blog posts and keep up to date on events. While the owner first and foremost have self interest in the app, it's also important that it offers the general public access to keep updated on the team, while preserving key features of the site for the team members themselves.  


### Typography

The website uses two fonts from [Google Fonts'](https://fonts.google.com/) library called [Oswald](https://fonts.google.com/specimen/Oswald?query=oswald) and [Roboto](https://fonts.google.com/specimen/Roboto?query=roboto)

Oswald is used for all header type elements, while Roboto is used for paragraph type elements and large blocks of text. These fonts, especially Oswald, was chosen with two sources of inspiration: [Roboto](https://www.runnersworld.com)
![runnersworld](documentation/images/runnersworld.png)
the "Love Running" mini project at Code Institute. Roboto was chosen as it is pleasant to look at and easy to read. This is especially important in the "training blog" section of the website where the user is potentially exposed to large blocks of text. Roboto is also a popular pairing with Oswald and suggested by google fonts.  



 ### Colors
 The color theme of the website is very simplistic. All text is green, while backgrounds alternate between black and dark grey. Black and grey is very important to provide some variation against the green text. It also serves the purpose of separating the three main parts of the website.

 There are a few instances across the website where a tone of white is used. Most of these instances are for
 text that needs to stand out, like in the learn section and the alternating green/white "start game" button, but also on hover on links in the navbar.

 A tone of orange is used for all error messages in the encryption forms and in the game. 
 

### User Stories


- Upon entering the website, I immediately get the feeling of working with an old computer/command line.

- I want to see a navbar at the top of the screen.

- I want to see a large jumbotron/hero which sums up the most important features of the website. 

- As a learner, I would like to see a section which explains the two encryption/decryption methods used in the website, as well as examples and figures.

- I want to see a section beneath the learning section where I can try to encrypt and decrypt text in an easy way. 

- I would like to see a feature that lets me test what I have learned.

### Wireframes

The wireframes somewhat deviates from the finished website as some of the ideas and features came into existence after the planning process. Note that there is only wireframes for large and small screens. This is due to the simple structure of the website. There is only one breakpoint, so any screen under large (991px) will display the website in single columns.   

- [Learn and explore section](https://github.com/thorole/encryptinator/tree/master/wireframes/learn_forms_sections.pdf) | [Learn section mobile](https://github.com/thorole/encryptinator/tree/master/wireframes/small_screen.pdf)
- [Explore section mobile](https://github.com/thorole/encryptinator/tree/master/wireframes/explore_mobile.pdf)
- [Game](https://github.com/thorole/encryptinator/tree/master/wireframes/game.pdf) | [mobile](wireframes/game_small_screen.pdf)
- [Learn section expanded and modal](https://github.com/thorole/encryptinator/tree/master/wireframes/dropdown_expanded.pdf)



## Features

The website is divided into three main sections, all on the same page. The content is layed out in such a way that a user who has no experience with encryption can read through the learning section at the top, move on to the encryption forms and try it out for themselves, and finally test themselves in a simple game where the goal is to decrypt as many words as possible.   


### Nav bar and jumbotron
![Navbar and jumbotron](documentation/navjumbotron.PNG)

The navbar is custom built with flexbox. It consists of four navigation links which takes the user to the desired sections of the site. All links turn white on hover. The navbar does not collapse into a button on small screens, like you would usually see in webdesign these days. The reason for this is to maintain the illusion of a toolbar.

The jumbotron has two purposes. It displays the title of the website, and sumarizes its main features.

### Learning section
![Learning section](documentation/learningsection.PNG)

This section is part of the meat and potatos of the website. It is key for users without any knowledge of encryption to read through this section in order to understand the other two sections of the website. However, the learning section works fine on its own, and she's/he's not required to try out the later sections.

The learning section features two sub sections, one for each encryption method. Both sub sections have buttons that lets the user expand or collapse it. The main purpose for this is that these sections are relatively long, and being able to collapse them when a user has read through the content makes the website easier to navigate, and visually more tidied.

Each subsection contains information on how encryption works when using Cesar cipher and Vigenere cipher. There are also figures present to aid the user in understanding the concepts. Both figures opens in a modal on click and displays even further explaining and examples. Modals close by either clicking on the close symbol (X) or by clicking anywhere in the window.

### Explore section
![Explore section](documentation/exploreforms.PNG)

In this section the user can try out encrypting/decrypting text on their own. Both forms are built in a similar way. The user enters some text in the appropriate textfield, sets the shift or key, and then click encrypt or decrypt button. If the user don't enter any text in the textfield, or fails to meet the required format of the shift or key, an error message will be displayed over the current input element. This message briefly explains what the user must do to make it right.

The Vigenere Cipher form also sports an option to generate a key. This functionality uses an API to retrieve a random word. The drawback of this functionality is that if you request many words repeatedly, you're timed out for a few seconds. If this happens, the user will also be notified in the same way as explained in the last paragraph. Optionally, in the mean time, the user can just enter their own key instead if they don't wish to wait.

It is also worth mentioning that all input areas are highlighted with a green glow around the borders when focused. There are also "clear" buttons present to quickly clear all the text areas.

### Game
![Game](documentation/game.PNG)

The game is an additional feature of the website, and is meant to be a fun and quick way to test your own decryption skills. It has a very simple interface that displays a blinking start button, and on click starts the game. For each level there's a word displayed that the user must try to decrypt before the time runs out. The encryption is based on the Cesar cipher and both the shift and length of the current word changes as the user makes progress through the levels. 

The game screen displays the current shift, score, timer, the word to be decrypted, "check" button, exit button, and the alphabet.  

The check button is used to submit the answer. If wrong, the user gets an error message. The same happens if the input field is empty. The exit button takes you back to the blinking "start game" screen.

The alphabet is there to help the user traverse the letters in the alphabet according to the current shift. Note that all decryption fields in the forms are disabled when the game is active.

Between each level, the game displays a success message and your current score. The "next level" button takes you to the next stage. If the user fails to decrypt the word before time's up, the game displays a game over screen with your final score and a "back to start" button that takes you back to the "start game" screen.

**_Note to assessors and testers:_** There's a hidden feature at the end of the game. If the user fails to decrypt the final word, the website is encrypted and rendered unusable. If this happens, a "restore website" button appears fixed on screen, which refreshes the browser on click. If you wish to experience this feature without playing through the game, click repeatedly (up to 15 times) on the copyright symbol in the footer of the page. The cursor turns to crosshairs when you hover over the correct spot. This will take you directly to the last level. Please note that this only works when the game is not active and the blinking "start game" button is displayed. This is easiest achieved on a larger screen when using a mouse.

### Features Left to Implement
All of the features that was planned for on this website was executed. However, there are a few ideas which could be implemented in the future.

- Let the user encrypt a text, enter an email address and send the encrypted text to that email with a short explanation on how to decrypt the message, using the same website.

- Build out the game so that it involves both decryption and encryption. In addition, the user could set difficulty before starting the game.

## Technologies Used

- [VS Code](https://code.visualstudio.com/)
- [HTML5](https://www.w3.org/) 
- [CSS3](https://www.w3.org/)
- [JavaScript](https://www.javascript.com/)
- [jQuery](https://jquery.com/)
- [Bootstrap](https://www.getbootstrap.com)
- [Google Fonts](https://fonts.google.com/)
- [Wordnik API](https://developer.wordnik.com/) - Retrieves random word
- [Jasmine](https://jasmine.github.io/)
- [Node.js](https://nodejs.org/en/) - In the early stages, node.js was used to run javascript on the cli.
- [npm-package: http-server](https://www.npmjs.com/package/http-server) - Used to set up a server in development.

 
## Testing

The testing of the website, both in development and as a finished product has been done through both manual testing and automated testing (jasmine). As the manual test documentation became very long, it can be viewed in [this document](https://github.com/thorole/encryptinator/blob/master/TESTING.md).

The automated testing tests the functionality of the encryption/decryption forms. All the test can be viewed in [this file](https://github.com/thorole/encryptinator/blob/master/testing/spec/functionSpecs.js). You can view the test results [here](https://thorole.github.io/encryptinator/testing/test.html).

### Bug report

Through out development, there has been a series of minor and more complex bugs. The most important tool for debuggin has been the browser console in chrome. Here's how the console would typically look like during development.

Debugging forms
![Testing the forms](testing/images/consoletestingforms.png)

Debugging game
![Testing game](testing/images/consoletestinggame.png)

One of the more interesting bugs was discovered in automated testing. When passing numbers through the shift input field, the number was handled as a string, which again led to errors. This led to the re-writing of the function `checkShift()`. In the later stages of the project, the built in javascript method `checkValidity()` was introduced to the project to check all the input fields before the rest of the functions are called. This makes `checkShift()`, `writeDefaultKey()` and `writeDefaultShift()` a bit redundant but they were kept as an extra safety.



### Testing and Responsiveness across browsers and devices
The website was built and tested in Chrome throughout the construction. In addition it has been tested
in Mozilla Firefox, MS Edge and Mac OS Safari. The website is responsive as intended across
all browsers used in testing.

The website has also been tested physically on iPhone S, ipad 2nd gen., iPhone 7 and Mi a2 Redmi note 7.
The website responds well to smaller screen sizes and no major problems have appeared. The intention
is that on medium to small screens the website is layed out in a single column. During construction the site was constantly tested on phone sized
screen in the Chrome dev. tools to make sure it looked good and behaved as intended.

#### Tools used in testing
- [JsHint](https://jshint.com/) (0 warnings. Please note that there will be warnings of unused variables if you test each file individually. This is because game.js uses functions from encryption.js. JsHint will, of course, not detect this if not all the code is pasted in.)
- [W3C Markup Validation](https://validator.w3.org/) (0 errors in html.)
- [W3C CSS Validation](https://jigsaw.w3.org/css-validator/#validate_by_input)(0 errors, 17 warnings of unknown vendor extensions.) 
- [Accessibility checker](https://www.achecker.ca) (No known problems.)
- [Node.js](https://nodejs.org/en/) - In the early stages, node.js was used to run javascript on the cli.
- [npm-package: http-server](https://www.npmjs.com/package/http-server) - Used to set up a server in development.
- [Autoprefixer](https://autoprefixer.github.io/)
- [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools)
- [Jasmine](https://jasmine.github.io/)

## Deployment

**This procedure was followed to deploy Encryptinator**

1. Navigate to the [repository](https://github.com/thorole/encryptinator)
2. Select [Branch: master]
3. Go to settings
4. Scroll down to "Github Pages". Make sure the repo is set to public in "Danger Zone"-section beneath. 
5. Select [master branch] 
6. Refresh setting page and scroll down to "Github pages" to view the live website URL.

**To clone the repository, follow these instructions:**

1. Navigate to the [repository](https://github.com/thorole/encryptinator)
2. Click **Clone or download**
3. Copy the url from the **Clone or download** dropdown.
4. In cli, navigate to the folder where you want to clone the repository.
5. Type *git clone*, and then paste the URL you copied in Step 3.
6. Press Enter 

For more information, visit [Cloning a repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)
on github.

## Credits

### Content
The figure image in the cesar cipher learn section was taken from [Wikipedia](https://no.wikipedia.org/wiki/C%C3%A6sarchiffer). Most of the facts in the learn section was also taken from the same Wikipedia page.


### Acknowledgements

This template heavilly inspired the website and was used as a _visual reference_ to create a command line themed website. None of the actual code behind the template was used.
https://brobin.github.io/hacker-bootstrap/

Thanks to my mentor [Jonathan Munz](https://github.com/jpmunz) for guidance on the project and for providing online litterature.

This site was used to double check that the encryption/decryption forms was working correctly in development.
https://cryptii.com/pipes/vigenere-cipher

